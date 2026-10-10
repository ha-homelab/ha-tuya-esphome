# Tasmota SP20 to ESPHome with metering continuity

This procedure applies to an ESP8266 TECKIN SP20 whose **live** Tasmota template uses the standard layout below. SP20 variants exist; a matching case or model name alone is insufficient.

- Relay GPIO4; active-low pull-up button GPIO13.
- Active-low red LED GPIO0 and blue LED GPIO2.
- BL0937/HJL metering: CF GPIO5, CF1 GPIO14, inverted SEL GPIO12.
- The example uses the blue LED for relay state and red LED for ESPHome status. Confirm the desired LED policy; it is independent of calibration.

Read `Status 0`, `Template`, `Module`, `PowerOnState`, `PowerCal`, `VoltageCal`, `CurrentCal`, rules and protection settings before replacing firmware. Save these configuration facts privately. This is not a firmware backup. Do not publish private status responses, device addresses, credentials, retained MQTT topics or operational entity names.

Use the [metered profile](../examples/teckin-sp20-metered.yaml) together with
[its counter helper](../examples/energy_state.h).

## Transfer the actual calibration

For the Tasmota 13.4.0 **HJL/BL0937** driver, calculate pulse multipliers from the existing calibration:

```text
power_W_per_Hz = 1362 * PowerCal / 10000000
voltage_V_per_Hz = 822 * VoltageCal / 10000000
current_A_per_Hz = 3300 * CurrentCal / 1000000000

sp20_voltage_divider = voltage_V_per_Hz * 15397 / 1.218
sp20_current_resistor = 1.218^2 * sp20_voltage_divider / 1721506 / power_W_per_Hz
sp20_current_multiply = current_A_per_Hz / (1.218 / sp20_current_resistor / 94638)
```

These derive from the source driver's period measurements and ESPHome's frequency measurements. They preserve the installed calibration; they do not independently establish measurement accuracy. Do not use the HJL constants for a template selecting `HLW_CF` rather than `HJL_CF`.

Put the calculated numeric values in private `secrets.yaml` under the corresponding `sp20_*` keys. The profile selects `BL0937` explicitly, sets SEL inverted, and applies the current multiplier. The source energy counter and future increments therefore share the same power scale.

## Preserve energy counters and relay behavior

Immediately before the final build, capture total, today, yesterday, the source local date and total-start timestamp. Supply:

```yaml
# Shapes only: replace zeros and timestamp with the actual private source values.
sp20_energy_seed: 'EnergyTotals{0.0, 0.0, 0.0, 0}'
sp20_total_start_lambda: 'return {"REPLACE_WITH_SOURCE_TOTAL_START_TIME"};'
```

`EnergyTotals` fields are total kWh, today's kWh, yesterday's kWh, and the local calendar-date day number since 1970-01-01. Calculate that day number from the local **date**, not the UTC instant. Set the profile timezone to the installation timezone.

The supplied helper stores the migrated totals, adds raw metering energy deltas, rolls daily counters at the local date change, and retains the previous day's value. ESPHome preferences persist the structure every minute; an abrupt power loss can lose the most recent unsaved interval. A skipped full day sets yesterday to zero. No energy is invented for periods when the device was off. The native test covers cumulative deltas, duplicate readings, invalid readings, reboot baselines, daily rollover and missed days.

Preserve each source HA metering entity's unit, device class and state class. This example uses `total` for lifetime energy, `total_increasing` for today's energy, and no state class for yesterday. Keep existing recorder statistic IDs and cumulative history.

Read the final source relay state again before uploading. The sample's first-boot fallback is OFF. For an authorized migration preserving an ON source with Tasmota `PowerOnState 3`, explicitly choose `RESTORE_DEFAULT_ON`. ESPHome does **not** import Tasmota's stored relay-state bytes; subsequent boots restore ESPHome's own preferences. Preserve source rules or protection settings if they were configured; do not silently discard them.

## Build and perform one OTA upload

Use an isolated ESPHome build directory and PlatformIO core directory when another conversion is running. Keep the profile and `energy_state.h` together. The two include entries deliberately include the type before generated globals and copy the local header into the build.

Compile using the pinned ESPHome release, inspect the ESP8266 image header/checksum, and gzip the final binary. Verify exact device MAC identity again, ensure the compressed upload fits the reported free sketch space, and verify the saved energy and relay seeds still match. Use Tasmota's **Firmware Upgrade → file upload** with the compressed binary. Record the digest and one upload intent before writing. If the HTTP response times out, inspect actual device state before considering another write.

Tasmota 8.2 and later support gzip updates. Older releases need a documented intermediate upgrade path. `SetOption78` is relevant to some Tasmota upgrade paths; do not blindly add restarts or settings changes to a working web-upload path.

After boot, verify the same physical MAC, the expected ESPHome version, encrypted API connectivity, all ten meter fields, initial relay state, and plausible passive readings. No manual relay toggle or repeated physical test is implied by this verification.

## Home Assistant handover

Adopt ESPHome under its discovery identity first. Preserve the old canonical relay ID and all ten energy IDs when assigning the new entities. Handle registry collisions deliberately and retire only the exact Tasmota-owned device/discovery records after verifying ownership. A shared MQTT/Tasmota integration must remain in place for other devices. Preserve automations, dashboards, recorder metadata, sticky helpers and any existing Matter endpoint identity; do not reset a Matter bridge.

Tasmota-only diagnostics such as MQTT connection counts have no truthful ESPHome equivalent and must not be fabricated. Check references before retiring them. Save all migration receipts privately.

Sources: [ESPHome migration guide](https://esphome.io/guides/migrate_sonoff_tasmota/), [ESPHome SP20 pinouts](https://devices.esphome.io/devices/teckin-sp20/), [ESPHome HLW8012/BL0937 component](https://esphome.io/components/sensor/hlw8012/), [Tasmota 13.4.0 energy driver](https://github.com/arendst/Tasmota/blob/v13.4.0/tasmota/tasmota_xnrg_energy/xnrg_01_hlw8012.ino), [Tasmota upgrade guide](https://tasmota.github.io/docs/Upgrading/).
