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
