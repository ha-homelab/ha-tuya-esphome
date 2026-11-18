"""Run one authenticated exchange with an isolated virtual-relay bench."""

import argparse
import asyncio
import json
from dataclasses import asdict
from pathlib import Path

import tomllib
from aioesphomeapi import APIClient, APIConnectionError, TextSensorInfo, TextSensorState
from controller import (
    Controller,
    FrameError,
    Kind,
    Route,
    TransportError,
    UnconfirmedError,
    decode,
)

BLE_COMMAND = "ec3d570f-f92c-4c06-b300-1ca1e173a911"
BLE_REPLY = "ec3d570f-f92c-4c06-b300-1ca1e173a912"


def matches(key: bytes, request, wire: bytes) -> bool:
    try:
        reply = decode(key, wire)
    except FrameError:
        return False
    expected = Kind.SNAPSHOT if request.kind is Kind.GET else Kind.RESULT
    return (
        reply.request_id == request.request_id
        and reply.kind is expected
        and (expected is Kind.SNAPSHOT or reply.token == request.token)
    )


class ApiTransport:
    def __init__(self, host: str, psk: str, name: str, key: bytes):
        self.client = APIClient(host, 6053, None, noise_psk=psk, expected_name=name)
        self.key = key
        self.service = None
        self.pending = None

    def _receive(self, state):
        if not self.pending or not isinstance(state, TextSensorState):
            return
        request, result = self.pending
        if state.key != self.reply_key or state.missing_state or result.done():
            return
        try:
            wire = bytes.fromhex(state.state)
        except ValueError:
            return
        if matches(self.key, request, wire):
            result.set_result(wire)

    async def _connect(self):
        if not self.client.is_connected:
            self.service = None
            await self.client.connect(login=True, log_errors=False)
        if self.service is None:
            entities, services = await self.client.list_entities_services()
            service = next((x for x in services if x.name == "pilot_exchange"), None)
            reply = next(
                (
                    x
                    for x in entities
                    if isinstance(x, TextSensorInfo) and x.name == "Pilot Reply"
                ),
                None,
            )
            if service is None or reply is None:
                raise TransportError("bench API action or reply sensor is missing")
            self.reply_key = reply.key
            self.client.subscribe_states(self._receive)
            self.service = service

    async def exchange(self, frame: bytes) -> bytes:
        try:
            await self._connect()
            result = asyncio.get_running_loop().create_future()
            self.pending = (decode(self.key, frame), result)
            await self.client.execute_service(self.service, {"frame": frame.hex()})
            return await result
        except APIConnectionError as exc:
            raise TransportError("bench API unavailable") from exc
        finally:
            self.pending = None

    async def close(self):
        await self.client.disconnect(force=True)


class BleTransport:
    def __init__(self, address: str, key: bytes):
        from bleak import BleakClient, BleakError

        self.client = BleakClient(address)
        self.error = BleakError
        self.key = key

    async def exchange(self, frame: bytes) -> bytes:
        request = decode(self.key, frame)
        try:
            if not self.client.is_connected:
                await self.client.connect()
            await self.client.write_gatt_char(BLE_COMMAND, frame, response=True)
            while True:
                wire = bytes(await self.client.read_gatt_char(BLE_REPLY))
                if matches(self.key, request, wire):
                    return wire
                await asyncio.sleep(0.1)
        except self.error as exc:
            raise TransportError("bench BLE unavailable") from exc

    async def close(self):
        if self.client.is_connected:
            await self.client.disconnect()


async def operate(config, command):
    key = bytes.fromhex(config["command_key"])
    if key in (bytes(32), bytes(range(32))):
        raise ValueError("generate a unique command key for this bench")
    routes = [
        Route(
            "esp-now",
            ApiTransport(**config["gateway"], name="failover-lab-gateway", key=key),
            1.0,
        ),
    ]
    if satellite := config.get("satellite"):
        routes.append(
            Route(
                "wi-fi",
                ApiTransport(**satellite, name="failover-lab-satellite", key=key),
                1.0,
            )
        )
    if address := config.get("ble_address"):
        routes.append(Route("ble", BleTransport(address, key), 1.5))
    try:
        controller = Controller(key, routes, command_timeout=4.5)
        outcome = await (
            controller.read_state()
            if command == "state"
            else controller.set_state(command == "on")
        )
        print(json.dumps(asdict(outcome)))
        return 0
    except UnconfirmedError as exc:
        print(
            json.dumps(
                {
                    "error": str(exc),
                    "may_have_applied": exc.may_have_applied,
                    "attempts": [asdict(attempt) for attempt in exc.attempts],
                }
            )
        )
        return 1
    finally:
        await asyncio.gather(
            *(route.transport.close() for route in routes), return_exceptions=True
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("command", choices=("state", "on", "off"))
    args = parser.parse_args()
    with args.config.open("rb") as source:
        config = tomllib.load(source)
    return asyncio.run(operate(config, args.command))


if __name__ == "__main__":
    raise SystemExit(main())
