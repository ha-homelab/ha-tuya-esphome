# Tasks and acceptance gates

## Workbench

- [x] Reserve wired management address/name through OpenWrt dnsmasq.
- [x] Restore the reference Wi-Fi radio and verify AP capability.
- [x] Verify moving the radio to and from an isolated network namespace.
- [x] Install Docker and basic Linux tooling.
- [x] Locate the existing NAS Matter Hub/Server without redeploying either.
- [x] Finish the container build and real binary-identity TLS test.
- [x] Compile the GPIO-neutral ESPHome image and verify the loader size limit.
- [x] Verify an actual AP startup and save the result in the deployment record.

## First unit

The first unit is marked XS-SSA01. GPIO12 proved to be the indicator; the matching
GPIO15-relay/GPIO13-button profile now switches a known-working load in both
directions, confirmed by the operator. Each remaining unit still needs its own
hardware check.

- [x] First unit: fast-blinking pairing, successful loader connection, flash-size identification.
- [x] Direct ESPHome flash, with stock backup download disabled by owner choice.
- [x] Stable Wi-Fi and encrypted Home Assistant API; successful subsequent OTA.
- [x] Confirm relay GPIO, inversion, HA control and off state after software restart.
- [ ] Confirm off state after physically removing and restoring power.
- [x] Confirm physical button and actual load switching.
- [x] Save a sanitized, verified model profile; do not generalize from appearance.

## Ecosystems

- [x] Select only the verified relay entity in the existing Matter Hub.
- [x] Confirm Google Home discovers the new plug through the existing fabric and switches its load.
- [x] Confirm or add Alexa commissioning; use the intended bridge on UDP 5540.
- [x] Confirm Alexa discovers all selected devices, including both converted plugs.
- [ ] Confirm actual load control from Alexa on both plugs.
- [ ] Round-trip state/control checks in HA, Google, Alexa and the physical button.
- [ ] Restart checks for the plug and bridge; record results separately.

## Remaining batch

The second unit, marked YM-WS-1, is blocked at pairing before any flash write.
Rapid-blink mode could not be established; its GPIO variant is unverified.
A replacement WP5 has booted ESPHome with encrypted API access. Diagnostics
confirmed its GPIO13 button. The matching GPIO15-relay profile is installed,
physical button/load and HA software-restart checks passed, and its relay is
exported through the existing Matter Hub. Google Home discovery and actual load
control passed for this second plug as well. Alexa commissioning/discovery passed;
Alexa load control and complete state round-trip checks remain pending.

- [ ] Convert sequentially and record local unit IDs/results.
- [ ] Retire incompatible/unresponsive units under the chosen policy.
- [ ] Validate each apparent model variant before reusing a GPIO profile.
- [ ] Add metering only after chip identification and independent calibration.

No dates or successful conversion counts are invented. Publish only anonymized
results and reusable configuration; maintain the per-unit operational inventory
privately.
