# Tuya plugs to ESPHome

An English-language field guide and reproducible workbench for converting old
Tuya Wi-Fi plugs to ESPHome, then exposing their Home Assistant
entities through an **existing Home Assistant Matter Hub** to Google Home and
Amazon Alexa.

The current batch consists of old, unboxed plugs reported by the owner to use
ESP8266/“ESP-01” hardware. Similar-looking plugs were converted previously.
The first unit reports 1 MB flash and is marked **XS-SSA01**. Its observed button
and LED match the GPIO15-relay variant in the official Tasmota catalog. Identical
markings and similar enclosures can still hide different board revisions.

**First unit physically verified:** the XS-SSA01 profile uses GPIO15 for the relay,
GPIO13 for the button and inverted GPIO12 for the indicator. The operator confirmed
mechanical clicks and actual load switching in both directions. The earlier GPIO12
relay candidate drove only the LED; [the investigation](https://github.com/ha-homelab/ha-tuya-esphome/issues/1)
records that correction. See [the deployment record](docs/deployment-record.md) for
restart and ecosystem acceptance results.

**Second successful conversion:** a WP5 replacement also passed the physical
button/load test with GPIO13 button and GPIO15 relay. The similar Gosund WP5 map
is different; use the [variant identification procedure](docs/gpio.md) before
applying either profile. A separate YM-WS-1 attempt stopped at pairing without
writing firmware.

A later AWP02L-N attempt reached the conversion Wi-Fi but presented patched
Tuya PSK identity version `02`. It never reached the intermediate loader and
received no firmware. Its existing HA and client bindings were retained.
Follow-up research found an experimental ESP8266 CloudCutter port. One experimental
packet was sent to the identified unit in AP mode; its connection dropped, but
replacement-key authentication and conversion remain unverified. See the
[AWP02L-N experimental procedure](docs/awp02l-n-psk02.md).

Eight plugs have now been converted: two XS-SSA01 units, three WP5 units, one
KMC 30137, one YM-WS-1 and one JH-G01U. Seven passed their own physical button/load test;
the first two WP5 units also passed their independent red-indicator check.
Per-unit HA software-restart results are recorded in the deployment record.
For the latest WP5, the operator chose the existing profile and waived repeated
physical and restart tests. The first two converted plugs passed actual load
switching from Google Home and Amazon Alexa through the existing Matter Hub.
The operator deferred later controller checks. The original controller fabrics
were preserved when Alexa was added. See the deployment record for migration
results and remaining checks.

The later YM-WS-1 reached the ordinary conversion loader and now runs ESPHome.
Its GPIO15 relay, GPIO13 button and inverted GPIO12 indicator passed the
operator's load test. This success is recorded separately from the earlier
unflashed pairing attempt; the marking alone still does not select a variant.

The JH-G01U uses GPIO4 for its verified relay and GPIO5 for its verified button.
Its GPIO12 indicator initially ran opposite to the load. Active-low polarity was
then installed through encrypted OTA and the API checked again; the corrected
indicator has not yet been visually rechecked. See [GPIO details](docs/gpio.md).

```mermaid
flowchart LR
  T[Old Tuya ESP8266 plug] -->|one-time tuya-convert| E[ESPHome over Wi-Fi]
  E -->|encrypted native API| H[Home Assistant]
  H -->|selected entities| B[Existing Matter Hub on NAS worker]
  B -->|Matter over LAN| G[Google Home controller]
  B -->|Matter over LAN| A[Amazon Echo controller]
```

ESPHome does not turn an ESP8266 plug into a native Matter device. Matter Hub
provides that bridge. Home Assistant's separate **Matter Server** manages Matter
devices for Home Assistant; it is not the component exporting arbitrary ESPHome
entities.

## Start here

1. [Understand the hardware and batch policy](docs/hardware.md).
2. [Prepare the Linux workbench](docs/workbench.md).
3. [Build and convert one plug](docs/conversion.md).
4. [Identify its GPIOs and finish the ESPHome configuration](docs/gpio.md).
5. [Expose selected entities to Google Home and Alexa](docs/matter.md).
6. Use [troubleshooting](docs/troubleshooting.md) and record progress in the
   [task list](ROADMAP.md).

## Project policy

- Convert one disconnected-load plug at a time.
- Do not initialize this batch in Tuya/Smart Life or install vendor updates first.
- The owner explicitly chose **no factory-firmware backups** and accepts retiring
  unsuccessful units rather than spending time on serial recovery. The container
  disables the upstream download step; session logs and metadata are still local.
- Start unidentified variants with a GPIO-neutral ESPHome image. Record an
  operator's explicit choice to reuse a same-model profile without repeated tests.
  A working Wi-Fi/API connection and a functional mains relay are different milestones.
- Keep Wi-Fi settings, API keys, actual addresses, device identifiers, logs,
  compiled firmware and Matter commissioning data out of this repository.

## What is included

- A pinned `tuya-convert` source revision and Python 3.11 container recipe.
- A TLS-PSK compatibility patch and executable binary-identity handshake check.
- An isolated-radio launcher that preserves the Ethernet management connection.
- A minimal ESPHome 2026.9.1 configuration targeting `esp01_1m`.
- Local secret generation, binary size validation, and operating procedures.
- An anonymized [deployment record](docs/deployment-record.md).

Repository provisioning is managed by
[terraform-github-ha-homelab](https://github.com/4alvit/terraform-github-ha-homelab).
See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

## Upstream projects

[Tuya-Convert](https://github.com/ct-Open-Source/tuya-convert),
[ESPHome](https://esphome.io/),
[Home Assistant](https://www.home-assistant.io/), and
[RiDDiX Home Assistant Matter Hub](https://github.com/RiDDiX/home-assistant-matter-hub)
provide the underlying tools. This repository is an independent integration
project and does not claim that every Tuya firmware or plug is compatible.
