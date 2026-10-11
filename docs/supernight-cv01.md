# Supernight CV01: two outlets and metering

The owner identifies this two-outlet plug as SUPERNIGHT, FCC ID 2ANJ7-CV01.
The owner reported that it was not previously configured in HA; the registry
check found no matching device. Both outlets were confirmed empty before
conversion.

Stock firmware 1.0.4 accepted ordinary Tuya-Convert. VTRUST-FLASH 1.5 reported
an ESP8266-family device, normal boot, bootloader 4, and 1 MiB DOUT flash at
40 MHz. A full flash read was retained privately after loading the intermediate
firmware; it is not a pristine factory dump. The 420,800-byte GPIO-neutral
ESPHome 2026.9.1 image installed and joined the LAN with encrypted native API
access. Exact network identifiers and credentials remain private.

## Button observations

The [published ESPHome profile](https://devices.esphome.io/devices/supernight-double-outlet-plug/)
uses GPIO1 for the left button and the ADC input for the right button. An
input-only probe on this sample recorded an owner-confirmed left press and
release on GPIO1, active low. The right button read approximately 7 when
released and 1024 when pressed. This is the opposite polarity to the published
example. Copying its low-reading press condition would be incorrect here.

The candidate uses a raw ADC threshold above 500 for a press, 20 ms filtering,
and a ten-second startup delay. The right button is armed only after the delay
and a released reading below 50. This addresses the reference's warning about
unstable early ADC readings without treating a held button as a startup command.

## Verified configuration and remaining checks

The 435,872-byte relay/metering firmware uses GPIO3 for the left relay and
GPIO12 for the right relay, both `ALWAYS_OFF`. UART logging is disabled because
GPIO1 and GPIO3 are used by the hardware. Each button toggles its corresponding
channel. GPIO14 is configured as an inverted status indicator.

The stock application contains the `hlw8012.c` identifier. The candidate follows
the reference's metering connections: inverted SEL on GPIO13, CF on GPIO5, and
CF1 on GPIO4. It exposes voltage, current, active power, and energy since boot,
plus a `Not calibrated` diagnostic. The provisional shunt and divider values
are 0.001215 ohm and 806; no calibration points from the reference's test load
were copied. These are not verified absolute measurements.

Native API checks independently exercised each relay and returned both outputs
OFF after a software restart from both ON. The owner then tested a fan in each
outlet: left-only powered the left outlet, and right-only stopped it there and
powered it after moving to the right outlet. The right button stopped and
restarted the fan in the right outlet. Pressing the left button twice changed
only the left channel's reported state, leaving the right fan running.

With both outputs ON, the owner disconnected mains power for five seconds and
restored it without pressing a button. The right fan remained stopped, and a
fresh encrypted API connection reported the same firmware and both channels
OFF. These checks do not measure short boot transients.

HA adopted the device through its encrypted ESPHome API. Both switch entities
passed independent HA service checks, ending OFF. Voltage, current, active power,
energy since boot and calibration status were all present with their expected
units and measurement/energy state classes. A no-load reading was approximately
120.3 V, 0 A and 0 W; these values are not reference calibration. The complete
source and private credentials were persisted and verified in HA and the
ESPHome Dashboard without changing existing secret values.

The [hardware package](../examples/supernight-cv01.yaml) reproduces the tested
button, relay and metering configuration. The published reference reports blue
indicators wired to the relays and a photosensor-controlled night light; those
behaviors have not yet been checked on this sample. Absolute meter calibration
and coverage of the left outlet remain unverified.

## Later role reassignment

The owner subsequently assigned separate household roles to the right and left
outlets, with orientation explicitly confirmed while looking at the device
from the front. The right outlet took over an existing television role; the
left took over another existing switch role. The displaced plugs were retained
in HA. Registry verification matched the right and left roles to their
respective ESPHome unique IDs and the same physical device.

HA name overrides implement this reassignment without changing the accepted
firmware, GPIO mapping or independent button behavior. No relay command or
additional flash was issued for the reassignment. Exact household entity IDs
remain in the private inventory.
