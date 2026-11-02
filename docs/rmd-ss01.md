# RMD-SS01S00A / TYWE3S wall switch

Status: relay firmware installed. Encrypted API ON/OFF control, restart to OFF, and subsequent native OTA passed. The owner confirmed the physical button, relay and indicator operate together. Home Assistant and Lovelace migration are complete; the voice-control allowlist will take effect at the next HA restart.

## Hardware identification

The tested unit has a TYWE3S module (ESP8266), a label reading `RMD-SS01S00A`, and a carrier marked `SS01_LED V05 2019-01-04`. Its bootloader reports 2 MiB of flash. This is a different board from the [SWP1-PW2-V5](swp1-pw2-v5.md); do not copy that board’s pin assignments.

The mapping was selected from the TreatLife SS01S entry in [Tasmota’s templates](https://github.com/arendst/Tasmota/blob/development/TEMPLATES.md):

- GPIO12: relay, active high; always OFF after startup.
- GPIO13: button, inverted with an internal pull-up.
- GPIO4: relay indicator, active high.
- GPIO5: network indicator, inverted.

The relay/button/indicator behavior was subsequently accepted by the owner on this sample. No controlled mains-cycle or connected-load test was performed after the final firmware.

## Observed conversion path

1. UART boot messages confirmed download mode. Intermittent probe contact prevented a reliable transfer; soldering subsequently damaged a UART pad. Further serial recovery was abandoned for this sample.
2. Legacy Tuya-Convert successfully installed a GPIO-neutral ESPHome 2026.9.1 image. Encrypted API identity was verified after startup.
3. Native ESPHome OTA accepted the connection but failed on the first staging-sector erase. Compressed transfer failed at `0x001AF000`; uncompressed transfer failed at `0x00192000`.
4. Software restart and a full power cycle did not resolve the failure. This does not establish whether the cause is flash geometry, protection, or hardware damage.
5. A conservative 1 MiB-layout relay image was compiled and installed through the ESPHome captive portal. The endpoint returned HTTP 200 and `Update Successful!`; the device then reported the new build and relay over its encrypted API.
6. API ON/OFF and restart-from-ON to OFF passed. A subsequent **native encrypted OTA** of the same image also succeeded. This confirms future OTA for this tested image and layout, not a general repair of every flash-sector failure.

## Recovery through the captive portal

For this sample, a temporary isolated WPA2 AP admitted only the target MAC and did not offer DHCP. The device started its password-protected fallback AP; a second radio connected to it. The portal’s reported MAC and hostname were checked before uploading. The temporary AP was stopped and both radios returned to the host afterward. This is an advanced recovery technique, not a required step for normal OTA.

The ESPHome 2026.9.1 ESP8266 backend places a known-size native OTA image before the filesystem boundary. Its web uploader starts an unknown-size upload instead. In this implementation, that can put the temporary image immediately after the running sketch, avoiding the high addresses that failed on this unit.

Changing the *new* image’s board setting alone does not move the staging address used by the *currently running* firmware. The uploader and existing image determine that address. The successful upload was followed by a reboot and encrypted API readback. The owner subsequently confirmed the button, relay and indicator work together.

See the [ESPHome ESP8266 OTA backend](https://github.com/esphome/esphome/blob/2026.9.1/esphome/components/ota/ota_backend_esp8266.cpp) and [web uploader](https://github.com/esphome/esphome/blob/2026.9.1/esphome/components/web_server/ota/ota_web_server.cpp).

## Acceptance and migration

The relay, button and indicator were checked; startup-OFF was verified through a software restart. A relay replacement must use switch actions and a switch-compatible dashboard card, not brightness controls inherited from a dimmer.

The new name is **Living Fireplace**, entity `switch.living_fireplace`. The old dimmer was `light.living_wall_dimmer_l`, displayed as **Living room fireplace** on the dashboard. A separate `switch.fireplace_switch` is a different device and must remain untouched.

The completed migration replaced the light card with a switch button and updated the dashboard’s automatic-list filter. The old LocalTuya device was removed only after these references were replaced; unrelated entity identities and LocalTuya configurations were verified unchanged. Scheduled shutdown uses `switch.turn_off`; household shutdown keeps `homeassistant.turn_off` for its mixed-domain list. The YAML voice-control allowlist is updated too; this integration reads that list at startup, so a full Home Assistant restart is needed before its in-memory allowlist changes. This conversion does not restart Home Assistant.

Reviewed source changes: [morning shutdown](https://github.com/ha-homelab/automations/pull/53), [household shutdown](https://github.com/ha-homelab/scripts/pull/27). Changes in pull requests are not yet part of their repositories’ primary branches.

Keep firmware binaries, Wi-Fi credentials, encryption keys, packet captures, and raw diagnostics private. The opened mains switch must never be connected to mains while UART or bench wiring is attached. Closed-enclosure mains testing and low-voltage bench work are separate stages.
