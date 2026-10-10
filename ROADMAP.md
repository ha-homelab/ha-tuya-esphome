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
- [x] Confirm Alexa discovers all selected devices, including the first two converted plugs.
- [x] Confirm actual load control from Alexa on both plugs.
- [ ] Round-trip state/control checks in HA, Google, Alexa and the physical button.
- [ ] Restart checks for the plug and bridge; record results separately.

## Remaining batch

An AWP02L-N later joined the conversion AP but was blocked by patched Tuya PSK
identity version `02`. No loader or firmware write occurred. Its migration was
deferred, existing HA/client bindings retained, and the AP cleaned up. Keep its
uninstalled candidate separate from the six successful conversions.

- [ ] Evaluate the experimental ESP8266 CloudCutter port against the AWP02L-N's
      actual stock firmware. A research implementation exists; this unit's
      compatibility and a usable conversion profile are not yet established.
      One experimental packet was sent; replacement-key authentication and
      conversion are unverified. See [the procedure](docs/awp02l-n-psk02.md).

The second unit, marked YM-WS-1, is blocked at pairing before any flash write.
Rapid-blink mode could not be established; its GPIO variant is unverified.
A replacement WP5 has booted ESPHome with encrypted API access. Diagnostics
confirmed its GPIO13 button. The matching GPIO15-relay profile is installed,
physical button/load and HA software-restart checks passed, and its relay is
exported through the existing Matter Hub. Google Home discovery and actual load
control passed for this second plug as well. Alexa commissioning, discovery and
actual load control also passed on the first two plugs. A third successful
conversion, another WP5, passed its own GPIO13 input probe, physical button/load
and red-indicator checks, encrypted OTA, and HA software-restart checks. Its
verified relay is now exported through the existing three-fabric Matter bridge.
The operator deferred post-migration Google Home/Alexa acceptance.
Complete state round-trip checks remain pending.

A fourth successful conversion, a second XS-SSA01, passed its own input probe,
encrypted OTA, physical button/load test and HA software-restart check. Its
GPIO15 relay, GPIO13 button and inverted GPIO12 indicator match the first verified
XS-SSA01 profile. The count of four excludes the unflashed YM-WS-1 pairing attempt.
The fourth plug's verified relay replaced three legacy LocalTuya
devices under one stable role, with curtain automations and persisted desktop
bindings migrated, and was added to the existing Matter bridge.

A fifth conversion, KMC 30137, passed a GPIO1 input probe and physical button,
lamp and indicator checks with its GPIO14-relay/GPIO13-indicator profile. HA
command dispatch initially failed despite working native API control; recreating
only the new ESPHome entry restored it, and the HA software-restart check passed.

A sixth conversion uses the existing WP5 profile. The operator explicitly waived
repeat physical/button/indicator and restart testing for this same-model unit.
Its firmware transfer and encrypted API were verified; those results are not
recorded as physical acceptance.

- [ ] Convert sequentially and record local unit IDs/results.
- [ ] Retire incompatible/unresponsive units under the chosen policy.
- [ ] Validate each apparent model variant before reusing a GPIO profile.
- [ ] Add metering only after chip identification and independent calibration.

No dates or successful conversion counts are invented. Publish only anonymized
results and reusable configuration; maintain the per-unit operational inventory
privately.
