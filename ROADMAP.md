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
uninstalled candidate separate from the ten successful firmware conversions.

- [ ] Evaluate the experimental ESP8266 CloudCutter port against the AWP02L-N's
      actual stock firmware. A research implementation exists; this unit's
      compatibility and a usable conversion profile are not yet established.
      One experimental packet was sent; replacement-key authentication and
      conversion are unverified. A later authentication-only AP ran for 120
      seconds without the target joining; this did not test the replacement key.
      See [the procedure](docs/awp02l-n-psk02.md).

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

A seventh conversion, YM-WS-1, reached the ordinary loader, with its physical
identity matched to the old LocalTuya role. A GPIO-neutral installation was
followed by encrypted OTA of the GPIO15-relay/GPIO13-button/inverted-GPIO12 LED
profile. The operator confirmed button, load and indicator behavior. HA migration
and Matter readback passed. Its software restart started off and returned off;
on-to-off restoration was not exercised. This success does not
retroactively change the earlier YM-WS-1 pairing-only record.

An eighth conversion, JH-G01U, passed encrypted OTA/API verification and physical
button/load testing with GPIO4 relay and GPIO5 button. The operator observed an
inverted GPIO12 indicator; active-low polarity was installed and the API checked
again. A visual recheck of that correction and separate restart/power-cycle tests
remain unperformed. Its role migration removes obsolete controls and motion
rules from the old room and uses a switch card at the requested new position.

A ninth conversion reuses the established WP5 profile, with physical/load and
restart checks explicitly waived again. The complete profile was installed
directly after matching the loader to the intended old device; encrypted API
identity and expected entities were verified. These checks do not count as
per-unit physical acceptance. Its HA references, cached curtain power profiles
and existing Matter bridge were migrated with runtime readback; the router name
was updated while retaining the reserved address. The installed desktop client,
six persisted configurations and two server configuration Secrets were updated.
The web deployments were already not ready, so their runtime adoption remains
unverified.

A tenth conversion uses the established YM-WS-1 profile under the same standing
instruction to reuse a matching model's profile without repeated physical or
restart checks. The intended old-device identity matched the loader and final
encrypted API. Its complete image was installed directly; this is software
verification, not an additional per-unit physical acceptance result.
HA references, two away-scene targets and DNS were migrated. Client configuration
inspection found no old references to replace. Matter exposure was completed
after longer bounded API requests recovered management access; an uncertain
filter write was checked by readback instead of repeated.

An additional device already running ESPHome was updated and renamed separately;
it is not included in the ten conversions. The operator confirmed its button,
load and corrected indicator. Its HA motion rules and dashboard were migrated
while preserving manual overrides, and DNS kept the original reservation.
Both the relay and renamed firmware-update diagnostic are available after a
targeted integration reload resolved its cached old node name.
The tenth conversion and this maintenance unit have reachable relay endpoints
in the existing Matter bridge, with prior endpoints and all three fabrics kept.

- [ ] Convert sequentially and record local unit IDs/results.
- [ ] Retire incompatible/unresponsive units under the chosen policy.
- [ ] Validate each apparent model variant before reusing a GPIO profile.
- [ ] Add metering only after chip identification and independent calibration.

No dates or successful conversion counts are invented. Publish only anonymized
results and reusable configuration; maintain the per-unit operational inventory
privately.
