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
- Wi-Fi credentials were imported privately from the existing ESPHome setup;
  new initial API/OTA/fallback credentials were generated on the workbench.
- The compatibility container built successfully. A real TLS 1.2 handshake with
  a non-UTF-8 PSK identity passed using the pinned Python and sslpsk3 versions.
- The reference radio reached `AP-ENABLED` in the isolated container. DHCP, DNS,
  HTTP, MQTT, TLS-PSK and Tuya discovery listeners started while wired SSH stayed
  reachable. The launcher reached its pre-pairing prompt without starting a flash.

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

No physical plug in this batch has yet been converted, mapped, load-tested or
commissioned into Google Home/Alexa. Existing bridge fabrics and household entity
selection were not reset or published. A functioning server process is not a
completed end-to-end acceptance test. Track those gates in [ROADMAP.md](../ROADMAP.md).
