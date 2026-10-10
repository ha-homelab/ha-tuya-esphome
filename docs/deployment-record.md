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
  power to a load that works directly from the wall. GPIO12 remains unverified
  as a relay output. Physical output/restart checks and Matter export are blocked
  until a correct mapping is established; no completed plug conversion is claimed.
- Removing the first conversion container left the Broadcom radio inaccessible.
  Reloading its driver restored it. An explicit numeric-PHY return before
  container removal then passed a live namespace round-trip check; the launcher
  now performs that return during cleanup.

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
OTA. Its initial output test failed; physical relay mapping and Google Home/Alexa
control remain pending. No successful load test is claimed. Existing bridge fabrics and household entity
selection were not reset or published. A functioning server process is not a
completed end-to-end acceptance test. Track those gates in [ROADMAP.md](../ROADMAP.md).
