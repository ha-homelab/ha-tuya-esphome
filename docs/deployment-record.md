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

Seven converted plugs passed per-unit physical button/load checks. Six also have
HA software-restart evidence; the seventh conversion's restart began already off,
so it does not prove on-to-off restoration. The eighth has no separate restart
test and its corrected indicator has not been visually rechecked.
The sixth uses a previously verified WP5 profile with repeated physical
and restart checks explicitly waived by the operator; its transfer and encrypted
API were verified separately. Google Home and Alexa app control passed on the
first two converted plugs. Later controller checks were deferred. Physical
power-cycle tests and the full button-to-controller round trip remain pending.
Existing bridge fabrics were preserved, and household entity identifiers were
not published. A functioning server process is not a completed end-to-end
acceptance test. Track those gates in [ROADMAP.md](../ROADMAP.md).
