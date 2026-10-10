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

- Legacy ESP8266/ESP8285 with compatible stock firmware: `tuya-convert`.
- Already running ESPHome: normal ESPHome OTA; do not run Tuya-Convert again.
- Already running Tasmota: follow ESPHome's
  [Tasmota migration guide](https://esphome.io/guides/migrate_sonoff_tasmota/).
- A Beken/Realtek module is a different target. Stop using the ESP8266 image.
  [Tuya CloudCutter](https://github.com/tuya-cloudcutter/tuya-cloudcutter) and
  [LibreTiny](https://esphome.io/components/libretiny/) cover some such hardware,
  but they are outside this batch's selected workflow.

## Handling unsuccessful units

The chosen operating policy skips original-firmware backups and does not include
disassembly, soldering, serial recovery, or module replacement. If pairing fails,
check the station and pairing mode once; if the unit remains incompatible or
unresponsive, label it locally as failed and move to the next unit. Retire it as
electronic waste. This policy does not authorize deleting existing Matter fabrics
or resetting unrelated equipment.

Keep plugs unloaded during identification. Do not connect a live mains-powered
board to a USB/UART adapter. This workbench performs the selected conversion over
Wi-Fi with the enclosure intact.
