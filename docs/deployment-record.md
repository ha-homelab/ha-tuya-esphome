# Anonymized deployment record

Date: 2026-10-10. This record distinguishes observed facts from pending physical
tests. Private addresses, names, identifiers and credentials are intentionally
omitted; keep an exact operational record outside Git.

## Observed

- The dedicated x86-64 Debian 12 host is reachable through wired Ethernet.
- An OpenWrt dnsmasq reservation and local DNS name were added after checking
  existing reservations/leases. DNS lookup and a fresh SSH connection succeeded.
- The Linux DHCP stanza was completed so the reservation remains authoritative
  after restart; the host was not rebooted for this work.
- A board-specific NVRAM file restored the reference Broadcom radio. AP support
  is advertised, and transfer into/out of a temporary network namespace worked.
- Package installation required removing a stale APT proxy configuration.
- The existing NAS-backed k3s deployment has one running Matter Hub and one
  running Matter Server in `ha-infra`. Hub uses `net1`; its health endpoint returned
  HTTP 200. The obsolete alternative deployment was not enabled.
- The active Hub reports version 2.0.56, a running bridge on port 5540, and
  existing commissioned fabrics. The connected Home Assistant API reports
  version 2026.10.0. Household filters and commissioning data are not published.
- Wi-Fi credentials were imported privately from the existing ESPHome setup;
  new initial API/OTA/fallback credentials were generated on the workbench.
- The compatibility container built successfully. A real TLS 1.2 handshake with
  a non-UTF-8 PSK identity passed using the pinned Python and sslpsk3 versions.
- The reference radio reached `AP-ENABLED` in the isolated container. DHCP, DNS,
  HTTP, MQTT, TLS-PSK and Tuya discovery listeners started while wired SSH stayed
  reachable. The launcher reached its pre-pairing prompt without starting a flash.
- The first physical unit subsequently reached VTRUST-FLASH 1.5. The loader
  reported 1,024 KiB flash and DOUT at 40 MHz. The stock backup download was
  skipped. Exact chip identifiers, MAC address and raw output remain private.
- A native Apple Silicon Mac build used ESPHome 2026.9.1, Python 3.12 and eight
  compile workers. Actual compilation took 28.17 seconds after toolchain downloads.
  The GPIO-neutral image was 420,800 bytes; inspection confirmed an ESP8266 image,
  valid checksum, 1 MB flash, DOUT and 40 MHz.
- The loader confirmed successful ESPHome installation in about 14.6 seconds.
  The unit joined the home LAN, answered its encrypted native API, and was added
  to Home Assistant. It initially exposed only status, Wi-Fi signal and version.
- A subsequent candidate-relay image compiled on the Mac in 25.73 seconds and
  uploaded successfully through encrypted ESPHome OTA in about 27.5 seconds.
  The API and Home Assistant report the relay entity, with state changes observed
  over the API. Physical switching is a separate acceptance gate.
- A GPIO13 button candidate was installed by another successful encrypted OTA
  update. Home Assistant history records press/release events and corresponding
  software switch changes. The earlier report of relay clicks was superseded:
  the operator observed only LED changes, no mechanical clicks and no switched
  power to a load that works directly from the wall. GPIO12 was therefore rejected
  as the relay output. Matter export was held until a correct mapping and physical
  output test were established.
- The operator then identified the enclosure marking as XS-SSA01. The official
  Tasmota catalog includes a variant with GPIO13 button, GPIO12 inverted LED and
  GPIO15 relay, matching the observed input and LED behavior. A corresponding
  ESPHome profile compiled on the Mac in 24.54 seconds and was installed through
  encrypted OTA. The operator then confirmed mechanical clicks and actual load
  switching in both directions using the physical button. This verifies the
  GPIO15 relay and GPIO13 button for this unit, not every XS-SSA01 variant.
- Home Assistant successfully commanded the verified relay on, restarted the
  ESPHome device, and observed a fresh off state afterward. A separate physical
  power-cycle test remains pending.
- Added exactly the verified relay entity to the existing Matter Hub. The include
  filter count and device count each increased from seven to eight. Both existing
  fabrics, prior filters, exclusions, bridge name, port and running state were
  preserved. No factory reset or new bridge was used. The endpoint tree identifies
  the new device as an OnOffPlugInUnit.
- The operator confirmed that Google Home discovered the plug and switched its
  connected load from the app through the existing Google fabric.
- Removing the first conversion container left the Broadcom radio inaccessible.
  Reloading its driver restored it. An explicit numeric-PHY return before
  container removal then passed a live namespace round-trip check; the launcher
  now performs that return during cleanup.

## Second unit: pairing blocked before flashing

The next unit is marked YM-WS-1. An isolated conversion AP was started and the
phone connected, but the plug did not associate during the initial pairing
attempt. The operator then reported being unable to obtain rapid blinking.
The indicator remained steadily lit after a long button press. The unit never
reached the intermediate loader and no replacement firmware was written. The session was stopped cleanly and the radio returned to host managed
mode. Model-specific diagnosis remains open; do not classify this as a bricked
unit or assume the first plug's GPIO map applies.

## Replacement unit: second successful ESPHome installation

After setting aside the YM-WS-1, a different plug reached the intermediate loader.
The loader confirmed 1 MB flash, DOUT and 40 MHz. Its identity was checked against
the first plug to prevent targeting the wrong unit. The same validated 420,800-byte
GPIO-neutral image installed in about 12.3 seconds, without a stock backup.
The replacement joined the home LAN and answered the encrypted ESPHome 2026.9.1
API. It was also adopted in Home Assistant after checking its encrypted API
identity. The AP was stopped and the radio returned to the host normally.

The operator identified the replacement as WP5. Input-only diagnostics recorded
repeated GPIO13 button presses; the alternative GPIO4 input stayed inactive.
The operator also observed that the outlet supplied power during diagnostics:
unassigned GPIOs do not guarantee an off output. A matching candidate with a
GPIO15 relay, GPIO13 button and inverted GPIO2 indicator compiled on the Mac in
28.97 seconds and was installed through encrypted OTA. Home Assistant reports
the new firmware and an off switch state. The operator subsequently confirmed
actual load switching in both directions using the physical button. This
verifies the GPIO15 relay and GPIO13 button for the observed unit. Home Assistant
also turned the relay on, restarted the device, and observed a fresh off state.
Only its verified relay was then added to the existing Matter Hub with an exact
entity filter. Filter/device counts increased from eight to nine, both existing
fabrics and all prior filters were preserved, and the endpoint reports
OnOffPlugInUnit. The operator confirmed that Google Home discovered this second
plug and controlled its connected load. The failed pairing attempt and this replacement retain separate
private inventory records.

At the operator's request, the catalog's second inverted LED channel, GPIO0, was
added as a separate Red Indicator light. That update compiled in 16.55 seconds
and passed encrypted OTA. ESPHome and HA acknowledge its on state, and the
operator confirmed the red color with the relay off. The indicator is not
included in the Matter filter. A software-restart check of this final firmware
confirmed that both the relay and the previously lit red indicator return off.

## Alexa commissioning, discovery and load control

An additional-controller commissioning window was opened on the existing bridge.
The operator scanned its private code in Alexa. The bridge accepted the Amazon
fabric and reported a successful `commissioningComplete` response. Both earlier
fabrics remained present, increasing the total from two to three. The operator
then confirmed that Alexa discovered all nine selected devices, including both
converted plugs. In a separate physical check, the operator confirmed that Alexa
switches the connected load on and off on both converted plugs.

## Third successful ESPHome installation: another WP5

The operator identified the next plug as the same WP5 model. A new input-only
GPIO13/GPIO4 probe compiled on the Mac in 25.59 seconds. The 424,448-byte image
passed the first-image size limit, ESP8266 checksum and 1 MB DOUT/40 MHz checks.
The loader identity differed from both working plugs and independently reported
1 MB DOUT/40 MHz. The probe installed in 13.95 seconds without a stock backup.
The new plug joined the home LAN and answered its encrypted API with both probe
inputs and no relay output. The conversion AP was stopped and its radio returned
to the Linux host.

Four GPIO13 button press/release cycles were observed while GPIO4 stayed inactive.
The previously verified WP5 final image was then reused via an explicit OTA file
path after checking its digest, credentials and target identity. This matters
because configurations sharing the same ESPHome node name also share a build
directory: the latest build there was the probe, not the final profile. Encrypted
OTA completed in 22.19 seconds. The operator confirmed actual load switching in
both directions, mechanical relay clicks and the independent red indicator.
The unit was adopted in Home Assistant. HA turned the relay on and restarted
the plug; fresh states confirmed both the relay and the previously lit red
indicator were off. The verified relay was then added to the existing Matter
bridge as an OnOffPlugInUnit. The bridge reports ten selected devices and filters,
with all three controller fabrics preserved. The operator deferred
post-migration Google Home/Alexa tests; no new physical controller result is
claimed for this third plug.

## Reusing existing household roles

The two WP5 units replaced existing HA roles. One old Tuya device was removed
from its integration after matching its identity; the other was retained under
an explicit `_old` name at the operator's request. The retained entity kept its
original `light` domain, while its replacement relay uses `switch`.

Active references in automations, scenes, dashboards, floorplans and configuration
were migrated. The light-to-switch replacement also changed explicit service
calls. A startup-only binding in a floorplan integration required an HA restart;
HA completed startup with the new binding. The floorplan UI test confirmed the
replacement control dispatches the switch service. Unrelated devices and
conditions were preserved.

The already exported WP5 retained its Matter endpoint during renaming, while the
third plug received a new endpoint. The bridge reports ten devices and three
fabrics. Six saved client/deployment configurations were checked, including the
installed desktop client's encrypted settings and the Python/Go dashboard inputs.
Native desktop controls showed both new entities, and settings survived normal
save and two client restarts. Credentials and private configurations were not
published. Post-migration Google Home/Alexa load tests were deferred by the
operator.

## Fourth successful ESPHome installation: another XS-SSA01

A second XS-SSA01 reached the intermediate loader, which reported 1 MB flash,
DOUT and 40 MHz. Its identity was checked against all three working plugs. The
validated 424,448-byte input-only probe installed in 11.637 seconds without a
stock backup. The plug joined the home LAN and answered the encrypted ESPHome
API; the conversion session was stopped and the radio restored to managed mode.

Three GPIO13 press/release cycles were recorded while GPIO4 remained inactive.
The matching XS-SSA01 profile uses GPIO15 for the relay, GPIO13 for the button
and inverted GPIO12 for its internal indicator. Its final 440,480-byte image
passed checksum and flash-header checks and was uploaded through encrypted OTA
using an explicit file path and digest check. The native API reported the
expected final configuration hash. Two further button presses changed the relay
state, and the operator confirmed mechanical clicks and actual load switching
in both directions. This is per-unit verification, not a guarantee about every
plug with the same marking.

Home Assistant adopted the final firmware, commanded its relay on, restarted the
device and observed a fresh off state afterward. The relay was left off.

At the operator's request, this plug replaces three numbered legacy LocalTuya
devices with one stable household role. All three old devices were removed after
identity checks. Morning/evening curtain references were updated while retaining
their schedules, delays and conditions. An obsolete action in a separate motion
automation was removed instead of retargeting it to the new curtain power outlet.
The replacement relay was added to the existing Matter bridge as one
OnOffPlugInUnit; all prior endpoints and three controller fabrics were preserved.

The installed desktop client picked up the canonical entity and its off state
without another client restart. Exactly one unnumbered control remained, and all
six saved client/deployment configuration sources were checked for stale bindings.
No curtain or load was activated during migration verification.
HA completed a restart and loaded both updated startup-only curtain profiles;
the replacement relay remained off.

## Fifth successful ESPHome installation: KMC 30137

The next unit was identified by the operator as KMC 30137. The first pairing
attempt timed out without a plug association or loader connection; no firmware
had been written at that point. The operator initially reported no visible LED
response, then obtained rapid blinking. A second attempt reached the loader,
which confirmed a distinct device with 1 MB flash and DOUT at 40 MHz.

A separate GPIO1-only input probe was used because the documented KMC mapping
differs from the earlier plugs. The 424,224-byte probe installed in 16.216 seconds
without a stock backup. Its encrypted API and identity were checked, then the
conversion AP was stopped and the radio restored to managed mode. Three controlled
GPIO1 press/release cycles were observed. A 440,480-byte final candidate with
GPIO14 relay, GPIO1 button and inverted GPIO13 indicator was installed through
encrypted OTA. The final encrypted API became available after startup and
reported the expected entities. Home Assistant adopted the final firmware and
reported the relay off. The operator then confirmed mechanical clicks, actual
lamp switching in both directions and the indicator changing with the relay.

The first HA entry accepted switch commands without changing the output, despite
working direct native API commands. Its address, identity and relay key matched.
Reloading the entry did not resolve it; removing and re-adding only this new
ESPHome entry restored control. An HA-commanded on/off sequence was observed
through a separate native API connection, and the final HA software-restart
check returned the relay to a fresh off state. The exact cause of the first
entry's command failure was not established.

## Sixth successful ESPHome installation: WP5 with profile reuse

For the next WP5, the operator explicitly requested the existing working profile
without repeated button, load, indicator or restart tests. The loader's identity
was checked against all earlier converted units. It reported 1 MB flash and QIO
at 40 MHz; the replacement image uses the established DOUT/1 MB/40 MHz layout.
The staged input-only image was replaced before any ESPHome flash started, so
the 440,688-byte final WP5 image was installed directly in 17.171 seconds.

The encrypted native API confirmed the new device and the final relay, separate
red indicator and diagnostic entities. Passive state observation found both
relay and red indicator off. No commands were sent to toggle outputs or restart
this unit. The conversion AP was stopped and the radio returned to managed mode.
Its private record explicitly distinguishes inherited profile evidence from
waived per-unit physical acceptance. No separate OTA update was needed.

An earlier converted WP5 also had a stale LocalTuya entry under a former heater
role. Matching the physical device identity established that it was the same
plug. The stale entry, its dashboard control and four obsolete heater automations
were removed. Shared energy-management rules retained their other participants.
The active replacement and the separately retained old-role device were preserved;
183 active configuration files were checked for the retired references.

The KMC and latest WP5 then replaced existing HA roles under stable, unnumbered
entity IDs. Their old LocalTuya entries were removed, active automation and
dashboard/floorplan references updated, and only the relay entities were added
to the existing Matter bridge. Prior endpoints and all three controller fabrics
were preserved. Both replacements were saved across all six desktop/deployment
configuration sources, and the installed client showed both canonical controls
available and off. No repeated physical test was performed on the latest WP5.

## Later AWP02L-N attempt: patched stock firmware

An AWP02L-N previously managed through LocalTuya joined the conversion AP.
Ten observed TLS attempts presented PSK identity version `02` and failed with
`DECRYPTION_FAILED_OR_BAD_RECORD_MAC`, consistent with the unsupported patched
firmware described by Tuya-Convert. The intermediate loader was never reached.
The attempt was stopped; no stock backup or replacement firmware was written.
The conversion container was removed and the Wi-Fi radio restored to managed
mode.

A private 428,224-byte ESPHome candidate was compiled for the planned replacement
role but was not installed. Published AWP02L-N variants agree on GPIO15 for the
relay and GPIO13 for the button but differ in their indicator wiring. This unit
therefore provides no physical pinout validation or new reusable verified profile.
The existing LocalTuya entity and automation references were retained. The six
desktop/deployment configuration sources remained unchanged; the proposed new
role was recorded only in the private migration plan. The converted total stays
at six.

An explicitly accepted follow-up used the experimental ESP8266 CloudCutter
revision `defb7ba92a228dc8149599a54aadcd37e0e862c6`. The dedicated radio joined
the unit's slow-blinking AP inside an isolated namespace. Its BSSID and gateway
neighbor were checked against the private target identity. One 256-byte
experimental UDP packet was sent; no firmware image was sent. The station
connection subsequently dropped and a rescan found no matching AP. This is a
reaction, not proof of key replacement. The investigation was set aside for the
next plug before replacement-key authentication or firmware-format validation.
No HA, client or Matter migration was performed. See the
[experimental procedure](awp02l-n-psk02.md); it is not a verified conversion recipe.

A later authentication-only checkpoint sent normal Wi-Fi provisioning once to
the identified unit. The first AP setup failed because process supervision
treated dnsmasq's daemonizing parent exit as a failure. A resumed checkpoint used
foreground dnsmasq, reached AP/listener readiness, and observed no target
association, DHCP lease or application request over 120 seconds. Neither the
exploit nor provisioning was repeated for that resume. Key authentication
remains unverified; no firmware was served and the old role was not migrated.

## Later YM-WS-1: seventh ESPHome installation

A YM-WS-1 selected from an existing LocalTuya role reached VTRUST-FLASH 1.5 using
the ordinary conversion path. The loader MAC matched the intended old device
and differed from all previously converted units. It reported 1,024 KiB flash,
DOUT at 40 MHz and active user1. This success is recorded separately from the
earlier YM-WS-1 attempt that never reached the loader.

The 420,800-byte GPIO-neutral image installed in 26,208 ms, with the factory
backup step disabled. After encrypted API identity verification, a 440,480-byte
YM-WS-1 candidate was installed through encrypted OTA. It uses GPIO15 relay,
GPIO13 active-low button with pull-up/debounce and an inverted GPIO12 internal
indicator. The operator confirmed actual load switching in both directions
using the button, with the indicator following. The encrypted API reported the
final firmware and expected entities, and HA accepted a new ESPHome entry.
HA control and production role migration were subsequently completed. A software
restart started with the relay already off and it returned off; this did not test
restoration from an on state. The exact old LocalTuya entry was removed, active
references migrated, and the canonical relay was verified in the existing Matter
bridge. All three fabrics and existing endpoint identities and filters remained
intact. A bridge write response timed out, but readback proved it had applied;
the mutation was not repeated. Controller-app acceptance remains deferred.

The conversion container was removed and a privileged radio inspection confirmed
that the Wi-Fi interface had returned to managed mode. No device identities,
household role names, credentials or firmware are published here.

## JH-G01U: eighth ESPHome installation

A second AP-capable USB Wi-Fi adapter allowed the ordinary conversion to run in
its own container/network namespace while the AWP02L-N experiment retained the
first radio. Neither workflow changed the other's radio or wired management.
The JH-G01U loader identity matched the intended old LocalTuya device and reported
1,024 KiB flash, QIO at 40 MHz and active user2.

The 420,800-byte GPIO-neutral image eventually completed in 259,898 ms. Transfer
had stalled around 30 KiB while the target remained associated. A live TX bitrate
limit to legacy 1/2 Mbps was applied to that AP interface; the transfer then
completed without a power cycle or another flash request. This observation does
not establish that the bitrate change alone caused recovery. Inspect association,
TCP progress and logs before interrupting a slow write.

After encrypted API identity verification, a 440,480-byte JH-G01U candidate was
installed through encrypted OTA. The operator confirmed button-driven load
switching with GPIO4 relay and GPIO5 button. GPIO12 initially lit the indicator
opposite to the load; its active-low correction was compiled, uploaded and checked
through the API. A fresh visual LED check and separate restart/power-cycle tests
have not been performed. See the provisional [GPIO package](gpio.md#jh-g01u-gpio4-relay-and-active-low-gpio12-indicator).

HA migration uses a canonical switch entity. The requested existing light card
was changed to an on/off switch button in the same dashboard position; the
unrelated Matter light device was retained. The old room card and floorplan
binding were removed instead of retaining the plug at its previous location.
Two old motion rules targeting only this lamp were retired; applicable global
off and notification rules were migrated. Final readback found the new ESPHome
switch available and off, the exact old LocalTuya identity removed, and no old
references in 1,970 active files. The canonical switch was reachable as an
OnOffPlugInUnit through the existing Matter bridge; all three fabrics and the
previous endpoints were preserved. No extra load cycles or restarts were used
for this migration. Controller-app acceptance remains deferred.

## Another WP5: ninth ESPHome installation

The owner selected another WP5 and explicitly requested reuse of the established
profile without repeated physical/load or restart tests. After an initial pairing
window expired, the phone reconnected to the conversion AP and the exact intended
device reached the intermediate loader. Its identity matched the old LocalTuya
record and it reported 1,024 KiB flash.

The complete 440,688-byte WP5 image was written directly in 11,954 ms, rather than
installing a diagnostic-only image first. It uses GPIO15 relay, GPIO13 button,
inverted GPIO2 relay indicator and an independent inverted GPIO0 red indicator.
Encrypted API readback verified the same device and the expected entities. No
button, load, indicator or restart acceptance test was performed on this unit;
reuse was the operator's explicit choice.

The old LocalTuya device was removed only after the replacement was available.
Its HA automations, dashboard row and two curtain power profiles now use the
canonical replacement entity. One HA configuration restart loaded those cached
profiles; this was not a plug restart test. Runtime readback confirmed both
profiles and no active references to the old entity remained. A historical
power timestamp was retained as history, without inventing a new power-on event.
The relay is reachable as an OnOffPlugInUnit in the existing Matter bridge,
preserving all three fabrics and the previous endpoints. Router DNS naming was
updated without changing the reserved address. Controller-app checks remain
deferred.

The installed desktop client and six local/saved configuration files were
updated and verified after the client reopened. Its existing button position and
unrelated settings were preserved. Two existing server configuration Secrets
were updated by changing only this role's entity and label, with readback of the
result. Those web deployments were already not ready before the change, so
running web-application adoption is not claimed. No workloads or plugs were
restarted for this client update.

## Another YM-WS-1: tenth ESPHome installation

The next YM-WS-1 reused the established GPIO15 relay, GPIO13 active-low button
and inverted GPIO12 internal relay indicator. The operator's standing same-model
reuse instruction waived repeated physical/load/indicator and restart checks.
The exact old LocalTuya identity matched both the intermediate loader and final
encrypted ESPHome API; no diagnostic-only firmware was needed.

The complete 440,480-byte image was written in 11,754 ms. ESPHome 2026.9.1 returned
the expected relay, button, status and diagnostic entities. The conversion
container was removed and its radio returned to host managed mode. No physical
acceptance result or restart behavior is inferred from the successful API check.

The HA migration removed the exact old LocalTuya device and updated the existing
dashboard row, two automations and two shared away-scene references. The original
one-minute power-restoration delay and its helper condition were preserved.
Natural automation activity is not counted as a requested physical test. A scan
of 2,427 active files found no retired entity or legacy device-alias references.
No HA restart was required. Router DNS was normalized while retaining the address.
The installed client, six saved configurations, two server configurations and
three client projects had no old-role references, so no new client control was
added and no client configuration change was needed.

Matter management initially timed out through both service and LAN endpoints;
bounded container-exec and node-proxy health requests also timed out despite
ready pod/node status. Longer bounded requests from the wired workbench restored
management visibility. The filter update timed out, but independent readback
confirmed it had been applied, so it was not repeated. The relay was added with
the maintenance unit below; both appeared as reachable OnOffPlugInUnits. The
bridge count increased from 16 to 18 while existing endpoints and all three
fabrics were preserved. No bridge reset or recreation was needed. Controller
load checks remain deferred.

## Maintaining an existing ESPHome plug

A separate plug already running ESPHome was updated from 2026.8.0 to
[2026.9.1](https://github.com/esphome/esphome/releases/tag/2026.9.1) and given a new
household role. It is recorded separately from the Tuya conversion count. Its
identity, reserved address and existing API/OTA authentication mode were preserved. The
native API on this older installation is unencrypted; the encrypted-API claims
for newly converted plugs do not apply to this maintenance operation.

The first update preserved the historical GPIO configuration. The operator then
identified the hardware as YM-WS-1 and confirmed working physical button/load
control but a dark indicator. Inspection found two configuration problems:
the inherited LED used GPIO2 rather than the matching variant's inverted GPIO12,
and its actions were attached only to a template switch, bypassed by the physical
button's direct relay toggle.

A 409,376-byte corrective image installed in 8.76 seconds. It keeps the GPIO15
relay, GPIO13 button and `ALWAYS_OFF` behavior, but uses an internal binary LED
on inverted GPIO12 with actions on the underlying relay state changes. A fresh
native API connection confirmed the exact device, new compilation timestamp,
version and unchanged exposed switch identity. The operator's prior load/button
result is recorded separately. The operator subsequently confirmed that the
corrected indicator works, completing the button/load/indicator acceptance for
this existing device. No extra load or restart test was performed.

Both active source trees now contain the renamed, corrected YAML and no old
duplicate source. Shared includes and secrets were unchanged. The source requires
ESPHome 2026.9.1; the existing dashboard runtime is still 2026.8.2 and must be
upgraded before it can build this configuration. A firmware update does not
implicitly upgrade the dashboard service.

HA retained the original device and integration entry while assigning the new
canonical relay entity and updating its dashboard card. The relay was added to
the destination room's existing motion-on and motion-off rules; their sensors,
five-minute timeout, daylight conditions, manual-override helper and other
targets were retained. Obsolete sole-target rules from the former room were
removed, along with exact old references in shared rules and the shutdown
script. The old room's manual-override helper, its current state, button and
helper-control rules were explicitly preserved. A separate similarly named
device was not part of this migration.

A scan of 2,425 active files found no retired lamp references. HA required no
restart. The renamed firmware-update diagnostic initially remained unavailable
because its setup had captured the cached old node name. Once the cache and
dashboard filename matched the new node, reloading only that integration entry
restored the diagnostic. The relay and firmware entity were available again
after the operator moved the plug back to its installed position. Router DNS was
updated without changing the reservation. Client/deployment inspection found no
old bindings to replace.

The existing 3D floor-lamp object was bound to the canonical switch through a
narrow inventory update. Its geometry, placement and other objects were
preserved, and a full inventory readback matched the intended change. Control
uses the switch domain without implying dimming or color capabilities. No
physical load command or HA restart was needed for that binding.

## Another JH-G01U: eleventh Tuya conversion

The next JH-G01U reused the earlier GPIO4 relay, GPIO5 button and corrected
active-low GPIO12 indicator profile. The operator's standing same-model policy
waived repeated physical and restart checks. The old role had already been
removed during a previous multi-device cleanup, so the historical integration
record was matched to DHCP and then to the exact intermediate-loader MAC before
writing firmware. A stale DHCP hostname was not treated as role evidence.

The complete 440,480-byte image was built locally with ESPHome 2026.9.1 and
passed checksum, 1 MB flash, DOUT and 40 MHz checks. The loader wrote it in
11,878 ms without a stock backup. Encrypted native API readback confirmed the
same physical identity, version and final-profile entities. The conversion
container was cleaned up and both radios returned to host managed mode. Router
DNS was renamed while retaining the reservation, with forward and reverse
lookups checked from the router and client.

HA adopted one canonical relay and added a separate dashboard row, preserving
the existing curtain-power control. Its former motion-on action was restored
before the unrelated legacy actions and marked `continue_on_error`, so either
side's failures cannot prevent the other side's commands. The existing sensor
triggers and manual-override condition were retained. Configuration validation,
automation reload and runtime entity linkage passed without an HA restart or
manual load commands. All curtain schedules and manual-override helpers were
preserved.

The old evening-off rule had been retired earlier because its trigger lamp was
removed. The operator selected its current replacement explicitly. A separate
evening rule now turns off only the media-power relay after that lamp remains
off for 15 minutes, with the sun below -2 degrees and the existing manual override
off. It does not depend on an unrelated unavailable device or re-enable the
retired multi-device rule. Full configuration validation, an automation-only
reload and runtime references passed. Six isolated tests using the installed
HA runtime and fake services covered timing, cancellation, override and daylight
guards, wrong-lamp events and startup with the lamp already off. No physical
load was switched for those tests.

One exact relay filter was added to the existing Matter bridge. Its device count
increased from 18 to 19, with the new OnOffPlugInUnit reachable, every prior
endpoint identity preserved and all three controller fabrics unchanged. No
additional controller or physical load test was performed.

## Another YM-WS-1: twelfth Tuya conversion

The next YM-WS-1 reused the established GPIO15 relay, GPIO13 button and inverted
GPIO12 indicator profile. The operator renamed its role during the first write
attempt. That request stalled without a recorded final-image download, so the
outstanding HTTP client was stopped instead of issuing another blind write.
A fresh read later confirmed the same device still running the intermediate
loader. One bounded retry installed the already rebuilt final-name image in
11,689 ms. The 440,480-byte ESPHome 2026.9.1 image passed header and checksum
checks; encrypted API readback matched the physical identity, final role and
compilation timestamp. The API also remained reachable after the operator's
reported power interruption; no relay transition was tested during that event.

The profile previously verified on another sample was reused without repeated
physical or restart testing. The later recovery below establishes that this
unit needed a different GPIO map. The conversion container was removed, both
radios returned to managed mode, and the existing DNS reservation retained its MAC/address
while adopting the new name. Forward and reverse DNS checks passed.

The new HA relay replaced the exact old LocalTuya device. Eight references in
six power-management automations and customization were migrated; estimated
load, conditions, thresholds, ordering and delays were preserved. An active-file
audit found no old references. Dashboard content, unrelated devices and manual
override states were unchanged. Final firmware source and separate device
secret references were saved in both active ESPHome configuration locations.
Client/deployment configuration inspection found no old references to replace.
After the migration, the operator requested a dashboard control beside an
existing appliance. One switch row was added to that entities card; API and
persisted-storage readback confirmed that all prior rows and manual overrides
were preserved. This later UI change is separate from the migration baseline.

### Twelfth conversion follow-up: diagnosis deferred

On 2026-10-10, the owner reported a dim indicator and no physical response from
this unit. The encrypted API still reported the expected device and installed
build, with fresh signal readings. A requested short button press produced
neither an observed native button transition nor an owner-observed relay click
or indicator change. API availability does not validate this unit's reused
GPIO13-button/GPIO15-relay/GPIO12-indicator mapping.

The documented alternate YM-WS-1 map uses a GPIO1 button, GPIO14 relay and GPIO13
indicator. That makes a profile mismatch plausible, but the enclosure marking
was not reconfirmed and a hardware fault has not been excluded. An input-only
GPIO1/GPIO13 probe compiled successfully and passed the image checksum check;
it was not uploaded. No relay command or HA configuration change was made
during this investigation.

On 2026-10-11, the owner initially deferred the requested unloaded power cycle
and model check. Diagnosis stopped at that point with the existing firmware
still installed and no per-unit physical acceptance. The later recovery is
recorded separately below.

### Twelfth conversion recovery: alternate GPIO14 profile confirmed

Later on 2026-10-11, the owner reported the indicator lit but no response or
apparent network connection. A fresh check found the same device online with
its original ESPHome 2026.9.1 build and an accessible OTA service. The owner
confirmed the output was unloaded before diagnosis resumed.

The prepared 424,448-byte input-only image was installed and its identity
verified. A short physical press and release produced GPIO1 events, confirming
that the former GPIO13 button assignment was wrong. A 440,480-byte image with
GPIO1 button, GPIO14 relay and GPIO13 indicator restored physical switching.
The owner then reported that the indicator was opposite to the load. A second
440,480-byte update changed only LED polarity to active-high. The owner
confirmed that the lamp and indicator now turn ON and OFF together; native
events recorded both complete button cycles and the matching relay changes.

The final encrypted API check matched the same device, final build and all six
original component identities. The relay returned OFF after the firmware
restart and ended OFF after physical testing. The original HA entity IDs were
preserved, no temporary probe entities remained in HA, and the corrected
source was synchronized to HA, ESPHome Dashboard and the private workbench.
Dashboard validation passed without changing credentials. A controlled mains
cycle and boot-transient measurement were not performed in this recovery.

The reusable [alternate YM-WS-1 profile](../examples/ym-ws1-gpio14.yaml) records
the observed hardware. This repairs an existing conversion; it does not add
another device to the conversion count.

## Existing Tasmota SP20: metered ESPHome maintenance

A TECKIN SP20 already running Tasmota 13.4.0 was handled separately from the
Tuya conversion workflow. Its live template identified GPIO4 relay, GPIO13
button, GPIO0/GPIO2 indicators and BL0937/HJL metering with inverted GPIO12
selection, GPIO5 CF and GPIO14 CF1. Actual calibration values and existing
lifetime, daily and prior-day counters were read privately before the handover.

An isolated ESPHome 2026.9.1 build produced a 455,312-byte ESP8266 image; its
325,877-byte gzip upload fit the reported free sketch space. The existing
Tasmota web updater accepted it in 11.14 seconds. Encrypted API readback matched
the original MAC/address, version and relay state. All ten metering fields
became available with finite values, and cumulative energy continued from the
source counters. Calibration was transferred mathematically from the installed
driver; an independent measurement calibration was not performed.

The source used restore-prior-state behavior and was on immediately before the
upload. The replacement deliberately used a first-boot ON fallback and then
ESPHome's own persistent relay state. It did not reinterpret Tasmota's flash
bytes as ESPHome preferences. No manual relay toggle or extra restart test was
performed. The [reusable procedure](tasmota-sp20-migration.md),
[profile](../examples/teckin-sp20-metered.yaml) and counter helper keep deployment
values in private secrets. Native tests cover cumulative increments, invalid
readings, daily rollover, clock reversal and reboot baselines.

The HA handover kept the canonical relay and ten metering entity IDs. The old
Tasmota-owned device was removed through HA's supported device-removal hook,
which cleared only its retained discovery information. The shared integration
and unrelated devices were preserved. Units, device/state classes, the original
counter-start value and effective numeric display precision matched the source.
All eight existing statistic metadata records and the inspected historical data
remained unchanged. Solar-control references, the dashboard and manual-override
states were preserved without an HA restart or manual load commands.

The final YAML and its local counter header were saved in both active ESPHome
configuration locations, with the build-machine-only path removed and private
secret references resolved. DNS adopted the normalized name while retaining
the original reservation. Forward and reverse lookups passed.

## Twelfth conversion and SP20: delayed Matter discovery recovered

The twelfth converted plug and the separate metered SP20 received exact relay
filters in one additive update. Its client timed out, but independent readback
confirmed that both filters were saved. Prior endpoint identities and all three
controller fabrics were unchanged. The initial graph had 20 devices, with the
SP20 relay reachable; discovery of the other new relay remained pending.
The hub logged repeated HA registry request timeouts. A supported HA refresh
was requested once and a bridge refresh acknowledged. Discovery later caught up:
readback confirmed 21 devices and both relays reachable as OnOffPlugInUnits,
with every prior endpoint identity and all three fabrics preserved. No service
restart, factory reset or recommissioning was performed. Physical controller
tests remain deferred.

## Another KMC 30137: thirteenth Tuya conversion

The second KMC 30137 reused the established GPIO14 relay, active-low GPIO1 button
and inverted GPIO13 indicator profile. The operator selected a new equipment
role and waived repeated physical and restart checks under the existing
same-model policy. The relay retains the OFF-on-start policy.

The stock identity and DHCP lease matched the intermediate loader's physical
MAC and one-megabyte flash report. A 440,480-byte ESPHome 2026.9.1 image passed
DOUT/40 MHz/header/checksum validation, then one final upload completed in
18,894 ms. Encrypted API readback matched the expected MAC, friendly name,
version and exact compilation timestamp. Factory firmware was not backed up.
DNS kept the reserved address while adopting the new role name; both forward
and reverse checks passed. The conversion container and session were removed,
and both Wi-Fi radios returned to managed mode.

The HA handover retired only the exact old LocalTuya device and updated two
solar-control rules, customization and the existing dashboard row. The operator
explicitly retained the solar rules' thresholds, conditions and actions on
other loads. A scan of 2,455 active files found no old references. Other device
configuration, source files and manual-override states were preserved, and the
final YAML and private secret references were saved in both active ESPHome
locations. No HA restart or manual load command was used.

The role change also exposed five active shortcuts in an installed media-control
helper. With operator approval, the old plug was removed from two mixed audio
groups while their other target was retained; three lamp-only shortcuts were
retired. Those controls were not blindly renamed to operate the new equipment.
The installed command map and saved source were verified after the edit.

An exact relay filter was then added to the existing Matter bridge. Following
supported registry and bridge refreshes, readback showed 22 devices and the new
relay reachable as an OnOffPlugInUnit. All prior endpoint identities and all
three controller fabrics were preserved. No repeated controller load test was
performed.

## Second AWP02L-N: handshake blocked, AP recovery pending

A separate AWP02L-N associated with the ordinary conversion AP but failed six
PSK identity `02` handshakes with bad-record-MAC errors. No intermediate loader
or replacement firmware was reached. A 420,800-byte GPIO-neutral ESPHome image
was built and retained privately; it was not installed. Its intended role uses
an ordinary latching power switch, without pulse or inching behavior.

After the ordinary session was cleaned up, the operator placed this device in
slow-blinking AP mode. The isolated experimental session matched its BSSID and
gateway neighbor to the private target. All 117 archived source files matched
the pinned ESP8266 branch, and a dry run built one 256-byte packet without
transmission. One recorded packet was then sent. The first connection check
passed, but the subsequent authentication checkpoint could no longer reach
the AP; a rescan returned no matching target. Normal Wi-Fi provisioning never
started, and neither replacement-key authentication nor conversion is verified.

Recovery requires bringing this same physical device's AP back, keeping its
attempt marker, and validating identity again before provisioning. No HA,
desktop or Matter migration was applied. The successful Tuya conversion count
remained thirteen at that checkpoint; this unit is distinct from the earlier
AWP02L-N experiment.

## TanTan WP3: fourteenth firmware conversion

A TanTan WP3 previously exposed as a LocalTuya light reached the intermediate
loader. Its physical identity matched the private inventory, and the loader
reported ESP8266 bootloader version 4, normal boot and 1 MiB flash. A stock
backup was retained privately as an exception to the earlier batch policy.

The first 424,448-byte ESPHome 2026.9.1 image assigned only GPIO4 and GPIO13
button-probe inputs. It installed in 8,000 ms, and encrypted API readback
matched the intended identity, version and compilation timestamp. One
operator-controlled short button press produced GPIO13 press/release events
while GPIO4 stayed unchanged. That supports the older WP3 template as a
candidate, rather than the variant with GPIO4 button and GPIO14 relay.

The 440,480-byte final candidate uses a GPIO15 relay, active-low GPIO13 button
and internal inverted GPIO2 indicator; GPIO0 remains unassigned. Its DOUT,
40 MHz, 1 MiB image and checksum passed validation. Encrypted OTA transferred
it in 4.32 seconds, with a 4.34-second complete update. The native API matched
the expected physical identity, ESPHome version and compilation time, exposed
one relay and the physical button, and no longer exposed the probe entities.
API on/off state checks passed. A software restart requested from ON returned
the same build with reported relay state OFF. Physical contact state and boot
transients were not measured.

After that restart, two physical button presses produced button events and
matching reported relay transitions OFF, ON, OFF through the encrypted API.
The operator confirmed relay clicks and actual light-load and indicator
switching in both directions during those presses. This establishes the
observed GPIO15 relay, GPIO13 button and inverted GPIO2 indicator mapping for
this unit. The conversion container, AP and dedicated workbench session were
closed afterward.

The [WP3 profile](../examples/wp3-gpio15.yaml) also passed an isolated
configuration validation and build using nonproduction credentials. That
440,528-byte test image passed ESP8266 header, checksum and 512 KiB size checks;
it was not installed. The installed firmware and test build are separate
artifacts. The operator then moved the plug to its installed position, with
mains power disconnected and reconnected. Subsequent HA readback found the
ESPHome relay available and OFF. Availability-history gaps are not assigned
solely to that power interruption because HA migration and reloads overlapped.
Boot transients and an on-to-off physical power-cycle test were not measured.

All six persisted client configurations match their reviewed migration edits.
The running native desktop client shows the canonical switch available and
OFF with the intended label and placement, retaining the other related control,
unrelated plugins and authentication. HA, HA MQTT and gateway connections were
live, and no actuator commands were sent during this client verification.
During the handover, motion initially did not switch on the relocated load:
the loaded automation still targeted the old light through `light.turn_on`.
After reloading the automation and removing the old entity, a natural sensor
OFF-to-ON event triggered that automation and the new switch changed OFF to ON
about 0.13 seconds later. Matching sensor-parent and automation contexts tied
the events together. The operator confirmed that motion control was working.
No synthetic trigger was used; the sensor and manual-override helper were
unchanged. The final audit scanned 2,456 active files with no retired-entity
references. Migrated files matched the intended content; unrelated source
files and LocalTuya device configurations were unchanged, and the old identity
was absent. Automations, scripts, Lovelace and the floorplan were updated.
The existing mixed group retained its other two members alongside
the new switch. Final firmware source and private secret references were saved
in both active ESPHome locations. HA remained running with no restart.
The [WP3 migration procedure](wp3-migration.md) distinguishes source, runtime
and physical checks. No Matter or controller result is claimed for this unit.

## Another WP5: fifteenth firmware conversion

A further WP5 selected from an existing LocalTuya light role reached the
intermediate loader. Its identity matched the intended private device record;
VTRUST-FLASH 1.5 reported ESP8266 bootloader version 4, normal boot, DOUT at
40 MHz and 1,024 KiB flash. A 1 MiB stock backup was retained privately.

The 424,432-byte input-only ESPHome 2026.9.1 image passed header, checksum and
staged-digest checks, then installed in 12,787 ms. Encrypted API readback matched
the intended identity, version and exact compilation timestamp. One
operator-confirmed short press produced GPIO13 press/release events while GPIO4
stayed inactive, identifying the button input. The probe assigned no outputs.

The 440,464-byte final image passed DOUT/40 MHz/1 MiB and checksum checks, then
transferred through encrypted ESPHome OTA in 9.78 seconds, with a 9.85-second
complete update. Encrypted API readback matched the expected physical identity,
version and compilation timestamp. It exposed one relay switch without the
temporary probes. Native API on/off control passed, and a software restart
requested from ON returned the same build with the relay reporting OFF.
The operator then connected a lamp and pressed the button twice, confirming
the relay, actual lamp and indicator worked. Matching button events and relay
states OFF, ON, OFF were captured. Their batched recording timestamps are not
used as latency measurements. This unit passed its own physical acceptance;
a controlled mains-cycle test and boot-transient measurements were not performed.
The operator later confirmed returning it to the installed position. A subsequent
HA read found the new switch available and OFF, with the previous migrated plug
still available. This relocation is not recorded as a controlled ON-to-OFF
power-cycle test.

The installed profile omits the independent GPIO0 red-indicator channel;
the operator requested the relay switch without that extra light entity. The
existing public [WP5 example](../examples/wp5-gpio15.yaml), which includes the
separately controlled red channel for earlier units, remains unchanged. The
existing motion automation's sun-elevation condition is retained, even when
it currently prevents motion control.

The desktop handover is complete. All six persisted configurations use the new
canonical switch and label, with the old identifier and alias absent. The
running native client shows that switch available and OFF at its existing
position with its icon preserved. The previously migrated plug is still
available. Gateway, HA and HA MQTT connections are live; no actuator commands
were sent during the client update. HA migration and reload verification are
complete across automations, scripts, the group and Lovelace. A direct HA
service-control cycle passed and restored the original
relay state. The exact old LocalTuya device was retired with unrelated
identities preserved; the old entity and its alias are absent. The existing
mixed group contains both newly migrated relay switches and its other light.

The loaded motion configuration was verified, but the unchanged daylight
condition prevented natural motion from turning the relay on at that time.
This is not recorded as an end-to-end natural motion acceptance test, and no
guard was bypassed to obtain one. The configured power estimate, off timeout,
sun and manual-override conditions were retained, and the loaded off action
handles the replacement switch correctly.

The final audit scanned 2,457 active files and found no retired-entity
references. Migrated files matched their intended content; unrelated sources,
LocalTuya devices, the preceding WP3 and manual-override helpers were unchanged.
Final ESPHome source and private secret references were saved in both active
configuration locations. HA remained running and required no restart.

## GREFIC CZ-U201: sixteenth firmware conversion

An owner-reported two-outlet GREFIC CZ-U201 accepted the ordinary handshake.
The live loader identified ESP8266 with 1 MiB flash. The retained private flash
image includes the original application's two-channel hardware JSON. A neutral
image followed by encrypted OTA installed ESPHome 2026.9.1. Independent native
API commands passed all four combinations and returned both outputs to OFF.
The left outlet is physically confirmed as channel 2/GPIO14 and the right outlet
as channel 1/GPIO15. A shared-button cycle passed with a real lamp. Starting
with both relays ON, a controlled mains cycle returned both to reported OFF,
and the connected right lamp stayed off. HA adopted separate left and right
switches. Each passed an ON/OFF service cycle with a matching command context
and the other outlet unchanged. Both ended OFF. Final source and secret
references were persisted and independently verified in HA and ESPHome Dashboard;
unrelated entities and secrets were preserved without restarting HA.
See [the detailed record](grefic-cz-u201.md). Ten converted units have now passed
their own physical button/load checks.

A subsequent software handover assigned the two outputs to separate load roles
previously served by LocalTuya and Matter plugs, retaining both original devices
and their names. HA automations, Lovelace bindings and the native desktop client
now use the replacement outputs. Configuration and availability checks passed
with both outputs OFF. The owner subsequently confirmed relocation and both
load connections; encrypted API and HA availability passed at the installation
location. The owner confirmed that an independent OFF-to-ON command illuminated
the installed floodlight while the other output remained OFF, then confirmed
that the floodlight went dark after an OFF command and the separately powered
appliance worked from its own remote after its output was turned ON. All three
transitions had matching HA command contexts and left the unaddressed output
unchanged. Both intended loads passed their installation checks. A final
owner-requested OFF command to appliance power left both outputs OFF, with a
matching HA command context. No firmware or shared-button behavior changed.

The owner later requested deletion of the retained LocalTuya appliance-power
plug, reporting that it was reset and not currently needed. Its device and
entity were removed through HA's supported API. The persisted LocalTuya
configuration changed from 37 devices to 36, with every other device's settings
unchanged. The replacement output remained available and OFF; the old Matter
plug was retained.

## Third AWP02L-N: stock OTA blocked before firmware transfer

The owner confirmed rapid pairing mode, the phone on the conversion AP and an
unloaded outlet. The plug associated with the MAC corresponding to its existing
LocalTuya identity. Thirteen TLS attempts presented PSK identity version `02`
and failed with `DECRYPTION_FAILED_OR_BAD_RECORD_MAC`. The intermediate loader
never appeared and the HTTP log recorded no firmware image transfer.

A fresh GPIO-neutral ESPHome 2026.9.1 candidate compiled successfully in 28.82
seconds with separate private credentials. Its 420,784-byte ESP8266 image passed
checksum and 1 MB DOUT/40 MHz header checks. It was staged but not installed;
its flash layout is therefore not a hardware confirmation for this unit.
The ordinary session was stopped, its container removed and its Wi-Fi radio
returned to host managed mode. No experimental packet was sent.

The ESP8266 CloudCutter branch was rechecked and still matches the previously
examined revision. Its stock-image addresses are not established for this
unit, so it provides no justified automatic next step. The known model and
Espressif network identity support investigating an ESP8266 serial path, but
the actual module and boot/UART pads still need inspection of the unplugged
board. Existing HA, client, automation and Matter references were not changed.
HA still displayed its earlier state while the original local TCP endpoint was
unreachable; no present relay state or restored home-network connection is
claimed. The count of successful conversions remains sixteen.

## KMC 30608: seventeenth firmware conversion

A three-relay Smart Tap running stock firmware 1.0.5 accepted the ordinary
Tuya-Convert path. The loader identity matched HA, with ESP8266 and 1 MiB flash.
A private full-flash read was retained after loader installation. GPIO-neutral
ESPHome and an input-only probe established encrypted API access and GPIO16
button behavior. The final 429,312-byte ESPHome 2026.9.1 image uses relay
GPIO15/13/14 and starts all outputs OFF.

Native control and a software restart passed. The owner verified each numbered
outlet with a lamp, the common button's OFF/ON behavior, and a five-second mains
cycle from all outputs ON. The same build returned with all outputs OFF. The
existing three HA entity IDs now address the corresponding ESPHome switches;
only this device was retired from LocalTuya. Final source was saved in HA and
the ESPHome Dashboard. Visual indicator acceptance remains separate.
See [the detailed record](kmc-30608.md).

All three channels also passed separate HA ON/OFF service checks with matching
state contexts and the other channels OFF. The final state is all OFF. Other
LocalTuya device configurations are unchanged. Two obsolete third-channel alias
references in one notification automation were corrected; configuration
validation passed and automations were reloaded without restarting HA.

A subsequent 432,560-byte ESPHome 2026.9.1 update added all four native HLW8012
fields: voltage, current, active power and energy since boot. The published
GPIO12/4/5 interface produced readings and responded to the test lamp on outlet
3; energy increased under load. HA exposes all four fields and a diagnostic
`Not calibrated` status. Calibration was explicitly deferred by the owner, and
coverage of the other outlets has not been tested. The three switch IDs remain
unchanged, all relays ended OFF, and updated source was saved in both HA and the
ESPHome Dashboard. See the [metering observations](kmc-30608.md#metering-update).

## Second KMC 30608: eighteenth firmware conversion

A second KMC 30608 with stock firmware 1.0.5 accepted ordinary Tuya-Convert.
The loader reported ESP8266, bootloader 4, and 1 MiB QIO flash at 40 MHz.
A private post-loader flash read was retained. The 420,800-byte neutral image
was followed by a GPIO16 button probe and a 432,560-byte relay/metering image.
Three numbered outlets passed individual fan tests, and the common button
stopped and restarted the fan. A five-second mains disconnection from all ON
left the fan stopped and all three native states OFF on the production build.
HA handover retained the three existing IDs, and source/private credentials
were persisted and verified in HA and ESPHome Dashboard. Exactly this LocalTuya
device was removed; the other 34 device configurations remained unchanged.

The separate outlet indicators remained dark. A temporary GPIO1 test lit only
the common indicator beside the button, confirmed by the owner. The stock
hardware table disables all three per-channel LED outputs. The production
image was restored; no speculative GPIO assignments were added. Stock Tuya
datapoints 1/2/3 map to GPIO14/13/15, while physical outlets 1/2/3 map to
GPIO15/13/14. Migration preserves this distinction. After the owner confirmed
the first KMC remained on the table without its normal loads, that unit's
earlier HA role association for outlets 1 and 3 was corrected while retaining
its existing entity IDs. The owner also clarified that the individual outlet
indicators previously lit with their loads; the second sample's dark indicators
remain an unresolved regression, not a confirmed hardware failure.
The first sample's outlet 3 indicator subsequently lit correctly with the same
GPIO/metering configuration. The owner deferred further diagnosis of the second
sample's indicators. Both KMCs were returned to all outputs OFF.

## Supernight CV01: nineteenth firmware conversion

The owner identified SUPERNIGHT FCC ID 2ANJ7-CV01 and confirmed both outlets
empty. Stock firmware 1.0.4 accepted ordinary Tuya-Convert. The loader reported
an ESP8266-family device, bootloader 4 and 1 MiB DOUT flash at 40 MHz. A full
post-loader read was retained privately, followed by the 420,800-byte neutral
ESPHome 2026.9.1 image.

An input probe confirmed the left button on active-low GPIO1 and the right
button on the ADC input. The latter read about 7 released and 1024 pressed,
opposite to the published reference. The 435,872-byte production image uses
that observed polarity and waits ten seconds plus a released reading before
arming the right button. It adds two `ALWAYS_OFF` relay channels and four
uncalibrated HLW8012 measurements.

Native controls, a software restart, both physical outlets and independent
button behavior passed. After a five-second mains disconnection from both
outputs ON, the fan remained stopped and both reported OFF on the same build.
HA adopted the new device, verified both switches through service calls and
exposed all four measurements. Both outputs ended OFF. Source and private
credentials were saved and verified in HA and ESPHome Dashboard. No unrelated
entity identity or existing secret value changed. Indicator/night-light
behavior, absolute calibration and left-outlet meter coverage remain pending.

## Third KMC 30608: twentieth firmware conversion

An isolated KMC 30608 Type 3 SPD running stock 1.0.6 reached the ordinary
Tuya-Convert loader on a second attempt after an owner-controlled mains cycle.
The first attempt downloaded the intermediate image but did not expose the
loader. The working loader reported ESP8266-family silicon and 1 MiB DOUT flash
at 40 MHz. A private post-loader flash read was retained. A header-checked
420,800-byte neutral image and an input-only GPIO16 probe both passed.

The stock channel initializer matches the second KMC sample. The final
432,560-byte ESPHome 2026.9.1 image exposes three independently controlled
relays and four uncalibrated HLW8012 measurements. Native channel controls and
a software restart from all ON to all OFF passed. The owner confirmed a test
load on physical outlet 1, then deferred the remaining outlet, common-button
and mains-cycle checks. HA adopted three switches
and four available metering sensors with the expected units and state classes.
Source and private credentials were saved and read back in HA and ESPHome
Dashboard. No pre-existing LocalTuya entity identity changed. Cleanup returned
all three outputs OFF, confirmed through the encrypted API. HA service
switching tests are also deferred by the owner, not passed. See the
[third-sample record](kmc-30608.md#third-sample-stock-106-and-dout-flash).

## Second WP3: twenty-first firmware conversion

The owner identified a previously retained LocalTuya WP3 for conversion to a
numbered spare switch. The loader matched the selected identity and reported
1 MiB flash; a complete private post-loader backup was saved. A 424,432-byte
input-only probe installed successfully, and a physical button press identified
GPIO13. The 440,480-byte final image uses GPIO15 for the relay and inverted
GPIO2 for the indicator, with an ALWAYS_OFF restore mode.

Encrypted OTA and native relay controls passed, including software restart
from ON to OFF. The owner confirmed button/load/indicator operation; the final
observer did not capture both physical cycles. HA adoption preserved the
existing numbered entity ID and dashboard row. Final source and private
credentials were persisted and read back in both configuration locations.
Controlled mains-cycle and boot-transient tests remain unperformed. See the
[second WP3 record](wp3-migration.md#second-sample).

## Subsequent household role changes

The owner reassigned outlets 1 and 2 of the second KMC 30608 and both Supernight
outlets after physical acceptance. Three predecessor plugs were retained under
neutral names; the former television plug was also retained. Logical role IDs
were attached to the new channels only after their original owners had been
renamed. Independent registry checks confirmed all seven mappings against
device and channel unique IDs, and confirmed that the KMC's third channel kept
its existing identity.

HA dashboard references, shared shutdown logic and state notifications were
updated for the new roles. Existing logical-role references were kept where
they already selected the correct replacement channel. Duplicate dashboard
entries were removed. An obsolete audio automation in an unloaded legacy file
was disabled rather than repurposed as lighting behavior. Configuration checks
and targeted reloads passed, retaining the enabled/disabled states of all 120
automations. The rename work issued no load-control or firmware commands.
Exact household mappings and before/after records remain private.
At the owner's subsequent request, the three retained predecessor plugs were
also added to the bottom of the existing dashboard switch list. A readback
confirmed exactly one entry for each, with the other dashboard content and
relay states preserved.

The first KMC was subsequently assigned three utility-power roles. Its former
decorative-light targets were removed from morning shutdown, shared shutdown
and surplus-power lighting actions before completing the role change. The new
names explicitly distinguish supply power from appliance operation. Existing
separate utility controls were retained for the owner's later physical move;
no automatic handover or scheduled disconnection was created. Notifications
and a grouped dashboard section use the new IDs. An active-reference scan found
no remaining retired lighting IDs; no load commands or firmware changes were
part of the reassignment.

## Deployed source audit and restoration

On 2026-10-11, the active HA and ESPHome Dashboard source directories were
audited against the ESPHome device registry and the private per-unit inventory.
Eleven earlier converted plugs had no individual YAML in either active source
directory, although their accepted source files remained in the private
workbench. The more recent conversions already had deployed source files.

The eleven missing configurations were restored to both locations. Each source
was matched to the recorded unit, current HA role, node name and API credential
before publication to the private deployment. Validation with ESPHome passed
for all eleven prepared files. Local build-directory overrides were removed;
the installed node names, hardware profiles and existing credentials were
retained. Per-unit secret references prevent accidental dependence on generic
secret names. Existing deployed source files and secret values were preserved,
and both copies of every restored YAML matched on readback.

There are now thirty top-level configurations in each deployment source
directory, including twenty-five plug configurations. The latter include all
twenty-one Tuya conversions, the two previously documented maintenance units
and two older plugs. Registry-only role names can differ from the preserved
firmware friendly names. Source presence does not establish physical acceptance
or mean that a new firmware image has been installed. This restoration sent no
relay commands, performed no firmware uploads and did not resume the deferred
hardware investigations. Exact paths, identities, backup receipts and secret
values remain private.

The deployed validator initially exposed a separate build-environment gap: its
ESPHome version was 2026.8.2, whereas the recent local builds used 2026.9.1. Only
two of the twenty-five plug configurations passed validation in that container.
Twenty-one failed on a compile-process limit above the two CPUs visible there;
the two maintained older devices explicitly required at least 2026.9.1. The
source audit therefore left a separate requirement to align the Dashboard
version and compilation parallelism before attempting a new build. No deployment
upgrade or firmware update was performed as part of that initial audit.

The separately authorized Dashboard upgrade later on 2026-10-11 resolved that
gap. The active deployment now runs ESPHome 2026.9.1 pinned by OCI digest. All
twenty-two explicit compile-process limits above the container's two CPUs were
reduced to two in both private source copies, including the maintained device
whose version requirement had previously prevented its full validation.
Credentials, hardware profiles and relay behavior were preserved.

After the rollout, the Dashboard had one ready replica, returned HTTP 200 and
validated all twenty-five plug configurations successfully. The Deployment
specification changed only its image; its source volume, security settings and
replica count were retained. This maintenance did not upload device firmware
or establish any additional physical acceptance results. Detailed deployment
receipts remain in the private operations records.

## Software provenance

- Tuya-Convert: `a34b2c91862ed855542e8a32a14a9ab7573c4de9`.
- ESPHome target: `ghcr.io/esphome/esphome:2026.9.1`.
- Compatibility runtime: Python 3.11; paho-mqtt 1.6.1; sslpsk3 1.1.1;
  tornado 6.5.10; pycryptodomex 3.23.0.
- Existing Matter Hub image:
  `ghcr.io/riddix/home-assistant-matter-hub@sha256:0255708cac22bc5109fec84c9c87605a82825c557ca07cecbcb36a7aac795c8f`.
- Existing Matter Server image:
  `ghcr.io/home-assistant-libs/python-matter-server@sha256:170aa093ce91c76cde4cc390918307590f0f5558fcec93f913af3cb019e6562a`.

Image digests are public software identifiers, not credentials. The local
`versions.txt` records the actually pulled workbench images; mutable base-image
tags mean builds are not promised to be byte-for-byte identical.

## Still pending

Sixteen converted plugs passed per-unit physical button/load checks. Six earlier units also have
HA software-restart evidence; the seventh conversion's restart began already off,
so it does not prove on-to-off restoration. The eighth has no separate restart
test and its corrected indicator has not been visually rechecked.
The sixth and ninth use a previously verified WP5 profile, the tenth reuses
the established YM-WS-1 profile, the eleventh reuses the corrected JH-G01U
profile, and the thirteenth reuses the KMC 30137 profile. Repeated physical and
restart checks were waived by the operator for those units. The twelfth
initially reused the YM-WS-1 profile but subsequently required a different
GPIO map and LED polarity; its corrected configuration now has physical
button/load/indicator acceptance.
Their transfers and encrypted APIs were verified separately.
The fourteenth conversion, TanTan WP3, passed physical button/load/indicator
checks, encrypted API control and a software restart from reported ON to OFF.
It was available and OFF after the operator relocated and reconnected it;
an on-to-off physical power-cycle test and boot-transient measurements remain
pending.
The fifteenth conversion, another WP5, passed physical button/load/indicator
checks, encrypted API control and a software restart to reported OFF. Its
desktop handover and HA service-control/retirement checks passed. Its natural
motion acceptance was not exercised because the unchanged daylight condition
blocked it. The final source-reference audit passed. No controlled mains-cycle
or boot-transient checks were performed; its GPIO0 red channel is not configured.
Google Home and Alexa app control passed on the
first two converted plugs. Later controller checks were deferred. Controlled
power-cycle checks remain pending for earlier units; the GREFIC and KMC 30608
checks passed. KMC 30608 also passed a native-API software restart from all ON.
The full button-to-controller round trip remains pending.
Existing bridge fabrics were preserved, and household entity identifiers were
not published. A functioning server process is not a completed end-to-end
acceptance test. Track those gates in [ROADMAP.md](../ROADMAP.md).


### 2026-10-11 — iNewSwitch maintenance and s6 rename

The pre-existing iNewSwitch outlet was updated from ESPHome 2025.4.0 to stable
2026.9.1 by native OTA and renamed `s6`; this is maintenance, not another Tuya
conversion. Its private source is now `s6.yaml` in both HA `/config/esphome`
and Dashboard `/config`, replacing `inewswitch.yaml` without changing the
25-plug source count. Both copies pass validation with the deployed toolchain.

The accepted GPIOs, metering calibration, credentials and `ALWAYS_OFF` relay
behavior were preserved. The uptime unit was corrected from `minutes` to `min`
without changing its values. The final firmware is 476112 bytes, below 512 KiB.
API reconnect and version 2026.9.1 were verified; both API and MQTT relay states
remained OFF, and metering was available. No test relay toggle was sent.

HA uses `switch.s6`; existing secondary MQTT exposure uses `switch.s6_mqtt`.
Twenty-five entity names/IDs were normalized and seven existing automation
references plus the Lovelace item were migrated. Twenty-two registry identities
were retained. The newer MQTT implementation changes signal/uptime/version
unique IDs; those three secondary diagnostics use new records while existing
recorder history remains untouched. Retained discovery topics were migrated,
and the invalid old uptime registry record was removed. The firmware's legacy
component names and MQTT state/command topic prefix intentionally remain stable.

HA configuration validation passed. Reloading only the seven changed automation
IDs preserved unrelated active motion-off timers. Refreshing HA's Dashboard
coordinator resolved its stale node-name cache before final API verification.

### 2026-10-11 — KMC voltage reference adjustment

All three KMC 30608 samples received separate voltage-only multipliers against
the owner's Victron reference. An initial nominal-122 V adjustment was refined
against concurrent live readings using the mean of the two reference phases;
the outlet phase assignments remain unknown. The firmware's current, power and
energy calculations were preserved and remain uncalibrated; the diagnostic
text states this partial scope. The update preserved device/component identities
and all GPIO behavior. Each unit was updated in sequence, and all nine recorded
relay states were restored afterward. Active sources and private workbench
copies were synchronized and the deployed Dashboard validated all three files.

See the [KMC voltage adjustment](kmc-30608.md#voltage-only-reference-adjustment)
for individual factors, the measurement basis and limits. This maintenance
does not add conversions or change the outstanding physical acceptance gates.


### 2026-10-11 — Switch06 and Switch07 naming

The existing s6 device was subsequently renamed **Switch06** in HA, including
its native and secondary MQTT entity names, both device records and the
ESPHome entry title. Its saved source is now `switch06.yaml` in HA and the
Dashboard, with only the friendly-name metadata changed; native node name,
component identities, MQTT topics and electrical configuration remain stable.
Seven active HA automation sources follow the new entity IDs without changing
control policy or load estimates.

The corrected standalone YM-WS-1 sample became **Switch07**, and its former
logical role moved to outlet 2 of the third KMC 30608. Existing role consumers
follow that KMC output; the other KMC outputs are unchanged. Its saved source
is now `switch07.yaml`, retaining the corrected GPIO1/GPIO14/GPIO13 profile.
The two numbered controls appear together after Switch05 in Lovelace.

This was an HA registry/reference and saved-source migration: no firmware was
uploaded, no device was restarted and no test relay command was sent. Running
firmware friendly names may still reflect the earlier deployment; HA names
are explicit registry overrides. Both saved sources validate with ESPHome
2026.9.1, and secret values and the total source count are unchanged.


### 2026-10-11 — Ping01: fourth AWP02L-N, ordinary conversion successful

This sample completed ordinary Tuya-Convert, unlike the three earlier AWP02L-N
PSK `02` failures. VTRUST-FLASH 1.5 reported an ESP8266 with 1 MiB flash, DOUT,
40 MHz. A private 1 MiB post-loader flash backup was saved; this is not a pristine
factory image. An input-only GPIO13 probe preceded the final relay firmware.

The final ESPHome 2026.9.1 image is 440480 bytes. GPIO13 is the active-low pull-up
button, GPIO15 the active-high relay, and GPIO2 the inverted relay indicator;
GPIO0 is unused. Encrypted API and OTA, ON/OFF control, restart from ON to OFF,
and the owner's physical button/load/indicator test passed. A controlled mains
cycle remains untested. This raises the Tuya-conversion count to 22 and the
per-unit physical button/load acceptance count to 16.

HA uses Ping01. Its exact former LocalTuya device was removed, with all 31
remaining configurations preserved. No active dashboard, automation or script
reference used the old entity. The source is saved as `ping01.yaml` in both HA
`/config/esphome` and Dashboard `/config`, using private per-device secrets.

### 2026-10-11 — Ping02: existing Tasmota MJ_XS-SSA01 migration

The existing Tasmota 6.7.1 device was matched by physical MAC and its stored
MJ_XS-SSA01 template. A private 4096-byte settings backup was saved. The template
maps GPIO13 to the button, GPIO15 to the relay and inverted GPIO12 to the LED.
The raw 440480-byte ESPHome image fitted the conservative 446464-byte OTA space
calculated from this Tasmota version's uploader; no minimal-image or gzip step
was used. Direct upload succeeded. This is a separate Tasmota migration and is
not counted as another Tuya conversion.

Encrypted API, native ON/OFF control, restart from ON to OFF, HA control and the
owner's physical button/load/indicator test passed. An earlier report of relay
clicks without load power did not recur in this test; this does not establish a
hardware diagnosis or repair. A controlled mains-cycle check remains pending.

HA uses Ping02. Only the old device's three MQTT entities and three retained
Home Assistant discovery topics were retired. No matching LocalTuya device
existed. The shared MQTT integration and unrelated devices were preserved.
Two obsolete customization entries were removed. Both sources are available as
`ping01.yaml` and `ping02.yaml` in HA and Dashboard; the managed plug-source count is
now 27 (32 device YAML files including five non-plug devices). Lovelace ends with Switch07, Ping01, Ping02.

Migration references: [ESPHome Tasmota migration](https://esphome.io/guides/migrate_sonoff_tasmota/)
and the [Tasmota 6.7.1 uploader source](https://github.com/arendst/Tasmota/blob/v6.7.1/sonoff/xdrv_01_webserver.ino).


### 2026-10-11 — Unidentified square outlet: initial Switch08 reservation

A white-and-silver square outlet with no readable manufacturer/model/FCC marking
was selected for Switch08. Two bounded ordinary Tuya-Convert sessions produced
no target association, no intermediate loader and no ESPHome transfer. The first
started while the device was in slow-blinking mode; the second began after the
owner switched it to fast blinking. Only the companion phone associated.

Its protected `SmartTouch_…` setup AP was subsequently identified by a controlled
power interruption: fresh beacons stopped and the AP uptime reset after power
returned. An isolated station connected and verified the gateway's physical MAC.
The checked TCP service ports and UDP discovery ports did not expose a recognized
provisioning or firmware-update interface. This is not proof that all OTA methods
are impossible, nor does the MAC alone identify the chip or GPIO mapping.

A unique-key GPIO-neutral ESPHome image is prepared privately but uninstalled.
No HA entity or live Dashboard source was created. The factory firmware remains
in place, both workbench sessions were cleaned up, and the Wi-Fi radio returned
to managed mode. Continue after identifying the original app or board/module;
do not count this unit among successful conversions. The owner subsequently
deferred Switch08; no further probing or flashing is scheduled.

The owner later reassigned the Switch08 name to the second CV01 below. The
unidentified square outlet remains deferred and unflashed, without a reserved
number or HA entity.

### Twenty-third conversion: second SUPERNIGHT CV01

The second owner-confirmed CV01 accepted ordinary Tuya-Convert. Its stock
version was 1.0.4 and its loader reported 1 MiB DOUT flash at 40 MHz. A distinct
credential set was used. After the neutral firmware and an owner-performed
power cycle, the encrypted API was available. The input-only probe confirmed
both button inputs, with the ADC button on the left in the owner's orientation.

At the owner's explicit request, the previous CV01 hardware profile was reused
without repeated physical load or controlled mains-cycle tests. Both native
relay controls and a software restart from both ON to both OFF passed.
The second sample is counted as converted, but not as another physically
verified button/load acceptance. See [the profile record](supernight-cv01.md#second-sample-profile-reuse).

HA adopted the second unit as Switch08 and Switch09. Its complete source is
saved separately as `switch08-switch09.yaml` in HA and ESPHome Dashboard,
with distinct named secrets. No existing device matched its identity, so no
LocalTuya or MQTT records were removed.


### Twenty-fourth conversion: sixth WP5, Switch10

The owner confirmed an unloaded WP5 with no other pairing targets. Ordinary
Tuya-Convert reached the intermediate loader from stock version 1.0.1; the
loader reported 1 MiB QIO flash at 40 MHz. The accepted WP5 profile was installed
directly as ESPHome 2026.9.1, using distinct credentials: GPIO13 active-low button,
GPIO15 relay and inverted GPIO2 indicator. GPIO0 remains unassigned, matching
the previous single-indicator configuration. This does not establish compatibility
with the different Gosund WP5 pinout.

The 440352-byte full image installed successfully. Its encrypted API identity,
independent native and HA on/off state control, and software restart from ON
to OFF passed. The existing request to reuse known profiles without repeating
manual tests was carried forward. This unit has no separate physical button/load,
indicator or controlled mains-cycle acceptance; the physical verification count
therefore remains sixteen.

HA uses `switch.switch10` with device and friendly name Switch10. The complete
source is saved as `switch10.yaml` in HA and ESPHome Dashboard, with distinct
named secrets and the Dashboard's two-worker compile limit. Lovelace places it
after Switch09. No preexisting HA identity matched this unit, so no old entities
were removed. The final relay state is OFF and the workbench AP was cleaned up.


### Twenty-fifth conversion: XS-SSA05, Switch11

This sample accepted ordinary Tuya-Convert from stock firmware 1.0.1, despite
the published model entry describing serial installation. The loader reported
1 MiB QIO flash at 40 MHz. A distinct-key neutral ESPHome 2026.9.1 image installed
in 7397 ms, followed by encrypted OTA updates. The final image is 444352 bytes.

The relay is GPIO12 and the active-low button is GPIO13. Output tests established
active-low GPIO0 red, GPIO15 bright blue and GPIO4 faint blue channels. With both
blue channels driven high the glow disappeared. The final profile holds GPIO4
off, assigns GPIO15 to connection/warning status and makes GPIO0 follow the relay.
The owner confirmed that the physical button switches both the test load and red
indicator on and off, with relay clicks. Native and HA state control and software
restart from ON to OFF passed. Controlled mains-cycle acceptance remains pending.

Switch11 exposes voltage, current, power and energy since boot through the
HLW8012 interface, with a Not calibrated diagnostic. The initial voltage scale
was visibly inaccurate; quantitative readings need reference calibration.
The complete source is saved as switch11.yaml in HA and ESPHome Dashboard, with
separate secrets and the two-worker compile limit. Lovelace places Switch11
after Switch10. No existing HA identity matched this plug. Final relay state: OFF.
See [the profile and calibration notes](xs-ssa05.md).


### Twenty-sixth conversion: second XS-SSA05, Switch12

At the owner's request, this unit reuses the accepted first XS-SSA05 profile
without repeating button, load, indicator or mains-cycle acceptance. The owner
confirmed that the outlet was unloaded and in fast pairing mode. The complete
ESPHome 2026.9.1 relay firmware was installed directly through ordinary
Tuya-Convert, without a diagnostic firmware stage. Distinct private credentials
were generated, and the encrypted API matched the loader identity.

GPIO12 switches the relay; GPIO13 is the active-low button. Active-low GPIO0
follows the relay, GPIO15 provides connection status, and GPIO4 stays off. The
HLW8012 voltage/current/power/energy readings remain explicitly uncalibrated.
Native and HA controls and software restart to OFF passed. The source is saved
and validated in HA and ESPHome Dashboard as `switch12.yaml`, with two compile
workers. Lovelace places Switch12 after Switch11. Final relay state: OFF.


### Twenty-seventh conversion: third XS-SSA05, Switch15

The owner requested Switch15 as the next number and the same profile-reuse
workflow. The final ESPHome 2026.9.1 firmware was installed directly through
ordinary Tuya-Convert with distinct private credentials. The encrypted native
API matched the new loader identity. The accepted GPIO12 relay, GPIO13 button,
GPIO0 red, GPIO15 status and disabled GPIO4 indicator profile is unchanged.

Repeated physical button/load/indicator and mains-cycle acceptance was waived.
Native and HA control and software restart to OFF passed. The HLW8012 meter is
exposed but remains uncalibrated. Both complete deployed source copies validate
as `switch15.yaml`, with two compile workers. Lovelace places Switch15 after
Switch12. Final relay state: OFF.


### Twenty-eighth conversion: fourth XS-SSA05, Switch16

The owner requested the next identical conversion as Switch16, reusing the
accepted GPIO12/GPIO13/GPIO0/GPIO15/GPIO4 profile without repeated physical
checks. Ordinary Tuya-Convert installed the final ESPHome 2026.9.1 image
directly. A spare, previously disconnected workbench Wi-Fi adapter supplied the
associated AP client for this session; no phone reconnection was needed.
It was disconnected and restored after the session.

Encrypted API identity, native and HA controls and software restart to OFF
passed. Meter readings remain uncalibrated. Complete `switch16.yaml` source
copies are saved and validated in HA and ESPHome Dashboard with two compile
workers. Lovelace places Switch16 after Switch15. Final relay state: OFF.
No new physical button/load/indicator or mains-cycle acceptance is claimed.


### Twenty-ninth conversion: fourth KMC 30608, Switch17–Switch19

The owner identified the same model, confirmed all four physical outlets were
unloaded, and requested the next three numbered controls. The final ESPHome
2026.9.1 image was installed directly by ordinary Tuya-Convert with distinct
credentials, reusing the accepted profile without diagnostic firmware or
repeated physical acceptance. Encrypted API identity matched the new loader.

Embossed outlets 1, 2 and 3 use GPIO15, GPIO13 and GPIO14 and are named Switch17,
Switch18 and Switch19. The GPIO16 button turns all relays off when any is on,
or all on when all are off. GPIO1 provides inverted connection status. The
fourth outlet remains always on and has no relay entity. Existing unresolved
per-outlet LED behavior was not re-investigated.

Independent native and HA controls and software restart from all ON to all
OFF passed. Shared HLW8012 voltage/current/power/energy remain uncalibrated;
no other unit's calibration factors were copied. Both complete source copies
are persisted and validated as `kmc-switch17-19.yaml`, with two compile workers.
Lovelace places Switch17, Switch18 and Switch19 after Switch16. All relays end OFF.


### LSPA11, prospective Switch20: authentication blocked

The owner reports one button, two AC outlets with individual indicators and two
USB ports, and confirmed every output unloaded. The unit joined the isolated
workbench network but made repeated PSK identity `02` handshakes ending in
`DECRYPTION_FAILED_OR_BAD_RECORD_MAC`. No VTRUST loader started and no replacement
firmware was transferred. A prepared GPIO-neutral ESP8266 image was not installed;
the actual chip family and GPIO assignments remain unconfirmed.

The current upstream CloudCutter device index has no exact LSPA11 profile.
Profiles for similarly named LSPA models are not evidence of compatibility.
Continuation requires the stock main-module firmware version and a matching
profile, or identification of the actual radio module. The two AC outlets' and
USB ports' independent control remains unknown. Switch20 is reserved only; no
HA entity, dashboard control or deployed ESPHome source was created. This attempt
does not increase the successful conversion or physical-acceptance counts.
