#!/usr/bin/env python3
"""Validate and compile a USB-provisionable encrypted device profile; never flash."""
import base64
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='tuya-firmware-check-') as directory:
        work = Path(directory)
        for name in ('tuya-plug.yaml', 'xs-ssa01-gpio15.yaml'):
            shutil.copyfile(root / 'examples' / name, work / name)
        (work / 'device.yaml').write_text(
            'packages:\n  base: !include tuya-plug.yaml\n  hardware: !include xs-ssa01-gpio15.yaml\n')
        key = base64.b64encode(secrets.token_bytes(32)).decode()
        password = secrets.token_urlsafe(24)
        secret_file = work / 'secrets.yaml'
        secret_file.touch(mode=0o600)
        original = ('wifi_ssid: "TEST_ONLY_NOT_A_REAL_NETWORK"\n'
                    f'wifi_password: "{password}"\n'
                    f'fallback_password: "{password}"\n'
                    f'api_encryption_key: "{key}"\n')
        secret_file.write_text(original)
        short_key = base64.b64encode(secrets.token_bytes(31)).decode()
        secret_file.write_text(original.replace(key, short_key))
        result = subprocess.run([sys.executable, '-m', 'esphome', 'config', str(work / 'device.yaml')],
                                capture_output=True, text=True, check=False)
        if result.returncode == 0 or '32' not in result.stdout + result.stderr:
            raise RuntimeError('Pinned firmware validator did not reject a 31-byte API/OTA key')
        print('PASS: 31-byte API/OTA key rejected', flush=True)
        secret_file.write_text(original)
        for operation in ('config', 'compile'):
            with (work / 'build.log').open('w') as log:
                result = subprocess.run([sys.executable, '-m', 'esphome', operation,
                                         str(work / 'device.yaml')], stdout=log,
                                        stderr=subprocess.STDOUT, check=False)
            if result.returncode:
                message = (work / 'build.log').read_text(errors='replace')
                message = message.replace(key, '<redacted>').replace(password, '<redacted>')
                print('\n'.join(message.replace('\r', '\n').splitlines()[-60:]))
                return result.returncode
            print(f'PASS: encrypted XS-SSA01 {operation}', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
