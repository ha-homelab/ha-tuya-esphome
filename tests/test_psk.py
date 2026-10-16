"""Verify legacy Tuya binary-identity TLS on loopback, without any device."""
import socket
import ssl
from concurrent.futures import ThreadPoolExecutor

import sslpsk3 as sslpsk

identity = b"\xff\xfe\x01TuyaBinaryIdentity"
key = b"0123456789abcdef"
listener = socket.socket()
listener.bind(("127.0.0.1", 0))
listener.listen(1)
listener.settimeout(5)


def server():
    conn, _ = listener.accept()
    conn.settimeout(5)
    with sslpsk.wrap_socket(
        conn,
        server_side=True,
        ssl_version=ssl.PROTOCOL_TLSv1_2,
        ciphers="PSK-AES128-CBC-SHA256",
        psk=lambda received: key if received == identity else b"",
        hint=b"test",
    ) as wrapped:
        assert wrapped.recv(4) == b"ping"
        wrapped.sendall(b"pong")


with ThreadPoolExecutor(max_workers=1) as pool:
    result = pool.submit(server)
    conn = socket.create_connection(listener.getsockname(), timeout=5)
    with sslpsk.wrap_socket(
        conn,
        ssl_version=ssl.PROTOCOL_TLSv1_2,
        ciphers="PSK-AES128-CBC-SHA256",
        psk=(key, identity),
    ) as wrapped:
        wrapped.sendall(b"ping")
        assert wrapped.recv(4) == b"pong"
    result.result(timeout=5)
listener.close()
print("PASS: TLS 1.2 PSK handshake with binary Tuya identity")

# Exercise the exact patched upstream derivation, without publishing its key.
import contextlib
import importlib.util
import io
from pathlib import Path

spec = importlib.util.spec_from_file_location("tuya_psk_frontend", Path.cwd() / "scripts/psk-frontend.py")
frontend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frontend)
output = io.StringIO()
with contextlib.redirect_stdout(output):
    derived = frontend.gen_psk(bytes([1]) + frontend.IDENTITY_PREFIX + bytes(16), bytes(32))
assert len(derived) == 32
assert derived.hex() not in output.getvalue()
assert "PSK:" not in output.getvalue()
print("PASS: upstream derivation does not log session PSKs")
