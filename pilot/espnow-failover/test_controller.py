import asyncio
import hmac
import unittest

from controller import (
    HEADER,
    BusyError,
    Controller,
    Frame,
    FrameError,
    Kind,
    Route,
    TransportError,
    UnconfirmedError,
    decode,
    encode,
)

KEY = bytes(range(32))


class FrameTests(unittest.TestCase):
    def test_shared_wire_vector(self):
        frame = Frame(Kind.SET, 0x0102030405060708, 0x1112131415161718, 1)
        wire = bytes.fromhex(
            "010301020304050607081112131415161718012469e6ce27de476370189587d7f02a45"
        )
        self.assertEqual(encode(KEY, frame), wire)
        self.assertEqual(decode(KEY, wire), frame)

    def test_decode_rejects_wrong_key_corruption_and_length(self):
        valid = encode(KEY, Frame(Kind.GET, 1, 0, 0))
        cases = (
            (KEY[::-1], valid),
            (KEY, valid[:-1] + bytes([valid[-1] ^ 1])),
            (KEY, valid[:-1]),
            (KEY, b"\x00" + valid),
        )
        for key, wire in cases:
            with self.subTest(key=key, wire=wire), self.assertRaises(FrameError):
                decode(key, wire)

    def test_authenticated_invalid_fields_are_still_rejected(self):
        cases = (
            (2, 1, 8, 0, 0),  # version
            (1, 9, 8, 0, 0),  # kind
            (1, 1, 0, 0, 0),  # request ID
            (1, 1, 8, 3, 0),  # GET token
            (1, 1, 8, 0, 1),  # GET state
            (1, 2, 8, 0, 0),  # SNAPSHOT token
            (1, 3, 8, 1, 2),  # desired state
        )
        for fields in cases:
            header = HEADER.pack(*fields)
            wire = header + hmac.digest(KEY, header, "sha256")[:16]
            with self.subTest(fields=fields), self.assertRaises(FrameError):
                decode(KEY, wire)


class Endpoint:
    """One shared fake device behind two routes, with a single request token."""

    def __init__(self):
        self.state = 0
        self.transitions = 0
        self._tokens = {}
        self._results = {}

    def reply(self, frame):
        if frame.kind is Kind.GET:
            token = self._tokens.setdefault(frame.request_id, len(self._tokens) + 1)
            return Frame(Kind.SNAPSHOT, frame.request_id, token, self.state)
        if (
            frame.kind is not Kind.SET
            or self._tokens.get(frame.request_id) != frame.token
        ):
            raise TransportError("wrong token")
        if frame.request_id not in self._results:
            if self.state != frame.state:
                self.transitions += 1
                self.state = frame.state
            self._results[frame.request_id] = self.state
        return Frame(
            Kind.RESULT, frame.request_id, frame.token, self._results[frame.request_id]
        )


class TestPath:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.requests = []
        self.faults = {}

    async def exchange(self, wire):
        self.requests.append(wire)
        frame = decode(KEY, wire)
        if handler := self.faults.get(frame.kind):
            return await handler(frame)
        return encode(KEY, self.endpoint.reply(frame))


async def unreachable(_):
    raise TransportError("simulated link outage")


class ControllerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.endpoint = Endpoint()
        self.radio = TestPath(self.endpoint)
        self.wifi = TestPath(self.endpoint)
        self.routes = (Route("esp-now", self.radio), Route("wifi", self.wifi))
        self.controller = Controller(KEY, self.routes)

    async def test_primary_returns_actual_on_and_off(self):
        self.assertTrue((await self.controller.set_state(True)).state)
        result = await self.controller.set_state(False)
        self.assertFalse(result.state)
        self.assertEqual(
            (result.snapshot_route, result.result_route), ("esp-now", "esp-now")
        )
        self.assertEqual(self.endpoint.transitions, 2)
        self.assertFalse(self.wifi.requests)

    async def test_read_uses_only_get(self):
        reading = await self.controller.read_state()
        self.assertFalse(reading.state)
        self.assertEqual(reading.route, "esp-now")
        self.assertEqual(
            [decode(KEY, wire).kind for wire in self.radio.requests], [Kind.GET]
        )

    async def test_get_failover_reuses_wire_and_uses_reachable_path_for_set(self):
        self.radio.faults[Kind.GET] = unreachable
        result = await self.controller.set_state(True)
        self.assertEqual(self.radio.requests, self.wifi.requests[:1])
        self.assertEqual((result.snapshot_route, result.result_route), ("wifi", "wifi"))
        self.assertEqual(result.attempts[0].status, "unreachable")
        self.assertEqual(self.endpoint.transitions, 1)

    async def test_lost_set_response_retries_identical_bytes_without_double_transition(
        self,
    ):
        async def lost_ack(frame):
            self.endpoint.reply(frame)
            raise TimeoutError

        self.radio.faults[Kind.SET] = lost_ack
        result = await self.controller.set_state(True)
        self.assertEqual(
            (result.snapshot_route, result.result_route), ("esp-now", "wifi")
        )
        self.assertEqual(self.radio.requests[1:], self.wifi.requests)
        self.assertEqual(result.attempts[1].status, "timeout")
        self.assertEqual(self.endpoint.transitions, 1)

    async def test_ble_takes_over_when_both_ip_paths_fail(self):
        self.radio.faults[Kind.GET] = unreachable
        self.wifi.faults[Kind.GET] = unreachable
        ble = TestPath(self.endpoint)
        controller = Controller(KEY, (*self.routes, Route("ble", ble)))
        result = await controller.set_state(True)
        self.assertEqual((result.snapshot_route, result.result_route), ("ble", "ble"))
        self.assertEqual(self.radio.requests, ble.requests[:1])
        self.assertEqual(self.wifi.requests, ble.requests[:1])
        self.assertEqual(self.endpoint.transitions, 1)

    async def test_demotes_broken_path_and_rechecks_priority_when_cooldown_is_zero(
        self,
    ):
        self.radio.faults[Kind.GET] = unreachable
        await self.controller.set_state(True)
        self.radio.faults.clear()
        self.assertEqual((await self.controller.read_state()).route, "wifi")
        fresh = Controller(KEY, self.routes, cooldown=0)
        self.radio.faults[Kind.GET] = unreachable
        self.assertEqual((await fresh.read_state()).route, "wifi")
        self.radio.faults.clear()
        self.assertEqual((await fresh.read_state()).route, "esp-now")

    async def test_wrong_kind_id_token_state_and_auth_never_confirm(self):
        for fault in ("kind", "id", "token", "state", "tag"):
            with self.subTest(fault=fault):

                async def wrong_reply(frame, fault=fault):
                    kind = Kind.SNAPSHOT if fault == "kind" else Kind.RESULT
                    request_id = (
                        (frame.request_id % 2) + 1
                        if fault == "id"
                        else frame.request_id
                    )
                    token = frame.token + int(fault == "token")
                    state = 1 - frame.state if fault == "state" else frame.state
                    key = KEY[::-1] if fault == "tag" else KEY
                    return encode(key, Frame(kind, request_id, token, state))

                self.radio.faults[Kind.SET] = wrong_reply
                self.wifi.faults[Kind.SET] = unreachable
                with self.assertRaises(UnconfirmedError) as captured:
                    await self.controller.set_state(True)
                error = captured.exception
                self.assertEqual(error.phase, Kind.SET)
                self.assertTrue(error.may_have_applied)
                self.assertIn(
                    "invalid_response", [attempt.status for attempt in error.attempts]
                )
        self.assertEqual(self.endpoint.transitions, 0)

    async def test_no_get_means_no_set_is_sent(self):
        self.radio.faults[Kind.GET] = unreachable
        self.wifi.faults[Kind.GET] = unreachable
        with self.assertRaises(UnconfirmedError) as captured:
            await self.controller.set_state(True)
        self.assertEqual(captured.exception.phase, Kind.GET)
        self.assertFalse(captured.exception.may_have_applied)
        self.assertEqual(self.radio.requests, self.wifi.requests)
        self.assertEqual(len(self.radio.requests), 1)

    async def test_lost_set_on_all_paths_is_unknown_until_reconciled(self):
        async def lost_ack(frame):
            self.endpoint.reply(frame)
            raise TimeoutError

        self.radio.faults[Kind.SET] = lost_ack
        self.wifi.faults[Kind.SET] = lost_ack
        with self.assertRaises(UnconfirmedError) as captured:
            await self.controller.set_state(True)
        self.assertTrue(captured.exception.may_have_applied)
        self.assertTrue((await self.controller.read_state()).state)
        self.assertEqual(self.endpoint.transitions, 1)

    async def test_slow_path_is_cancelled_before_fallback(self):
        closed = asyncio.Event()

        async def blocked(_):
            try:
                await asyncio.Event().wait()
            finally:
                closed.set()

        self.radio.faults[Kind.GET] = blocked
        controller = Controller(
            KEY, (Route("esp-now", self.radio, 0.02), self.routes[1])
        )
        self.assertEqual((await controller.set_state(True)).result_route, "wifi")
        self.assertTrue(closed.is_set())

    async def test_command_deadline_spans_routes_and_prevents_late_set(self):
        async def blocked(_):
            await asyncio.Event().wait()

        self.radio.faults[Kind.GET] = blocked
        controller = Controller(KEY, self.routes, command_timeout=0.02)
        with self.assertRaises(UnconfirmedError) as captured:
            await controller.set_state(True)
        self.assertFalse(captured.exception.may_have_applied)
        self.assertFalse(self.wifi.requests)

    async def test_busy_fails_immediately_and_cancellation_releases_controller(self):
        entered = asyncio.Event()

        async def blocked(_):
            entered.set()
            await asyncio.Event().wait()

        self.radio.faults[Kind.GET] = blocked
        first = asyncio.create_task(self.controller.set_state(True))
        await asyncio.wait_for(entered.wait(), 1)
        with self.assertRaises(BusyError):
            await self.controller.set_state(False)
        with self.assertRaises(BusyError):
            await self.controller.read_state()
        first.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await first
        self.radio.faults.clear()
        self.assertFalse((await self.controller.read_state()).state)
        self.assertEqual(self.endpoint.transitions, 0)


if __name__ == "__main__":
    unittest.main()
