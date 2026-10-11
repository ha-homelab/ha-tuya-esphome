# Hardware and scope

## Current batch

The batch includes old, unboxed, not-yet-commissioned Wi-Fi plugs and later units
previously managed through LocalTuya. They look like previously converted units
and are reported to contain ESP8266/“ESP-01” hardware.
The first unit reports 1 MB flash, runs ESPHome, and is marked XS-SSA01. Its
GPIO13 button and GPIO12 indicator match a documented GPIO15-relay variant.
The operator confirmed mechanical clicks and actual load switching with that
profile; see [GPIO identification](gpio.md).
Do not infer a board revision from the enclosure or model marking alone.

The previous ESPHome configuration used `board: esp01_1m` for an AWP04L-style
plug. This board identifier selects an ESP8266 build layout; it does **not** prove
that a physical eight-pin ESP-01 module is inside. A literal ESP-01 does not expose
the same pins as every ESP8266-based plug board.

For unidentified variants, the first image contains no GPIO outputs, UART logger output,
metering driver, or assumed relay pin. It supplies Wi-Fi, encrypted API, OTA,
fallback provisioning and diagnostic entities. Confirm the actual memory layout
from the conversion loader's report before selecting the final image.

## Tool selection

The [KMC 30608 Smart Tap conversion](kmc-30608.md) records a separate three-relay
unit successfully converted from stock firmware 1.0.5 to ESPHome. The chip,
memory, numbered outlets, button and OFF state after a mains cycle were verified.
A third sample running stock 1.0.6 also accepted conversion, but reported DOUT
flash instead of the first two samples' QIO. Native relay controls, a software
restart and a physical load on outlet 1 passed. The owner deferred the remaining
physical acceptance checks; the three outputs were returned OFF.
The [Supernight CV01 record](supernight-cv01.md) covers another two-outlet
ESP8266-family sample converted from stock firmware 1.0.4. Its analog right
button has the opposite polarity to the published example; use a per-unit
input probe rather than assuming identical behavior from the enclosure.

- Legacy ESP8266/ESP8285 with compatible stock firmware: `tuya-convert`.
- Already running ESPHome: normal ESPHome OTA; do not run Tuya-Convert again.
- Already running Tasmota: follow ESPHome's
  [Tasmota migration guide](https://esphome.io/guides/migrate_sonoff_tasmota/).
- A Beken/Realtek module is a different target. Stop using the ESP8266 image.
  [Tuya CloudCutter](https://github.com/tuya-cloudcutter/tuya-cloudcutter) and
  [LibreTiny](https://esphome.io/components/libretiny/) cover some such hardware,
  but they are outside this batch's selected workflow.

## Handling unsuccessful units

The original operating policy skips original-firmware backups; the later
[WP3 attempt](wp3-migration.md) and a subsequent WP5 saved backups privately as
per-unit exceptions. The later GREFIC CZ-U201 investigation retained a private
post-loader image and recovered its two-channel configuration from the original
application. See [the observed variant](grefic-cz-u201.md). The selected workflow does not include disassembly,
soldering, serial recovery, or
module replacement. If pairing fails,
check the station and pairing mode once; if the unit remains incompatible or
unresponsive, label it locally as failed and move to the next unit. Retire it as
electronic waste. This policy does not authorize deleting existing Matter fabrics
or resetting unrelated equipment.

Keep plugs unloaded during identification. Do not connect a live mains-powered
board to a USB/UART adapter. This workbench performs the selected conversion over
Wi-Fi with the enclosure intact.
