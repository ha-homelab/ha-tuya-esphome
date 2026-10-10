# GPIO and final device configuration

Do not infer a pin map from a plastic enclosure. The batch's first image is
GPIO-neutral specifically because the operator cannot distinguish the unboxed
models. `esp01_1m` is a compiler board selection, not a verified hardware model.
GPIO-neutral means that firmware does not assign the relay pin; it does not
guarantee that the outlet is electrically off. The WP5 operator observed a powered
load while the input-only diagnostic firmware was running. Connect a test load
only for the controlled output checks below.

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

## WP5: identify the variant before assigning outputs

The replacement unit is marked WP5. The
[official Tasmota catalog](https://github.com/arendst/Tasmota/blob/63e278de74d14dab7c78a16e763bce6f3484c1b7/TEMPLATES.md)
records both a generic WP5 (GPIO13 button, GPIO15 relay, inverted LEDs on GPIO0
and GPIO2) and a Gosund WP5 (GPIO4 button, GPIO14 relay, inverted LEDs on GPIO12
and GPIO13). The marking alone does not select one of these maps.

After the GPIO-neutral conversion, use
[`wp5-button-probe.yaml`](../examples/wp5-button-probe.yaml) to observe the
documented button candidates as inputs before assigning a relay output. A controlled button press identifies the
responding input; physical relay/load testing is still required afterward. Do
not copy a GPIO15 output test onto an unidentified Gosund variant or enable both
relay candidates simultaneously.

On the observed WP5, repeated controlled button presses produced GPIO13
press/release events, while GPIO4 stayed inactive. A matching GPIO15-relay,
inverted-GPIO2-indicator profile was then built and installed. The operator
confirmed that the physical button switches the connected load on and off.
GPIO2 is configured from the catalog rather than used as proof of contact state.
The second inverted LED channel on GPIO0 is exposed as a separate **Red
Indicator** light at the operator's request; the operator confirmed its red color
with the relay off. It defaults off after restart and has independent HA control;
only the relay is exported through Matter. The matching package is
[`wp5-gpio15.yaml`](../examples/wp5-gpio15.yaml). Replace the input-only probe
package with this hardware package after identifying a matching unit; do not
include both because they would assign GPIO13 twice.

## KMC 30137: separate GPIO1-button variant

The operator identified the manufacturer as KMC and the model as 30137. The
[archived official Tasmota template](https://github.com/arendst/Tasmota/blob/36c8ae98da6f706b07f72aebd8dd1b770ca94cb3/TEMPLATES-PRE9.md)
provides a different map from either verified profile above:

- Button: GPIO1, active low with pull-up.
- Relay: GPIO14, active high.
- Indicator: GPIO13, active low.

The [`kmc-30137-button-probe.yaml`](../examples/kmc-30137-button-probe.yaml)
package observes GPIO1 without assigning an output. UART logging must stay
disabled (`logger.baud_rate: 0`) because GPIO1 is also the UART TX pin. Three
controlled press/release cycles were observed on this input for the current
unit. Replace the probe with
[`kmc-30137-gpio14.yaml`](../examples/kmc-30137-gpio14.yaml) only after matching
the input; verify physical relay/load behavior separately. Never include both
packages or copy the GPIO15 relay from the other models.

On the observed unit, the operator confirmed mechanical relay clicks, actual
lamp switching in both directions and the indicator following that state. This
verifies the profile for this unit; check each additional unit independently.

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

For a later WP5 in this batch, the operator explicitly chose to reuse the
previously verified profile and skip repeated button, load, indicator and restart
tests. Record that as an operator waiver for the individual unit, not a passed
physical test. Firmware identity, transfer completion and API availability can
still be recorded separately; they do not establish that unit's physical output.
