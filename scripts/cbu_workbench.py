#!/usr/bin/env python3
"""ME201W CBU bench inventory and explicit read-only factory backup.

No command here writes/erases target flash. `preflight` never opens a serial
device. `backup` opens the requested serial port and reads flash twice, so run
it only after physical wiring/power checks. Raw outputs contain secrets.
"""

import argparse
import datetime
import fcntl
import glob
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys

FLASH_BYTES = 0x200000


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def port_owners(port):
    tool = shutil.which("fuser")
    if not tool:
        raise RuntimeError("fuser is required to check for competing serial readers")
    result = subprocess.run([tool, str(port)], capture_output=True, text=True,
                            timeout=5)
    if result.returncode not in (0, 1):
        raise RuntimeError("Could not establish serial port ownership")
    pids = [int(p) for p in result.stdout.split() if p.isdigit()]
    return pids


def preflight(args):
    ports = sorted(set(glob.glob("/dev/serial/by-id/*") +
                       glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")))
    report = {
        "checked_at": utc_now(),
        "workdir": str(args.workdir),
        "python": sys.version.split()[0],
        "disk_free_bytes": shutil.disk_usage(args.workdir).free,
        "serial_ports": [{"path": p, "resolved_path": str(Path(p).resolve()),
                          "owner_pids": port_owners(p)} for p in ports],
        "serial_opened": False,
        "flash_written": False,
        "status": "adapter_present_wiring_not_verified" if ports else
                  "waiting_for_usb_uart_adapter",
    }
    print(json.dumps(report, indent=2))


def read_command(args, output):
    return [str(args.workdir / "venv/bin/python"), "-m", "ltchiptool", "flash",
            "read", "bk7231n", str(output), "--device", args.port,
            "--baudrate", "115200", "--start", "0x0", "--length", "0x200000",
            "--timeout", "30", "--check"]


def backup(args):
    if args.dry_run:
        print(json.dumps({"commands": [read_command(args, Path("PRIVATE_BACKUP_DIR") /
              f"factory-{i}.private.bin") for i in (1, 2)],
              "serial_opened": False, "flash_written": False}, indent=2))
        return
    device = Path(args.port)
    if not device.exists() or not stat.S_ISCHR(device.stat().st_mode):
        raise RuntimeError("Select the attached USB-UART character device explicitly")
    if port_owners(device):
        raise RuntimeError("Serial port is already in use; close the other reader")
    if shutil.disk_usage(args.workdir).free < 32 * 1024 * 1024:
        raise RuntimeError("At least 32 MiB of free space is required")
    os.umask(0o077)
    with (args.workdir / "backup.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        out = args.workdir / "backups" / stamp
        out.mkdir(parents=True, exist_ok=False, mode=0o700)
        copies = []
        for i in (1, 2):
            if port_owners(device):
                raise RuntimeError("Serial port became busy; close the other reader")
            target = out / f"factory-{i}.private.bin"
            log = out / f"read-{i}.private.log"
            print(f"Read {i}/2: while the tool connects, briefly bridge CEN to GND and release immediately.",
                  flush=True)
            with log.open("wb") as handle:
                result = subprocess.run(read_command(args, target), stdout=handle,
                                        stderr=subprocess.STDOUT, timeout=900)
            if result.returncode:
                raise RuntimeError(f"Read {i} failed; private diagnostic log: {log}")
            data = target.read_bytes()
            if len(data) != FLASH_BYTES:
                raise RuntimeError(f"Read {i}: expected 2097152 bytes; got {len(data)}")
            if data == b"\x00" * FLASH_BYTES or data == b"\xff" * FLASH_BYTES:
                raise RuntimeError(f"Read {i} is uniformly blank; no verified backup")
            copies.append({"file": target.name, "bytes": len(data),
                           "sha256": hashlib.sha256(data).hexdigest()})
        if copies[0]["sha256"] != copies[1]["sha256"]:
            raise RuntimeError("Factory reads differ; preserve both and inspect before writing")
        receipt = {"verified_at": utc_now(), "port": args.port, "family": "bk7231n",
                   "copies": copies, "two_reads_identical": True,
                   "flash_written": False, "requires_second_host_copy": True}
        (out / "backup-receipt.private.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps({"status": "two_identical_reads", "private_backup_dir": str(out),
                          "bytes_each": FLASH_BYTES, "sha256": copies[0]["sha256"],
                          "next": "Copy backup to a second private host and verify its SHA256."},
                         indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, required=True,
                        help="private workbench root containing venv; never the public checkout")
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("preflight", help="inventory only; never opens a serial device")
    read = sub.add_parser("backup", help="read full 2 MiB flash twice; never write/erase")
    read.add_argument("--port", required=True, help="explicit /dev/serial/by-id/... path preferred")
    read.add_argument("--dry-run", action="store_true", help="print commands without serial access")
    args = parser.parse_args()
    args.workdir = args.workdir.resolve()
    try:
        checkout = Path(__file__).resolve().parents[1]
        if (checkout / '.git').exists() and (
                args.workdir == checkout or checkout in args.workdir.parents):
            raise RuntimeError("Keep the private workbench outside this source checkout")
        (preflight if args.operation == "preflight" else backup)(args)
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"Stopped: {exc}\n")


if __name__ == "__main__":
    main()
