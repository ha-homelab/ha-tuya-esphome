# ESPHome radio failover bench

One virtual relay, controlled through a wired ESP-NOW gateway, direct Wi-Fi, or
optional BLE. All routes use the same authenticated command and state reply.
The controller chooses the first route that confirms each phase. The gateway
uses the MC2-D WROVER-IE/W5500 pinout from the [Radio Hub ESP-NOW
profile](https://github.com/ha-homelab/ha-radio-hub/pull/38). Use a separate
bench harness. The gateway firmware replaces the board's entire application
and is unsuitable for a working Radio Hub installation.

| Route | Path | Exercises |
| --- | --- | --- |
| ESP-NOW | Controller → Ethernet API → gateway → ESP-NOW → satellite | Radio path without gateway Wi-Fi association |
| Wi-Fi | Controller → ESPHome API → satellite | Direct path when the gateway is absent |
| BLE (optional) | Controller's Bluetooth adapter → satellite GATT | Short-range recovery without either IP route |

Use `gateway.yaml` on a spare MC2-D-compatible ESP32/W5500 harness and
`satellite.yaml`, `satellite-ble.yaml` or `satellite-no-ap.yaml` on an
ESP32-C3-DevKitM-1. The last profile uses a fixed ESP-NOW channel and BLE
without Wi-Fi association, a direct IP route or ESPHome OTA. Use USB for
updates and leave `[satellite]` out of the controller TOML for this profile. The
satellite has a software state indicator and no GPIO output. The BLE route
uses the controller host's Bluetooth radio. Support for a remote BLE proxy
or a Home Assistant logical entity requires additional integration.

## Prepare and run

1. Use an isolated bench LAN with a 2.4 GHz AP fixed to the gateway ESP-NOW
   channel (default 6). Keep station MAC addresses distinct. Use the ESP32's
   **Wi-Fi station MAC** for ESP-NOW and each API's **LAN address** for the
   controller. The gateway's Ethernet MAC is a separate identity.
2. Copy the bench directory outside the checkout. Copy `secrets.example.yaml`
   to `secrets.yaml` there and replace **every** placeholder. Generate a unique
   command key (32 random bytes encoded as 64 hex digits), two independent API
   keys (each 32 random bytes in base64) and separate OTA passwords. The
   public example command key is refused by both controller and satellite.
3. With ESPHome `2026.10.2`, validate and compile the chosen two YAMLs. Flash
   only the isolated, correctly identified bench boards. Confirm Ethernet
   on the gateway and Wi-Fi on the satellite. Use a connected antenna for
   a module with an external antenna connector.
4. Store the following controller TOML outside the checkout in a file readable
   only by the operator. Enter the same command key and Native API keys from
   the bench secrets. For BLE add `ble_address` at the top level, using the
   device address on Linux or the CoreBluetooth device UUID on macOS. Use
   `aioesphomeapi==46.12.0` and, for BLE, `bleak==3.0.2`.

```toml
command_key = "REPLACE_WITH_BENCH_COMMAND_KEY_HEX"
# ble_address = "REPLACE_WITH_BLE_ADDRESS_OR_PLATFORM_UUID"

[gateway]
host = "failover-lab-gateway.local"
psk = "REPLACE_WITH_GATEWAY_NATIVE_API_KEY"

[satellite]
host = "failover-lab-satellite.local"
psk = "REPLACE_WITH_SATELLITE_NATIVE_API_KEY"
```

```sh
python run_pilot.py --config /path/to/private-pilot.toml state
python run_pilot.py --config /path/to/private-pilot.toml on
python run_pilot.py --config /path/to/private-pilot.toml off
```

The CLI reports the route of the snapshot and final confirmation, plus each
attempt's outcome. It handles one operation per run. A persistent caller of
`Controller` also keeps the temporary route cooldown across operations.
Use one controller per endpoint. When a SET confirmation is lost, query
`state` to reconcile before issuing another command.

## What to verify on the bench

- Test ordinary ON and OFF. With the satellite still associated, block only
  its direct IP route and verify ESP-NOW still works. Recover that route, then
  unplug the gateway Ethernet and verify direct Wi-Fi takes over.
- With the BLE profile and host in range, disable both IP routes and check
  that a BLE command reports an authenticated result. Measure connect time,
  state confirmation time and coexistence under traffic. A failed BLE attempt
  can mean the 1.5-second route budget is too short for connection setup.
  Verify the entire 35-byte write and read using a negotiated ATT MTU of at
  least 38 or GATT long transfers.
- Test AP power loss, boot without an AP, reassociation, and the AP changing
  channels separately. The receiver's ESP-NOW channel follows associated
  Wi-Fi. While reconnecting it can scan off-channel. IP path loss coverage
  does not establish AP-loss coverage. For an installation without eero,
  test `satellite-no-ap.yaml` with the AP absent from cold boot and confirm
  ESP-NOW, BLE fallback and USB recovery before any installation.
- Run for longer than the stock API and Wi-Fi reboot timers. The bench
  disables both disconnect-induced timers on the satellite. Record uptime,
  link latency, successful delivery and heap on the actual boards.
- Only after bench acceptance, port to one spare outlet. Confirm flash and
  rollback fit, physical button behavior, physical relay/load readback,
  restored connectivity and actual coverage at its intended location.

## Wire contract and limits

Frames are 35 bytes: version u8, type u8, request ID u64, lease token u64,
state u8 (network byte order), followed by a 16-byte HMAC-SHA256 tag. GET
requests a snapshot and a random, five-second device-side token. SET is an
absolute ON/OFF request bound to that token. Only an authenticated RESULT
matching the request, token and requested state confirms the operation. The
same SET can arrive on a different route after its reply is lost and the
endpoint returns its cached result without applying it again. Expiry, a new
snapshot, restart or local override invalidates older commands. A local
physical control must call `local_state()` in any real relay integration.

The protocol authenticates commands and replies. Radio traffic is readable
and packet floods can cause denial of service. A replayed GET may replace a
lease, causing the newer SET to be rejected. The old SET still cannot execute
with a different token. Do not use this bench for critical loads. The current
RESULT confirms the virtual state only. It cannot confirm relay contacts or
load power.

Stable ESPHome `2026.10.2` targets ESP32 for native ESP-NOW. ESP8266/ESP8285
support appears in the `2026.11` prerelease. Existing 1 MB plugs need separate
RAM, image-size, forward/rollback OTA and radio qualification. They have no
Bluetooth radio. Keep the existing fleet firmware pins during the bench.
