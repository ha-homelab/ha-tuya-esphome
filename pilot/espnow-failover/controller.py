"""Transport-neutral controller for a single enrolled pilot endpoint.

Transport adapters deliver the same authenticated bytes over every path.
They must stop waiting and release their resources when cancelled. Late
responses are allowed on the wire but are never treated as a new request.
"""

import asyncio
import hmac
import math
import secrets
import struct
from collections.abc import Sequence
from dataclasses import dataclass
from enum import IntEnum
from typing import Protocol, overload


class Kind(IntEnum):
    GET = 1
    SNAPSHOT = 2
    SET = 3
    RESULT = 4


VERSION = 1
HEADER = struct.Struct("!BBQQB")
TAG_SIZE = 16
FRAME_SIZE = HEADER.size + TAG_SIZE
MAX_U64 = (1 << 64) - 1


@dataclass(frozen=True)
class Frame:
    kind: Kind
    request_id: int
    token: int
    state: int


class FrameError(ValueError):
    """The wire message is invalid or unauthenticated."""


def _validate_key(key: bytes) -> None:
    if not isinstance(key, bytes) or len(key) != 32:
        raise ValueError("key must contain exactly 32 bytes")


def _validate_fields(frame: Frame) -> None:
    if not isinstance(frame.kind, Kind):
        raise FrameError("unknown frame kind")
    if type(frame.request_id) is not int or not 0 < frame.request_id <= MAX_U64:
        raise FrameError("invalid request ID")
    if type(frame.token) is not int or not 0 <= frame.token <= MAX_U64:
        raise FrameError("invalid token")
    if type(frame.state) is not int or frame.state not in (0, 1):
        raise FrameError("invalid state")
    if frame.kind is Kind.GET:
        if frame.token != 0 or frame.state != 0:
            raise FrameError("GET must have zero token and state")
    elif frame.token == 0:
        raise FrameError("response or SET requires a nonzero token")


def encode(key: bytes, frame: Frame) -> bytes:
    _validate_key(key)
    _validate_fields(frame)
    header = HEADER.pack(
        VERSION, frame.kind, frame.request_id, frame.token, frame.state
    )
    return header + hmac.digest(key, header, "sha256")[:TAG_SIZE]


def decode(key: bytes, wire: bytes) -> Frame:
    _validate_key(key)
    if not isinstance(wire, bytes) or len(wire) != FRAME_SIZE:
        raise FrameError("invalid frame length or type")
    header, tag = wire[: HEADER.size], wire[HEADER.size :]
    if not hmac.compare_digest(tag, hmac.digest(key, header, "sha256")[:TAG_SIZE]):
        raise FrameError("invalid authentication tag")
    version, kind, request_id, token, state = HEADER.unpack(header)
    if version != VERSION:
        raise FrameError("unsupported frame version")
    try:
        message_kind = Kind(kind)
    except ValueError as exc:
        raise FrameError("unknown frame kind") from exc
    frame = Frame(message_kind, request_id, token, state)
    _validate_fields(frame)
    return frame


class Transport(Protocol):
    async def exchange(self, frame: bytes) -> bytes:
        """Send a frame and await one response for this exchange."""


class TransportError(Exception):
    """The adapter could not complete the exchange on this path."""


@dataclass(frozen=True)
class Route:
    name: str
    transport: Transport
    timeout: float = 1.0


@dataclass(frozen=True)
class Attempt:
    phase: Kind
    route: str
    status: str


@dataclass(frozen=True)
class Outcome:
    state: bool
    snapshot_route: str
    result_route: str
    attempts: tuple[Attempt, ...]


@dataclass(frozen=True)
class Reading:
    state: bool
    route: str
    attempts: tuple[Attempt, ...]


class BusyError(RuntimeError):
    """One command is already in progress. No later command is queued."""


class UnconfirmedError(RuntimeError):
    """No authenticated matching result was received for a phase."""

    def __init__(self, phase: Kind, attempts: list[Attempt]):
        super().__init__(f"no confirmed response for {phase.name}")
        self.phase = phase
        self.attempts = tuple(attempts)

    @property
    def may_have_applied(self) -> bool:
        """A missing SET result leaves the physical outcome unknown."""
        return any(attempt.phase is Kind.SET for attempt in self.attempts)


class Controller:
    def __init__(
        self,
        key: bytes,
        routes: Sequence[Route],
        *,
        cooldown: float = 10.0,
        command_timeout: float = 4.0,
    ):
        _validate_key(key)
        self._routes = tuple(routes)
        if not self._routes:
            raise ValueError("at least one route is required")
        names = {route.name for route in self._routes}
        if "" in names or len(names) != len(self._routes):
            raise ValueError("routes must have unique nonempty names")
        if any(
            not math.isfinite(route.timeout) or route.timeout <= 0
            for route in self._routes
        ):
            raise ValueError("route timeouts must be positive and finite")
        if not math.isfinite(cooldown) or cooldown < 0:
            raise ValueError("cooldown must be nonnegative and finite")
        # The receiver expires the first snapshot token after five seconds.
        if not math.isfinite(command_timeout) or not 0 < command_timeout < 5:
            raise ValueError(
                "command timeout must be positive and less than five seconds"
            )
        self._key = key
        self._cooldown = cooldown
        self._command_timeout = command_timeout
        self._retry_after: dict[str, float] = {}
        self._busy = False

    async def read_state(self) -> Reading:
        """Obtain a fresh state after startup or an unconfirmed command."""
        return await self._operate(None)

    async def set_state(self, desired: bool) -> Outcome:
        """Send one absolute command and return only after matching readback.

        An unconfirmed result or cancelled caller does not imply that the
        relay is unchanged. A caller can reconcile via a fresh state read.
        """
        if type(desired) is not bool:
            raise TypeError("desired state must be a bool")
        return await self._operate(desired)

    @overload
    async def _operate(self, desired: None) -> Reading: ...

    @overload
    async def _operate(self, desired: bool) -> Outcome: ...

    async def _operate(self, desired: bool | None) -> Reading | Outcome:
        if self._busy:
            raise BusyError("a command is already in progress")
        self._busy = True
        try:
            deadline = asyncio.get_running_loop().time() + self._command_timeout
            attempts: list[Attempt] = []
            request_id = secrets.randbelow(MAX_U64) + 1
            snapshot, snapshot_route = await self._exchange(
                Frame(Kind.GET, request_id, 0, 0), Kind.SNAPSHOT, deadline, attempts
            )
            if desired is None:
                return Reading(bool(snapshot.state), snapshot_route, tuple(attempts))
            result, result_route = await self._exchange(
                Frame(Kind.SET, request_id, snapshot.token, int(desired)),
                Kind.RESULT,
                deadline,
                attempts,
            )
            return Outcome(
                bool(result.state), snapshot_route, result_route, tuple(attempts)
            )
        finally:
            self._busy = False

    async def _exchange(
        self, request: Frame, expected: Kind, deadline: float, attempts: list[Attempt]
    ) -> tuple[Frame, str]:
        loop = asyncio.get_running_loop()
        now = loop.time()
        # Stable sort preserves configured priority among routes outside cooldown.
        routes = sorted(
            self._routes, key=lambda route: self._retry_after.get(route.name, now) > now
        )
        wire = encode(self._key, request)
        for route in routes:
            timeout = min(route.timeout, deadline - loop.time())
            if timeout <= 0:
                break
            try:
                reply = await asyncio.wait_for(route.transport.exchange(wire), timeout)
                if loop.time() >= deadline:
                    raise TimeoutError
                frame = decode(self._key, reply)
                if frame.kind is not expected or frame.request_id != request.request_id:
                    raise FrameError("response does not match this request")
                if expected is Kind.RESULT and (frame.token, frame.state) != (
                    request.token,
                    request.state,
                ):
                    raise FrameError(
                        "result does not confirm the requested state and token"
                    )
            except TimeoutError:
                status = "timeout"
            except (TransportError, OSError):
                status = "unreachable"
            except FrameError:
                status = "invalid_response"
            else:
                self._retry_after.pop(route.name, None)
                attempts.append(Attempt(request.kind, route.name, "confirmed"))
                return frame, route.name
            self._retry_after[route.name] = loop.time() + self._cooldown
            attempts.append(Attempt(request.kind, route.name, status))
        raise UnconfirmedError(request.kind, attempts)
