import argparse
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import cbu_workbench as workbench


class BackupChecks(unittest.TestCase):
    def test_dry_run_never_calls_subprocess(self):
        args = argparse.Namespace(workdir=Path('/not-created'), port='/not-opened', dry_run=True)
        with patch.object(workbench.subprocess, 'run') as run, contextlib.redirect_stdout(io.StringIO()):
            workbench.backup(args)
        run.assert_not_called()

    def test_busy_port_never_starts_a_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            port = base / 'fake-port'
            port.touch()
            args = argparse.Namespace(workdir=base, port=str(port), dry_run=False)
            with patch.object(workbench, 'port_owners', return_value=[123]), \
                 patch.object(workbench.stat, 'S_ISCHR', return_value=True), \
                 patch.object(workbench.subprocess, 'run') as run:
                with self.assertRaisesRegex(RuntimeError, 'already in use'):
                    workbench.backup(args)
                run.assert_not_called()
            self.assertFalse((base / 'backups').exists())

    def exercise_reads(self, payloads):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            port = base / 'fake-port'
            port.touch()
            args = argparse.Namespace(workdir=base, port=str(port), dry_run=False)
            def run(command, **kwargs):
                self.assertEqual(command[3:6], ['flash', 'read', 'bk7231n'])
                self.assertNotIn('write', command)
                Path(command[6]).write_bytes(payloads.pop(0))
                return argparse.Namespace(returncode=0)
            with patch.object(workbench, 'port_owners', return_value=[]), \
                 patch.object(workbench.stat, 'S_ISCHR', return_value=True), \
                 patch.object(workbench.subprocess, 'run', side_effect=run), \
                 contextlib.redirect_stdout(io.StringIO()):
                try:
                    workbench.backup(args)
                except RuntimeError:
                    self.assertFalse(list(base.glob('backups/*/backup-receipt.private.json')))
                    raise
            receipt = list(base.glob('backups/*/backup-receipt.private.json'))
            self.assertEqual(len(receipt), 1)
            data = json.loads(receipt[0].read_text())
            self.assertTrue(data['two_reads_identical'])
            self.assertFalse(data['flash_written'])

    def test_matching_full_reads_succeed(self):
        data = b'\x00\xff' * (workbench.FLASH_BYTES // 2)
        self.exercise_reads([data, data])

    def test_different_reads_never_create_success_receipt(self):
        first = b'\x00\xff' * (workbench.FLASH_BYTES // 2)
        second = b'\x01\xfe' * (workbench.FLASH_BYTES // 2)
        with self.assertRaisesRegex(RuntimeError, 'reads differ'):
            self.exercise_reads([first, second])

    def test_truncated_read_never_creates_success_receipt(self):
        with self.assertRaisesRegex(RuntimeError, 'expected 2097152'):
            self.exercise_reads([b'partial'])

    def test_blank_read_never_creates_success_receipt(self):
        with self.assertRaisesRegex(RuntimeError, 'uniformly blank'):
            self.exercise_reads([b'\xff' * workbench.FLASH_BYTES])


if __name__ == '__main__':
    unittest.main()
