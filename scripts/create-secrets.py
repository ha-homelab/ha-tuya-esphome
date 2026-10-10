#!/usr/bin/env python3
"""Create private ESPHome secrets without printing their values."""
import base64
import getpass
import json
import os
from pathlib import Path
import secrets
import sys

destination = Path(sys.argv[1] if len(sys.argv) > 1 else "secrets.yaml")
if destination.exists():
    raise SystemExit("Destination exists; refusing to replace device credentials.")
ssid = input("Wi-Fi SSID (stored only locally): ").strip()
password = getpass.getpass("Wi-Fi password: ")
if not ssid or not password:
    raise SystemExit("SSID and password are required.")
values = {
    "wifi_ssid": ssid,
    "wifi_password": password,
    "api_encryption_key": base64.b64encode(secrets.token_bytes(32)).decode(),
    "fallback_password": secrets.token_urlsafe(18),
}
with os.fdopen(os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as stream:
    json.dump(values, stream, indent=2)
    stream.write("\n")
print("Private secrets created. Do not commit them or a firmware containing them.")
