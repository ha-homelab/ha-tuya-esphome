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
the new firmware and an off switch state. Actual load/button checks are pending;
software state alone does not verify the relay contacts. The WP5 has not been
exported through Matter. The failed pairing attempt and this replacement retain
separate private inventory records.

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

The first plug runs ESPHome, is adopted in Home Assistant and accepts encrypted
OTA. Its initial GPIO12 output test failed; a model-specific GPIO15 profile is now
installed and has passed a physical load/button test and an HA-controlled
software-restart check. Google Home app control also passed. Physical power-cycle,
Alexa commissioning/control and the full button-to-controller round trip remain
pending. Existing bridge fabrics were preserved, and household entity
identifiers were not published. A functioning server process is not a completed
end-to-end acceptance test. Track those gates in [ROADMAP.md](../ROADMAP.md).
