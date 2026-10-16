"""Real CLI staging with synthetic images only; no hardware or firmware."""
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/stage-firmware.py"


class StagingTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / "tuya-convert/files"
        self.directory.mkdir(parents=True)
        self.output = self.directory / "esphome-initial.bin"
        self.input = self.root / "synthetic.bin"

    def run_stage(self):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.input), "--root", str(self.root)],
                              capture_output=True, text=True, timeout=5, check=False)

    def test_success_creates_private_exact_image(self):
        data = bytes([0xE9]) + bytes(4096)
        self.input.write_bytes(data)
        result = self.run_stage()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.output.read_bytes(), data)
        self.assertEqual(stat.S_IMODE(self.output.stat().st_mode), 0o600)
        self.assertFalse(list(self.directory.glob('.firmware-*')))

    def test_invalid_header_and_lengths_preserve_previous_image(self):
        self.output.write_bytes(b'previous-image')
        for data in (bytes(4097), bytes([0xE9]) + bytes(4095), bytes([0xE9]) + bytes(524288)):
            with self.subTest(size=len(data)):
                self.input.write_bytes(data)
                self.assertNotEqual(self.run_stage().returncode, 0)
                self.assertEqual(self.output.read_bytes(), b'previous-image')
                self.assertFalse(list(self.directory.glob('.firmware-*')))

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'FIFO input requires POSIX')
    def test_fifo_is_rejected_without_waiting_for_a_writer(self):
        os.mkfifo(self.input)
        self.assertNotEqual(self.run_stage().returncode, 0)
        self.assertFalse(self.output.exists())

    @unittest.skipUnless(hasattr(os, 'O_NOFOLLOW'), 'No-follow open requires platform support')
    def test_symlink_is_rejected(self):
        actual = self.root / 'actual.bin'
        actual.write_bytes(bytes([0xE9]) + bytes(4096))
        self.input.symlink_to(actual)
        self.assertNotEqual(self.run_stage().returncode, 0)
        self.assertFalse(self.output.exists())
