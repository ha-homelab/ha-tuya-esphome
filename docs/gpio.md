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

## YM-WS-1: different reported boards, one observed GPIO15 variant

The next unit is marked YM-WS-1. Its first pairing attempt ended before it joined
the conversion AP; no replacement firmware was written. The operator could not
restore rapid blinking. That is a pairing-stage blocker, not evidence of a
failed flash or incompatible firmware.

Upstream first-hand reports describe different boards under this marking:
[Geekbes YM-WS-1](https://github.com/ct-Open-Source/tuya-convert/issues/56) uses a
GPIO14 relay, while [ANIKUV YM-WS-1](https://github.com/ct-Open-Source/tuya-convert/issues/95)
uses GPIO15 relay, GPIO13 button and inverted GPIO12 LED. Neither report proves
every unit's mapping. Do not select the XS-SSA01 hardware package based only on
a similar enclosure.

A later YM-WS-1 selected from an existing LocalTuya role reached the loader and
was converted. The [ESPHome device entry](https://devices.esphome.io/devices/geekbes-ym-ws-1/)
also describes GPIO15 relay, GPIO13 button and inverted GPIO12 indicator. After
installing a GPIO-neutral image, that candidate was applied through encrypted
OTA. The operator confirmed that its physical button switches a real load on
and off and the indicator follows. This validates that mapping for the later
unit, not the contradictory variants above.

Use [`ym-ws1-gpio15.yaml`](../examples/ym-ws1-gpio15.yaml) with the GPIO-neutral
base after matching the hardware. It provides a local debounced button,
`ALWAYS_OFF` relay and internal indicator, and a diagnostic restart button.
Do not combine it with another GPIO package.

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

A later WP5 installation intentionally omitted the independent GPIO0 red-light
entity and left GPIO0 unassigned. Its own input probe identified GPIO13, then
the operator confirmed physical button, relay, connected lamp and inverted
GPIO2 indicator behavior in both directions. The installed relay-only profile
uses the same GPIO15 relay with `ALWAYS_OFF` and the internal GPIO2 indicator;
omitting the extra red channel does not change those pins. API on/off and
software restart from ON to reported OFF passed. No mains-cycle or
boot-transient acceptance is claimed for that check.

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

## JH-G01U: GPIO4 relay and active-low GPIO12 indicator

The observed unit reached the ordinary conversion loader and booted the
GPIO-neutral image. Its model-specific candidate used GPIO4 relay, GPIO5 button
with an inverted pull-up input, and GPIO12 indicator. The operator confirmed
that the physical button switches an actual load in both directions.

The first non-inverted GPIO12 configuration lit the indicator while the load was
off and extinguished it while the load was on. This identifies active-low LED
polarity for the observed unit. The corrected `inverted: true` firmware was
compiled, installed through encrypted OTA, and checked through the encrypted
API. The corrected LED has not been visually rechecked, and no separate
software-restart or power-cycle acceptance test was performed for this unit.

The provisional package is
[`jh-g01u-gpio4.yaml`](../examples/jh-g01u-gpio4.yaml). Include it with the
GPIO-neutral base only after matching the unit. It has a debounced local button,
an `ALWAYS_OFF` relay, an internal indicator following relay commands, and a
diagnostic restart button. Do not combine it with another GPIO package.

## TanTan WP3: observed GPIO15-relay variant

A TanTan WP3 selected from an existing LocalTuya light role initially ran an
input-only image with GPIO4 and GPIO13 button candidates. Its encrypted API identity and
build timestamp were verified. One controlled press produced GPIO13
press/release events while GPIO4 stayed unchanged. This supports the older
documented WP3 candidate. Its [GPIO15 package](../examples/wp3-gpio15.yaml)
is installed with encrypted OTA/API verification. Two final-profile button
presses produced matching reported relay transitions OFF, ON, OFF, and the
operator confirmed relay clicks, actual light-load switching and the inverted
GPIO2 indicator following those actions. GPIO0 remains unassigned. Software
restart from ON returned reported state OFF, and HA found it available and OFF
after relocation. No controlled ON-to-OFF mains-cycle test or boot-transient
measurement was performed. Follow the
[WP3 identification and switch-migration notes](wp3-migration.md). Do not reuse
another model's relay package merely because its enclosure appears similar.

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

## GREFIC CZ-U201: two independently switched outlets

One ESP8266/1 MiB sample's original application contains a two-channel hardware
JSON. Physical lamp tests confirmed channel 1/GPIO15 on the right and channel
2/GPIO14 on the left, both active high. Its shared active-low GPIO0 button
switches both outputs; the active-low GPIO13 LED is configured for network status.
Both outlets returned OFF after a controlled mains cycle from both ON.

The [dual-outlet package](../examples/grefic-cz-u201-dual.yaml) belongs with the
GPIO-neutral base, not with another model's hardware package. Its status LED is
normally dark when healthy; it is not a load-power indicator. Metering pins from
the original JSON are left unconfigured because metering has not been tested.
See [the complete evidence and limitations](grefic-cz-u201.md).

## KMC 30608: three independently switched outlets

One ESP8266/1 MiB Smart Tap running stock firmware 1.0.5 accepted ordinary
Tuya-Convert. An input-only probe confirmed active-low GPIO16 button events.
Separate physical lamp tests matched numbered outlets 1, 2 and 3 to active-high
GPIO15, GPIO13 and GPIO14 respectively. The common button turns all outputs OFF
if any is ON, or all ON if all are OFF. All three use `ALWAYS_OFF`; software
restart and a controlled mains cycle from all ON both returned all OFF.

Use the [three-outlet package](../examples/kmc-30608-three-outlet.yaml) with the
GPIO-neutral base. GPIO1 is reserved for the inverted network-status indicator,
so UART logging is disabled. Visual indicator behavior remains unverified.
The optional [metering package](../examples/kmc-30608-metering.yaml) uses HLW8012
SEL on GPIO12, CF on GPIO4 and CF1 on GPIO5. Voltage/current/power/energy readings
and a load response on outlet 3 were observed; calibration and coverage of the
other outlets remain unverified. See [the detailed evidence](kmc-30608.md); do not confuse
this hardware with the separate single-relay KMC 30137 variant.

The second KMC sample confirmed GPIO1 lights the common indicator only. Its
stock table disables separate per-channel LED outputs. It also associates
Tuya datapoints 1/2/3 with physical outlets 3/2/1; do not infer migration mapping
from channel numbers alone. The first unit's role association was corrected
after the owner confirmed its normal loads remained disconnected. Its outlet 3
indicator works with the same profile; the second unit's indicator diagnosis
was deferred by the owner.

## Supernight CV01: two outlets and an analog button

The tested sample uses GPIO3 for the left relay, GPIO12 for the right relay,
and active-low GPIO1 for the left button. Its right button is on A0: raw readings
are approximately 7 released and 1024 pressed, opposite to the published
reference. The [hardware package](../examples/supernight-cv01.yaml) uses the
observed polarity, debounce, and startup arming delay. Both outlets and button
behavior passed physical tests; restart and mains cycling returned both OFF.

The uncalibrated HLW8012 uses inverted SEL GPIO13, CF GPIO5 and CF1 GPIO4.
GPIO14 follows the reference's inverted status-indicator assignment but its
visual behavior remains unverified. UART logging must stay disabled. See
[the complete acceptance record](supernight-cv01.md).
