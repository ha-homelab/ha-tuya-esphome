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
uninstalled candidate separate from the twenty-two successful Tuya firmware conversions.

- [ ] Evaluate the experimental ESP8266 CloudCutter port against the AWP02L-N's
      actual stock firmware. A research implementation exists; this unit's
      compatibility and a usable conversion profile are not yet established.
      One experimental packet was sent; replacement-key authentication and
      conversion are unverified. A later authentication-only AP ran for 120
      seconds without the target joining; this did not test the replacement key.
      See [the procedure](docs/awp02l-n-psk02.md).

A second AWP02L-N reached the same ordinary PSK `02` failure. Its separate
single-packet AP trial stopped when the target disappeared before Wi-Fi
provisioning. Recover and re-identify that AP before continuing; preserve the
attempt marker and keep its existing HA/client references until a working
replacement is verified. It does not increase the conversion count.

A third AWP02L-N failed thirteen ordinary PSK `02` handshakes, without reaching
the loader or receiving firmware. The isolated session was stopped and its
radio returned to the host. No experimental payload was sent: the ESP8266
branch still uses an unmatched stock-firmware layout. A serial readout would
first require inspection of the unplugged board and identification of its
module, UART pads and boot strap. Its existing HA/client references remain.

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
it is not included in the conversion count. The operator confirmed its button,
load and corrected indicator. Its HA motion rules and dashboard were migrated
while preserving manual overrides, and DNS kept the original reservation.
Both the relay and renamed firmware-update diagnostic are available after a
targeted integration reload resolved its cached old node name.
The tenth conversion and this maintenance unit have reachable relay endpoints
in the existing Matter bridge, with prior endpoints and all three fabrics kept.

An eleventh conversion reuses the corrected JH-G01U profile with repeated
physical and restart checks waived. Historical role, DHCP and loader identity
matched before writing; encrypted API verification passed after the complete
image installed. HA adoption, its separate dashboard control, restored motion-on
action and DNS are ready. The operator selected the current lamp trigger for a
separate evening-off rule, which is installed and verified with six isolated HA
runtime tests. Unrelated curtain controls and manual overrides remain unchanged.
Its relay is exposed through the existing Matter bridge, which now reports 19
devices with prior endpoints and fabrics preserved.

A twelfth conversion reused the established YM-WS-1 profile. Its initial final-image
request stalled without a recorded image download. A fresh read confirmed that
the same device still ran the intermediate loader; one bounded retry installed
the complete profile with its new role name. The final encrypted API, identity
and compilation time were verified. Repeated physical and restart tests were
initially waived under the standing same-model policy. A later input probe and
load test corrected this unit to GPIO1 button, GPIO14 relay and active-high
GPIO13 indicator; the owner confirmed both button cycles and matching lamp/LED
operation. HA references and DNS use the new role; the exact old LocalTuya
device was removed, with automation logic and
manual overrides preserved. No corresponding client references were found.

A separate TECKIN SP20 moved from Tasmota to ESPHome through its existing web
updater, without using the conversion AP. The live template selected BL0937
metering; its actual calibration and energy counters were transferred, with all
ten meter fields verified through the encrypted API. This is a maintenance
migration, not an additional Tuya conversion or physical load test. The HA
handover preserved its relay and ten meter entity IDs, eight statistic metadata
records, inspected history, solar rules, dashboard and manual overrides. The
exact old Tasmota device was retired through its supported removal hook.

Both new relays have exact filters saved in the existing Matter bridge. HA
registry request timeouts initially delayed discovery; later readback confirmed
21 devices with both new relay endpoints reachable. All prior endpoint
identities and three fabrics were preserved without a service restart.

A thirteenth conversion reused the established KMC 30137 profile. Its 440,480-byte
ESPHome 2026.9.1 image installed in one final upload lasting 18,894 ms. The loader
identity, one-megabyte flash layout and final encrypted API identity/version/build
time were verified. Physical and restart checks were waived for the reused model
profile. The router retained the reserved address and adopted the new role name;
forward and reverse DNS passed, and the conversion AP was cleaned up.
HA retired the exact old LocalTuya device, migrated two solar rules and the
existing dashboard row, and verified no remaining old references. The operator
kept solar semantics but removed the plug from unrelated media shortcuts.
The new relay is reachable in the existing Matter bridge, now reporting 22
devices, with prior endpoint identities and all three fabrics preserved.

- [x] Complete [TanTan WP3 identification and switch migration](docs/wp3-migration.md).
      The matched loader reports 1 MiB flash, and the input-only image is
      installed with encrypted API identity/build verification. A controlled
      press identified GPIO13 as the button. The final GPIO15-relay/GPIO2-indicator
      profile passed encrypted OTA and API verification. The operator confirmed
      relay clicks, actual load switching and the visible indicator in both
      directions. After an automation reload replaced the stale light target,
      a natural motion event switched the new relay on with matching event
      contexts; the operator confirmed it worked. The final HA audit found no
      retired-entity references in 2,456 active files, with unrelated source and
      LocalTuya devices unchanged. Source was saved in both active ESPHome
      locations, and HA required no restart. All six persisted client files and
      the running native client's canonical switch were verified after migration.
      API on/off control and reported OFF after software restart from ON passed;
      physical contact state during boot and boot transients were not measured.
      Two later physical button presses produced reported relay states OFF, ON,
      OFF, matching that load/indicator confirmation; the conversion AP and
      dedicated workbench session are closed.
      HA found the relay available and OFF after the operator relocated and
      reconnected it. A controlled ON-to-OFF mains-cycle test and boot-transient
      measurements remain open.
- [x] Complete the latest WP5 handover. This fifteenth
      firmware conversion uses GPIO15 relay, GPIO13 button and an internal
      inverted GPIO2 indicator, without a separate GPIO0 red-light entity.
      Its encrypted final upload, identity/build readback, API on/off control
      and software restart from ON to reported OFF passed. The operator
      confirmed the relay, connected lamp and indicator with two button
      presses, matching captured OFF, ON, OFF states. All six persisted client
      configurations and the native switch display were verified, preserving
      the prior control's placement and icon. HA reload, direct service-control
      and exact old-device retirement passed; 2,457 active files had no retired
      references. Unrelated sources, devices, the prior WP3 and manual overrides
      were unchanged. Source was saved in both active ESPHome locations without
      an HA restart. The unchanged sun-elevation condition blocked a natural motion
      acceptance test; it was not bypassed.
      HA found the switch available and OFF after the operator returned it to
      the installed position. A controlled mains-cycle test and boot-transient
      measurement were not performed.
- [ ] Convert sequentially and record local unit IDs/results.
- [ ] Retire incompatible/unresponsive units under the chosen policy.
- [ ] Validate each apparent model variant before reusing a GPIO profile.
- [ ] Add metering only after chip identification and independent calibration.

No dates or successful conversion counts are invented. Publish only anonymized
results and reusable configuration; maintain the per-unit operational inventory
privately.

## GREFIC CZ-U201: sixteenth firmware conversion

- [x] Ordinary Tuya-Convert handshake, live ESP8266/1 MiB identification.
- [x] Retain a private flash image and recover the two-channel hardware JSON.
- [x] Install a GPIO-neutral image, then encrypted OTA of the two-relay image.
- [x] Verify independent native API states for both channels.
- [x] Confirm GPIO14/channel 2 controls the left outlet with an actual lamp.
- [x] Confirm the right outlet and shared button with an actual lamp.
- [x] Confirm both outputs return OFF after a controlled mains cycle.
- [x] Add and verify the two HA switch entities.

See [the unit's evidence and acceptance record](docs/grefic-cz-u201.md).

## KMC 30608: seventeenth firmware conversion

- [x] Match the three LocalTuya channels to one physical device.
- [x] Complete ordinary Tuya-Convert with stock firmware 1.0.5.
- [x] Verify ESP8266/1 MiB and retain a private post-loader flash image.
- [x] Install a GPIO-neutral image and verify the GPIO16 button with an input probe.
- [x] Install three-relay ESPHome firmware and check independent native states.
- [x] Confirm all three numbered outlets with a lamp and test the common button.
- [x] Confirm all outputs return OFF after software restart and mains cycling.
- [x] Preserve the three existing HA entity IDs while replacing LocalTuya with ESPHome.
- [x] Enable all four native HLW8012 measurements and verify HA adoption and load response.
- [x] Apply individual single-point voltage corrections to all three KMC samples using the owner's Victron reference.
- [ ] Calibrate current, power and energy independently, and verify voltage accuracy across the range.
- [ ] Verify metering coverage of outlets 1, 2 and the always-on outlet.
- [ ] Independently confirm the GPIO1 indicator's visual behavior.

See [the conversion and acceptance record](docs/kmc-30608.md).

## Second KMC 30608: eighteenth firmware conversion

- [x] Convert stock firmware 1.0.5 and retain a private post-loader image.
- [x] Confirm each numbered outlet using a fan and test the common button.
- [x] Verify that GPIO1 lights only the common indicator; stock per-outlet LED fields are disabled.
- [x] Recover the stock datapoint-to-GPIO order for the HA handover.
- [x] Complete the controlled mains-cycle check and migrate the existing HA IDs.
- [x] Correct the first KMC's role mapping while the owner confirms its normal loads remain disconnected.
- [ ] Explain the second sample's separate outlet indicators; further diagnosis deferred by the owner. The first sample's outlet 3 indicator works with the same profile.

## Supernight CV01: nineteenth firmware conversion

- [x] Convert stock firmware 1.0.4 and retain a private post-loader image.
- [x] Probe both buttons; use the measured high-on-press ADC polarity.
- [x] Verify both outlets, independent buttons, software restart and mains cycling.
- [x] Adopt two HA switches and four uncalibrated measurement sensors.
- [x] Persist and verify source/private credentials in HA and ESPHome Dashboard.
- [ ] Calibrate metering and verify left-outlet measurement coverage.
- [ ] Physically verify indicator and photosensor night-light behavior.

See [the Supernight evidence](docs/supernight-cv01.md).

## Third KMC 30608: twentieth firmware conversion

- [x] Convert the isolated stock 1.0.6 device and retain a private post-loader flash read.
- [x] Verify 1 MiB DOUT at 40 MHz and use a matching image header.
- [x] Confirm a physical GPIO16 button press and release with an input-only probe.
- [x] Match the stock three-channel initializer to the second sample.
- [x] Install the three-relay/metering image and verify independent native controls.
- [x] Verify software restart from all ON returns all OFF.
- [x] Confirm physical outlet 1 powers the test load.
- [ ] Verify physical outlets 2 and 3, common-button load control and a mains cycle; deferred by the owner.
- [x] Verify HA adoption and source persistence.
- [ ] Exercise HA service relay transitions; deferred by the owner.
- [ ] Calibrate measurements and determine per-outlet/always-on metering coverage.

## Second WP3: twenty-first firmware conversion

- [x] Match the former LocalTuya plug to the intermediate loader and retain a private post-loader backup.
- [x] Identify GPIO13 with a short physical press using an input-only GPIO4/GPIO13 probe.
- [x] Install the GPIO15 relay and inverted GPIO2 indicator profile through encrypted OTA.
- [x] Verify native relay control and software restart from ON to OFF.
- [x] Obtain owner confirmation of button, lamp and indicator operation.
- [x] Adopt ESPHome under the existing numbered switch ID and persist its source and credentials.
- [ ] Verify controlled mains-cycle behavior and boot transients separately.

## Reused YM-WS-1 profile: corrected follow-up

- [x] Confirm encrypted API communication and record the owner's dim-indicator/no-click report.
- [x] Observe no physical-button transition during the requested short press.
- [x] Compile an input-only GPIO1/GPIO13 probe; install it after the owner confirms the output is unloaded.
- [x] Identify GPIO1 with a complete physical press/release and restore switching with GPIO14.
- [x] Correct GPIO13 LED polarity to active-high and confirm that lamp and indicator follow both button cycles.
- [x] Preserve the original six component/entity identities, verify that no temporary probe entities remain and persist the corrected source.
- [ ] Separately verify controlled mains-cycle behavior and boot transients.

The original GPIO assignment was wrong for this unit. The corrected profile
now has physical button/load/indicator acceptance and a firmware-restart OFF
check. This recovery does not add another conversion to the device count.

## Deployed configuration completeness

- [x] Audit both active source directories against HA and the private unit inventory.
- [x] Restore eleven missing per-unit YAMLs and their existing credentials from the private workbench.
- [x] Validate the prepared configurations and verify identical source readback in both locations.
- [x] Preserve existing source files, secret values and installed firmware.
- [x] Align the deployed Dashboard to ESPHome 2026.9.1 and compile limits to two CPUs; all twenty-five plug configurations pass live validation.

At the earlier source audit, all twenty-one converted plugs had individual
deployed source files.
See the [source audit](docs/deployment-record.md#deployed-source-audit-and-restoration)
for scope and the distinction between saved source and physical acceptance.

### 2026-10-11 — Ping outlet additions

- [x] Convert a fourth AWP02L-N with ordinary Tuya-Convert; verify GPIO13 button,
      GPIO15 relay, inverted GPIO2 LED, actual load and restart-to-OFF. This is
      Tuya conversion 22 and physical button/load acceptance 16.
- [x] Migrate one existing Tasmota 6.7.1 MJ_XS-SSA01 to ESPHome 2026.9.1;
      verify GPIO13/GPIO15/inverted GPIO12, actual load and restart-to-OFF.
      This is a separate Tasmota migration, not a Tuya conversion.
- [x] Save both device sources in HA and the ESPHome Dashboard, retire exact old
      integration records and add the two new controls after Switch07.
- [ ] Controlled ON-to-OFF mains-cycle checks for these two additions.

- [ ] Identify the board or original application of the square outlet reserved
      as Switch08 (deferred by the owner). Ordinary pairing failed; its setup AP is identified, but no
      firmware update route is established and no image has been installed.
