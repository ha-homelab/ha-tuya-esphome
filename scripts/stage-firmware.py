#!/usr/bin/env python3
"""Check initial-loader constraints before staging a private ESP8266 image."""
import argparse
import hashlib
import os
from pathlib import Path
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("firmware", type=Path)
parser.add_argument("--root", type=Path, default=Path(os.environ.get("WORKBENCH_ROOT", "/opt/tuya-workbench")))
args = parser.parse_args()
data = args.firmware.read_bytes()
if not 4096 < len(data) <= 524288:
    raise SystemExit(f"Invalid first-image size: {len(data)} bytes; limit is 524288.")
if data[0] != 0xE9:
    raise SystemExit("Missing ESP image header; do not flash this file.")
destination = args.root / "tuya-convert/files/esphome-initial.bin"
if not destination.parent.is_dir():
    raise SystemExit("Run workbench setup first.")
shutil.copyfile(args.firmware, destination)
destination.chmod(0o600)
print(f"Staged ESP image: {len(data)} bytes, SHA-256 {hashlib.sha256(data).hexdigest()}")
print("Chip/flash layout must still match the actual unit. The image contains private credentials.")
