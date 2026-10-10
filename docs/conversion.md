# Convert one plug

## Build the first image

Use [the workbench setup](workbench.md), generate private secrets, and review the
local copy of `tuya-plug.yaml`. Each device adds its MAC suffix to its ESPHome
hostname so the same initial image can be used for a batch.

Reusing that image also shares its API/OTA key across those units. For separate
keys, generate and stage a separate image before converting each stock unit.
Renaming a YAML file does not rotate credentials. Preserve deployed keys and
check the installed ESPHome version's key-rotation limitations before changing them.
Keep per-unit keys under unique secret names, or in separate private configuration
directories with their own `secrets.yaml`; retain those mappings for later uploads.

```sh
/opt/tuya-workbench/bin/esphome config tuya-plug.yaml
/opt/tuya-workbench/bin/esphome compile tuya-plug.yaml
python3 scripts/stage-firmware.py \
  /opt/tuya-workbench/esphome/.esphome/build/tuya-plug/.pioenvs/tuya-plug/firmware.bin
```

Tuya-Convert's first custom image must include the ESP8266 bootloader, begin with
the ESP image magic byte, and be no larger than **524,288 bytes**. The staging
script enforces the size/header constraints; it cannot identify a physical chip
or guarantee that a binary matches a device. If this build exceeds the limit,
remove optional diagnostics and rebuild. Do not feed an ESP32 image, ELF file,
or a larger binary to this path. See the
[upstream requirements](https://github.com/ct-Open-Source/tuya-convert#flash-third-party-firmware).

The compiled binary contains private Wi-Fi and API credentials. It belongs only
on the private workbench, never in Git or a public GitHub release.

The template requires encrypted subsequent ESPHome OTA uploads using the API key.
Use the pinned, current uploader and preserve that key in the device's local YAML.
This does not encrypt the legacy Tuya-Convert transfer itself. See ESPHome's
[OTA encryption documentation](https://esphome.io/components/ota/esphome/#encryption).

## Pair and flash

1. Keep other unconverted plugs powered off. Put one unloaded plug near the host.
2. Start a persistent terminal: `tmux new -s convert`.
3. Run `/opt/tuya-workbench/bin/tuya-convert` and accept the upstream risk notice
   if this is the first session.
4. Connect a secondary phone/tablet to the station's `vtrust-flash` Wi-Fi network.
   Keep it connected despite the lack of Internet. The pinned upstream AP is
   open; do not confuse it with a Tuya/SmartLife device's own AP.
5. Put the plug into **fast-blinking smartconfig mode**, following its button
   behavior. Slow-blinking AP mode is a different workflow.
6. Press Enter only when the phone and the single target plug are ready.
7. After the intermediate loader appears, inspect the reported device/flash
   information. The original-firmware download is deliberately skipped.
8. Select `esphome-initial.bin` and confirm the write. Let the unit reboot and join
   its configured home Wi-Fi.
9. Check its DHCP lease and ESPHome API connection. End the conversion session
   before using the radio for ordinary Wi-Fi again.

Nothing in setup or the launcher chooses a firmware automatically. The selected
file remains visible at the upstream confirmation prompt. Logs and device
metadata go to `/opt/tuya-workbench/logs/<timestamp>/`; no stock dump is requested.

## Finish in Home Assistant

Add the discovered ESPHome device under Settings → Devices & services, supplying
its local API encryption key. If discovery is unavailable, use its DHCP address.
Only diagnostic entities exist at this stage. Continue with [GPIO identification](gpio.md)
before expecting a controllable plug entity or exposing it through Matter.

For a subsequent device-specific image, keep a separate local YAML named for that
unit and run ESPHome `upload <file>.yaml --device <address>`. Preserve its local
credentials and stable identity. Return to Tuya-Convert only for a still-stock unit.
