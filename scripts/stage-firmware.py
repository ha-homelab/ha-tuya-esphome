#!/usr/bin/env python3
"""Check initial-loader constraints before staging a private ESP8266 image."""
import argparse
import hashlib
import os
import stat
from pathlib import Path
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("firmware", type=Path)
parser.add_argument("--root", type=Path, default=Path(os.environ.get("WORKBENCH_ROOT", "/opt/tuya-workbench")))
args = parser.parse_args()
try:
    descriptor = os.open(args.firmware, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(descriptor, "rb") as source:
        if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
            parser.error("Firmware must be a regular file.")
        # Bound memory even if the file grows after metadata inspection.
        data = source.read(524288 + 1)
except OSError:
    parser.error("Cannot open a regular firmware file.")
if not 4096 < len(data) <= 524288:
    raise SystemExit(f"Invalid first-image size: {len(data)} bytes; limit is 524288.")
if data[0] != 0xE9:
    raise SystemExit("Missing ESP image header; do not flash this file.")
destination = args.root / "tuya-convert/files/esphome-initial.bin"
if not destination.parent.is_dir():
    raise SystemExit("Run workbench setup first.")
temporary = None
try:
    # Create privately from the first byte, then replace the staged image atomically.
    with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=".firmware-", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(data)
    os.replace(temporary, destination)
finally:
    if temporary is not None:
        temporary.unlink(missing_ok=True)
print(f"Staged ESP image: {len(data)} bytes, SHA-256 {hashlib.sha256(data).hexdigest()}")
print("Chip/flash layout must still match the actual unit. The image contains private credentials.")
