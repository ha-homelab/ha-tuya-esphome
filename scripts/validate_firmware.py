#!/usr/bin/env python3
"""Validate and compile USB-provisionable encrypted device profiles; never flash."""
import base64
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    profiles = (
        ('XS-SSA01', ('tuya-plug.yaml', 'xs-ssa01-gpio15.yaml'),
         'packages:\n  base: !include tuya-plug.yaml\n  hardware: !include xs-ssa01-gpio15.yaml\n'),
        ('SWP1-PW2-V5', ('swp1-pw2-v5.yaml',), None),
    )
    for label, sources, wrapper in profiles:
        result = validate_profile(root, label, sources, wrapper)
        if result:
            return result
    return 0


def validate_profile(root: Path, label: str, sources: tuple[str, ...],
                     wrapper: str | None) -> int:
    with tempfile.TemporaryDirectory(prefix='tuya-firmware-check-') as directory:
        work = Path(directory)
        for name in sources:
            shutil.copyfile(root / 'examples' / name, work / name)
        if wrapper is not None:
            (work / 'device.yaml').write_text(wrapper)
            config = work / 'device.yaml'
        else:
            config = work / sources[0]
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
        result = subprocess.run([sys.executable, '-m', 'esphome', 'config', str(config)],
                                capture_output=True, text=True, check=False)
        if result.returncode == 0 or '32' not in result.stdout + result.stderr:
            raise RuntimeError('Pinned firmware validator did not reject a 31-byte API/OTA key')
        print(f'PASS: {label} 31-byte API/OTA key rejected', flush=True)
        secret_file.write_text(original)
        for operation in ('config', 'compile'):
            with (work / 'build.log').open('w') as log:
                result = subprocess.run([sys.executable, '-m', 'esphome', operation,
                                         str(config)], stdout=log,
                                        stderr=subprocess.STDOUT, check=False)
            if result.returncode:
                message = (work / 'build.log').read_text(errors='replace')
                message = message.replace(key, '<redacted>').replace(password, '<redacted>')
                print('\n'.join(message.replace('\r', '\n').splitlines()[-60:]))
                return result.returncode
            print(f'PASS: encrypted {label} {operation}', flush=True)
        images = list((work / '.esphome' / 'build').glob('*/.pioenvs/*/firmware.bin'))
        if len(images) != 1:
            raise RuntimeError(f'{label}: expected exactly one compiled firmware image')
        image = images[0].read_bytes()
        if not 256 <= len(image) < 1024 * 1024 or image[0] != 0xE9:
            raise RuntimeError(f'{label}: unexpected ESP8266 image header or size')
        print(f'PASS: {label} ESP8266 image, {len(image)} bytes', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
