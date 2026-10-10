# Tasks and acceptance gates

## Workbench

- [x] Reserve wired management address/name through OpenWrt dnsmasq.
- [x] Restore the reference Wi-Fi radio and verify AP capability.
- [x] Verify moving the radio to and from an isolated network namespace.
- [x] Install Docker and basic Linux tooling.
- [x] Locate the existing NAS Matter Hub/Server without redeploying either.
- [x] Finish the container build and real binary-identity TLS test.
- [ ] Compile the GPIO-neutral ESPHome image and verify the loader size limit.
- [x] Verify an actual AP startup and save the result in the deployment record.

## First unit

- [ ] Fast-blinking pairing, successful loader connection, flash-size identification.
- [ ] Direct ESPHome flash, with stock backup download disabled by owner choice.
- [ ] Stable Wi-Fi and encrypted Home Assistant API; successful subsequent OTA.
- [ ] Confirm relay GPIO, inversion and off-at-boot behavior without a load.
- [ ] Confirm physical button and status reporting.
- [ ] Save a sanitized, verified model profile; do not generalize from appearance.

## Ecosystems

- [ ] Select only the verified relay entity in the existing Matter Hub.
- [ ] Confirm or add Google Home commissioning without resetting existing fabrics.
- [ ] Confirm or add Alexa commissioning; use the intended bridge on UDP 5540.
- [ ] Round-trip state/control checks in HA, Google, Alexa and the physical button.
- [ ] Restart checks for the plug and bridge; record results separately.

## Remaining batch

- [ ] Convert sequentially and record local unit IDs/results.
- [ ] Retire incompatible/unresponsive units under the chosen policy.
- [ ] Validate each apparent model variant before reusing a GPIO profile.
- [ ] Add metering only after chip identification and independent calibration.

No dates or successful conversion counts are invented. Publish only anonymized
results and reusable configuration; maintain the per-unit operational inventory
privately.
