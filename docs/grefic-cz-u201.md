# GREFIC CZ-U201: observed two-outlet ESP8266 variant

One owner-reported CZ-U201, with no FCC ID visible on its label, accepted the
ordinary Tuya-Convert handshake. The live VTRUST-FLASH 1.5 loader identified an
ESP8266, normal boot, bootloader version 4 and 1 MiB QIO flash at 40 MHz. This
identification takes precedence over assumptions from similar model names or
unmatched certification photographs.

A private 1 MiB flash image was read after the intermediate loader started. It
contains the original application and the intermediate loader; it is not a
pristine pre-conversion full-chip image. Firmware, credentials and identifying
network data are not published here.

## Hardware evidence

The original application's embedded hardware JSON describes two active-high
relay channels, GPIO15 and GPIO14, an active-low shared button on GPIO0, and an
active-low Wi-Fi status indicator on GPIO13. The owner confirms one shared
physical button. The JSON also contains metering configuration; metering has not
been enabled or validated, and its calibration must not be generalized.

The initial 420,800-byte GPIO-neutral ESPHome 2026.9.1 image installed in
31,122 ms. Its encrypted API matched the loader identity and expected build.
The subsequent 428,560-byte two-relay image installed using encrypted ESPHome
OTA in 24.39 seconds (24.28 seconds of transfer). Readback matched the intended
identity, build and two switch entities. Both relays use `ALWAYS_OFF`.

The shared button turns both relays off if either is on, and turns both on when
both are off. GPIO13 is a network-status LED, not feedback from relay contacts;
a dark indicator during normal operation is expected for this configuration.

## Acceptance status

Native API commands independently produced OFF/OFF, ON/OFF, OFF/ON, ON/ON and
OFF/OFF. Those are reported software states, not measurements at the outlets.
The owner confirmed the left-hand lamp stayed off with channel 1 alone and
turned on with channel 2 alone: GPIO14 controls the left outlet.

The right-hand lamp then lit with channel 1 alone, identifying GPIO15 as the
right outlet. With the right lamp attached, two shared-button presses turned it
off and back on. Native events recorded GPIO0 press/release and the expected
relay transitions, ending with both channels ON.

The owner removed mains power for five seconds and restored it without pressing
the button. The right lamp remained off, and a new encrypted API connection
reported both outputs OFF with the same firmware build. This is a controlled
mains-cycle check, not a measurement of short electrical transients during boot.
No separate software-restart, metering or Matter/controller acceptance is claimed.
The device was added to HA with separate left and right switch entities. Each
passed an ON/OFF service cycle with matching HA contexts while the other outlet
stayed OFF. Both ended OFF. The final YAML and private secret references were
saved and independently verified in both HA and the ESPHome Dashboard. Existing
entities and secret values were preserved; no HA restart was required.

## Replacing two existing plugs

The two outputs subsequently received separate load-role names in HA, replacing
one LocalTuya control and one Matter control. The old devices, entity IDs and
names were retained so they can be reused. Native ESPHome channel identities,
GPIO assignments and the firmware were unchanged. One role supplies power to a
separate appliance; it does not issue that appliance's operating command.

The handover updated two HA automations, three Lovelace bindings and six private
desktop configuration files. A stale light-domain reference in a load-selection
map now addresses the replacement switch; the existing power estimate and
automation guard were retained. Existing scripts had no matching references.
HA configuration validation passed and the automations were reloaded without a
HA restart. Both replacement controls appeared available and OFF in the native
desktop client. No load commands were sent during this role handover.

The owner confirmed relocation and the intended left/right load connections.
The encrypted API and both HA switches were available after relocation, with
both outputs initially OFF. A subsequent command turned on only the lighting
output; HA reported the matching command context and the other output stayed
OFF. After the owner resumed the lighting check, another OFF-to-ON command
received a matching HA context, and the owner confirmed that the installed
floodlight illuminated. The other output stayed OFF. The owner then requested
the second output's check: an OFF command to the lighting output and an ON
command to the appliance-power output each received a matching HA context,
with the unaddressed output unchanged. The owner confirmed that the floodlight
went dark and the separately powered appliance operated using its own remote.
Both intended loads therefore passed their installation checks. At the owner's
request, appliance power was then turned OFF with a matching HA command context;
both outputs ended OFF. The common button still
controls both outputs together, and both outputs still start OFF after loss of
mains power.

On 2026-10-10, the owner subsequently requested removal of the old LocalTuya
appliance-power plug after reporting that it was reset and no longer needed.
Its LocalTuya device and entity were removed through HA's device-removal API.
The saved configuration contains exactly one fewer device; all other LocalTuya
device configurations are unchanged. The replacement appliance-power output
remained available and OFF. The old Matter plug was not part of this removal.

Use [the observed dual-outlet package](../examples/grefic-cz-u201-dual.yaml) with
the GPIO-neutral base only after matching the hardware. Channel 1 is right and
channel 2 is left when facing the outlets. This one tested sample does not prove
that every enclosure with the same model marking uses the same board.
