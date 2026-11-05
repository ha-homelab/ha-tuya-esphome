# Contributing

Use English for documentation and issues. Separate observations from assumptions,
and record the firmware/software version for compatibility claims. A GPIO profile
needs physical relay/button/boot verification on the stated hardware. Enclosure
similarity and successful compilation are insufficient.

Run shell syntax checks, ShellCheck, the publication guard, and the container PSK
test before proposing runtime changes. Firmware changes also need ESPHome config
validation and a size-checked build. Do not flash devices from CI.

```sh
bash -n bin/* scripts/setup-workbench.sh
shellcheck bin/* scripts/setup-workbench.sh
python3 scripts/check-publication.py
# Workbench setup also runs tests/test_psk.py in its compatibility container.
```

Repository policy requires pull requests, two current approvals and resolved
review threads, with no administrator/automation bypass. Do not weaken that policy
to merge a convenience change. Public issue reports must follow [SECURITY.md](SECURITY.md).

Our additions are MIT-licensed. Upstream tools retain their own licenses and are
fetched separately. Do not upload vendor firmware, credentials, device dumps, or
radio calibration archives here.

All major functionality changes must include automated regression coverage and
relevant negative cases. Use the existing public issue/PR process for proposals;
follow [governance](GOVERNANCE.md) and [Code of Conduct](CODE_OF_CONDUCT.md).
Run `python3 -m unittest discover -s tests -p 'test_stage_*.py' -v` for local
staging tests. These synthetic files are not hardware firmware.

## Verified build dependencies

Both the ESPHome compiler environment and legacy protocol image install complete
artifact hash locks. Compiler source builds are restricted to crcmod, esptool
and paho-mqtt, with a separately hashed setuptools backend. The legacy image
builds only paho-mqtt and sslpsk3 using hashed setuptools/poetry-core. Isolated
backend downloads are disabled; every other package requires a binary wheel.
Existing runtime versions and the Python 3.11 legacy protocol are unchanged.

Use uv 0.13.4 to regenerate:

```sh
uv pip compile requirements-firmware.txt --python-version=3.12 --universal --generate-hashes --output-file=requirements-firmware.lock
uv pip compile .github/requirements-wheels-only.in requirements-build.in --python-version=3.12 --universal --generate-hashes --output-file=requirements-build.lock
uv pip compile container/requirements-runtime.in --python-version=3.11 --universal --generate-hashes --output-file=container/requirements-runtime.lock
uv pip compile .github/requirements-wheels-only.in requirements-build.in --python-version=3.12 --universal --generate-hashes --output-file=requirements-build.lock
```

The Docker build requires BuildKit named-context support. CI and
`scripts/setup-workbench.sh` pass `--build-context workbench-locks=.../container`
so the dependency locks are independent of the unchanged pinned upstream source
checkout. The existing isolated real TLS protocol test and encrypted firmware
build must pass after updates; no connected devices are involved in those checks.
