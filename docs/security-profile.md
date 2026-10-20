# Encrypted USB provisioning profile

The supported XS-SSA01 profile can be provisioned through a trusted local serial
connection without executing the legacy Tuya Wi-Fi conversion protocol. This is
a complete path from source to the supplied relay/button/indicator functionality,
followed by encrypted Home Assistant API and OTA updates. It applies only after
the operator has verified that the actual hardware matches this GPIO variant.

Use a qualified serial workbench with the device disconnected from mains power;
never connect a computer or serial adapter to a mains-connected plug. This guide
is not a hardware pinout or a substitute for model-specific electrical work.
If serial access is not safe or verified, do not use this profile.

On the trusted provisioning computer, create a private directory outside the
repository and install the exact compiler with a Python virtual environment:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install 'esphome==2026.9.1'
```

Copy `examples/tuya-plug.yaml` and `examples/xs-ssa01-gpio15.yaml` into that
private directory. Generate its `secrets.yaml` with
`python3 /trusted/repository/scripts/create-secrets.py secrets.yaml`, then write
`device.yaml` as follows:

```yaml
packages:
  base: !include tuya-plug.yaml
  hardware: !include xs-ssa01-gpio15.yaml
```

Run `.venv/bin/python -m esphome compile device.yaml`. Review the hardware and
image identity before using the standard ESPHome serial uploader with the
operator-selected serial port. Compilation does not flash a device. The
repository's container launcher is for LAN operation; it does not silently grant
USB device access. Retain credentials and firmware privately because the binary
contains the device key.

The supplied API and OTA configuration uses ESPHome's encrypted Noise transport
and one random 32-byte device PSK. `create-secrets.py` uses the operating system
CSPRNG and creates the file exclusively with mode 0600. ESPHome rejects a key of
any other length. Do not replace `api.encryption` or `ota.encryption` with a
password-only setup. The supplied profile implements no certificate-based TLS
transport of its own; repository download and compiler/package-manager trust
remain separate prerequisite tool responsibilities.

`python3 scripts/validate_firmware.py` in the pinned compiler environment creates
fresh disposable synthetic credentials, proves the actual compiler rejects a
31-byte key, validates the merged configuration and compiles the real firmware.
CI runs this command without flashing, network provisioning or hardware
acceptance. Build artifacts and synthetic secrets are discarded.

The same validation also compiles the standalone
[SWP1-PW2-V5 profile](../examples/swp1-pw2-v5.yaml) and rejects a short key for
that profile. Its [illustrated serial guide](swp1-pw2-v5.md) covers the distinct
TYWE3S wiring and GPIO evidence; do not substitute the XS-SSA01 pin mapping.

The alternative legacy Tuya converter requires `--allow-insecure-legacy-protocol` before it performs privilege escalation or any workbench operation. It remains explicitly insecure compatibility
code: its upstream fixed hint/MD5-derived AES key and CBC transport do not become
secure because the final ESPHome firmware uses a new key. Keep that path isolated
as described in SECURITY.md. This profile does not claim all legacy algorithms
meet modern recommendations or that compiling proves a physical device is safe.

Read the [compiler dependency assessment](compiler-dependency-assessment.md) before using the pinned build environment. Its Starlette findings are assessed for the command-line workflow only; do not expose PlatformIO Home or ESPHome dashboard from that environment.
