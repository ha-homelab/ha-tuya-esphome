#!/usr/bin/env python3
"""Reject common private artifacts and identifiers; not a full secret scanner."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
excluded = {".git", ".venv", "__pycache__"}
forbidden_suffixes = {".bin", ".elf", ".uf2", ".rbl", ".pcap", ".pcapng", ".tfplan", ".log"}
patterns = {
    "private IPv4": re.compile(r"\b(?:192[.]168[.]\d{1,3}[.]\d{1,3}|10[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|172[.](?:1[6-9]|2\d|3[01])[.]\d{1,3}[.]\d{1,3})\b"),
    "MAC identifier": re.compile(r"\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b"),
    "GitHub credential": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b"),
    "JWT-like credential": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
allowed = {"02:00:00:00:00:01"}  # Explicitly synthetic documentation MAC.
errors = []
for path in root.rglob("*"):
    relative = path.relative_to(root)
    if not path.is_file() or excluded.intersection(relative.parts):
        continue
    if path.suffix in forbidden_suffixes or path.name in {"secrets.yaml", ".env"} or ".tfstate" in path.name:
        errors.append(f"{relative}: private artifact filename")
        continue
    try:
        text = path.read_text()
    except UnicodeError:
        errors.append(f"{relative}: unexpected binary file")
        continue
    for label, pattern in patterns.items():
        if any(match.group() not in allowed for match in pattern.finditer(text)):
            errors.append(f"{relative}: {label}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("Publication guard passed. Also scan Git history and inspect the diff.")
