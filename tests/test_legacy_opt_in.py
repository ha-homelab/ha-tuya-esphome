"""The default launcher must not touch privileges, networks or devices."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "bin" / "tuya-convert"


class LegacyOptInTests(unittest.TestCase):
    def invoke(self, arguments):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker = root / "called"
            for name in ("sudo", "ip", "docker", "iw", "rfkill"):
                command = root / name
                command.write_text('#!/bin/sh\nprintf "%s\\n" "$0" >> "$TEST_CALL_MARKER"\nexit 77\n')
                command.chmod(0o700)
            env = {**os.environ, "PATH": str(root) + os.pathsep + os.defpath,
                   "TEST_CALL_MARKER": str(marker)}
            result = subprocess.run(["/bin/bash", str(SCRIPT), *arguments],
                                    env=env, capture_output=True, text=True, check=False)
            calls = marker.read_text().splitlines() if marker.exists() else []
            return result, calls

    def test_default_and_invalid_options_do_not_run_workbench_commands(self):
        for arguments in ([], ["--unknown"], ["--allow-insecure-legacy-protocol", "extra"]):
            with self.subTest(arguments=arguments):
                result, calls = self.invoke(arguments)
                self.assertEqual(result.returncode, 2)
                self.assertIn("USB provisioning", result.stderr)
                self.assertEqual(calls, [])

    def test_help_performs_no_workbench_operation(self):
        result, calls = self.invoke(["--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("encrypted ESPHome", result.stdout)
        self.assertEqual(calls, [])

    def test_explicit_opt_in_reaches_only_mocked_privilege_boundary(self):
        result, calls = self.invoke(["--allow-insecure-legacy-protocol"])
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(calls), 1)
        self.assertEqual(Path(calls[0]).name, "ip" if os.geteuid() == 0 else "sudo")
