"""Exercise the client/event contract without a real network or relay."""

import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from aioesphomeapi import TextSensorInfo, TextSensorState
from controller import Frame, Kind, encode
from run_pilot import ApiTransport

KEY = bytes(range(32))
GET = encode(KEY, Frame(Kind.GET, 11, 0, 0))
ANSWER = encode(KEY, Frame(Kind.SNAPSHOT, 11, 22, 0))


class FakeApi:
    def __init__(self, *_args, **_kwargs):
        self.is_connected = False
        self.block_inventory = False
        self.inventory_start = asyncio.Event()
        self.discovery_count = 0
        self.callback = None

    async def connect(self, **_kwargs):
        self.is_connected = True

    async def list_entities_services(self):
        self.discovery_count += 1
        self.inventory_start.set()
        if self.block_inventory:
            await asyncio.Future()
        return [TextSensorInfo(name="Pilot Reply", key=123)], [
            SimpleNamespace(name="pilot_exchange")
        ]

    def subscribe_states(self, callback):
        self.callback = callback

    async def execute_service(self, service, data):
        assert service.name == "pilot_exchange" and bytes.fromhex(data["frame"]) == GET
        self.callback(TextSensorState(key=123, state="not hex"))
        self.callback(TextSensorState(key=345, state=ANSWER.hex()))
        old = encode(KEY, Frame(Kind.SNAPSHOT, 10, 22, 1))
        self.callback(TextSensorState(key=123, state=old.hex()))
        self.callback(TextSensorState(key=123, state=ANSWER.hex()))

    async def disconnect(self, *, force):
        assert force
        self.is_connected = False


class AdapterTests(unittest.IsolatedAsyncioTestCase):
    async def test_inventory_cancellation_retries_setup_and_ignores_stale_replies(self):
        with patch("run_pilot.APIClient", FakeApi):
            route = ApiTransport("example.invalid", "build-only", "bench", KEY)
        route.client.block_inventory = True
        first = asyncio.create_task(route.exchange(GET))
        await route.client.inventory_start.wait()
        first.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await first
        route.client.block_inventory = False
        self.assertEqual(await route.exchange(GET), ANSWER)
        self.assertEqual(route.client.discovery_count, 2)
        route.client.is_connected = False
        self.assertEqual(await route.exchange(GET), ANSWER)
        self.assertEqual(route.client.discovery_count, 3)
        await route.close()
        self.assertFalse(route.client.is_connected)
