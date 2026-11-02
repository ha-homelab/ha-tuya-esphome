"""Reject input/lock drift in both compiler and legacy protocol environments."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAIRS = [("requirements-firmware.txt", "requirements-firmware.lock"),
         ("requirements-build.in", "requirements-build.lock"),
         ("container/requirements-runtime.in", "container/requirements-runtime.lock"),
         ("container/requirements-build.in", "container/requirements-build.lock")]


def pins(path):
    return dict(re.findall(r"^([A-Za-z0-9_.-]+)==([^ ;\\\n]+)",
                           (ROOT / path).read_text(), re.MULTILINE))


class DependencyLockTests(unittest.TestCase):
    def test_direct_versions_are_current(self):
        for source, lock in PAIRS:
            direct, locked = pins(source), pins(lock)
            self.assertTrue(direct)
            self.assertEqual(direct, {name: locked.get(name) for name in direct})

    def test_every_dependency_has_artifact_hashes(self):
        for _, lock in PAIRS:
            entries = re.split(r"(?m)(?=^[A-Za-z0-9_.-]+==)", (ROOT / lock).read_text())[1:]
            self.assertTrue(entries)
            self.assertTrue(all("--hash=sha256:" in entry for entry in entries))

    def test_both_build_callers_supply_the_lock_context(self):
        for name in ["scripts/setup-workbench.sh", ".github/workflows/ci.yml"]:
            self.assertRegex((ROOT / name).read_text(), r'--build-context "?workbench-locks=')
