# GPIO and final device configuration

Do not infer a pin map from a plastic enclosure. The batch's first image is
GPIO-neutral specifically because the operator cannot distinguish the unboxed
models. `esp01_1m` is a compiler board selection, not a verified hardware model.

## Historical AWP04L candidate

A previous, working household configuration had:

- Relay: GPIO12; startup state `ALWAYS_OFF`.
- Button: GPIO13, inverted; pressing toggled the relay.
- Red LED: GPIO0, inverted; blue LED: GPIO15, inverted.
- Metering candidate: HLW8012-compatible driver, inverted select on GPIO3,
  CF on GPIO5, CF1 on GPIO14. The older notes suggested BL0937 hardware.

This map is a **reference for identification**, not a configuration approved for
every unit. Do not copy the old unit's current/voltage calibration coefficients.
They do not establish the new unit's accuracy or even its metering chip.

## XS-SSA01: first observed unit

The operator read **XS-SSA01** on the enclosure. The first GPIO12 attempt changed
only an LED: a known-working load stayed off and there was no mechanical click.
Home Assistant history confirmed that the physical button is on GPIO13.

The [official Tasmota template catalog](https://github.com/arendst/Tasmota/blob/63e278de74d14dab7c78a16e763bce6f3484c1b7/TEMPLATES.md)
contains an XS-SSA01 variant matching those observations:

- Relay: GPIO15, active high.
- Button: GPIO13, active low with pull-up.
- Indicator: GPIO12, active low.

The catalog also contains an XS-SSA01 v2 with its button on GPIO1, and a Martin
Jerry XS-SSA01 with a GPIO14 relay. The marking alone does not identify the board
revision. Match observed behavior and verify physical output before reusing a
profile. Do not apply the historical AWP04L LED assignment to this plug: its
GPIO15 is the relay output.

The matching package is [`xs-ssa01-gpio15.yaml`](../examples/xs-ssa01-gpio15.yaml).
Copy it into the private build directory beside the GPIO-neutral base YAML and
include it in that unit's configuration:

```yaml
packages:
  hardware: !include xs-ssa01-gpio15.yaml
```

The package uses `ALWAYS_OFF`, a debounced local button, an internal LED following
the commanded relay state, and a diagnostic restart button. Neither the LED nor
the HA switch state is feedback from the relay contacts. The operator confirmed
mechanical clicks and actual load switching in both directions from the physical button with this GPIO15 profile. See
[the deployment record](deployment-record.md) for restart and ecosystem checks.

Keep the original GPIO-neutral YAML and image for unknown plugs. The historical
[`relay-gpio12-candidate.yaml`](../examples/relay-gpio12-candidate.yaml) and
[`button-gpio13-candidate.yaml`](../examples/button-gpio13-candidate.yaml) describe
the initial attempt; do not combine them with the XS-SSA01 package. GPIO12 is not
a relay output for this observed variant.

## YM-WS-1: a separate, unverified unit

The next unit is marked YM-WS-1. Its first pairing attempt ended before it joined
the conversion AP; no replacement firmware was written. The operator could not
restore rapid blinking. That is a pairing-stage blocker, not evidence of a
failed flash or incompatible firmware.

Upstream first-hand reports describe different boards under this marking:
[Geekbes YM-WS-1](https://github.com/ct-Open-Source/tuya-convert/issues/56) uses a
GPIO14 relay, while [ANIKUV YM-WS-1](https://github.com/ct-Open-Source/tuya-convert/issues/95)
uses GPIO15 relay, GPIO13 button and inverted GPIO12 LED. Neither report proves
the current unit's mapping. Do not flash the XS-SSA01 hardware package onto this
unit based only on its similar appearance.

## Verification sequence

1. Confirm stable Wi-Fi, API and OTA first.
2. Read visible markings and compare a model-specific source if available. Keep
   any photos or serial markings local until sanitized.
3. Work on one unloaded unit. Add only a relay candidate and an explicit
   `restore_mode: ALWAYS_OFF` after evidence supports that pin. Do not bulk-sweep
   GPIOs, drive supply pins, or enable an assumed metering interface.
4. Toggle it from Home Assistant, verify physical switching, then reboot and
   confirm the off state. Stop if behavior is inconsistent.
5. Add and verify the button; check that its polarity and boot behavior are correct.
6. Add LEDs and metering separately. Validate metering against a reference before
   relying on power values for automation.
7. Give the relay an appropriate plug/switch device class and a stable entity ID.
   Record a sanitized, verified model profile only after these checks pass.

Physical validation remains necessary: successful compilation says nothing about
which pin controls a real relay. The owner chose to retire unsuccessful units;
serial recovery and live-board probing are not part of this project.
