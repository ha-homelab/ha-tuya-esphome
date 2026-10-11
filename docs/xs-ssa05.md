# XS-SSA05 metered plug

The observed sample accepted ordinary Tuya-Convert from stock firmware 1.0.1.
The loader reported 1 MiB QIO flash at 40 MHz, and the GPIO-neutral ESPHome
2026.9.1 image installed successfully. Its encrypted native API matched the
loader identity. No experimental PSK payload was used.

The [ESPHome device entry](https://devices.esphome.io/devices/xiangshang-xs-ssa05/)
describes a sample requiring serial installation. The successful OTA result here
applies only to this observed firmware, not every plug with the same model name.
For a serial installation, disconnect mains before attaching a 3.3 V serial adapter.

## Observed indicator variant

The [catalog template](https://templates.blakadder.com/xs-ssa05.html) and ESPHome
entry agree on the GPIO12 relay, GPIO13 button and active-low GPIO0 indicator.
Their blue-indicator assignments differ. Separate output tests on this sample
showed that GPIO15 low produced bright blue light, while GPIO4 low contributed
faint blue light. Driving both high removed the blue glow. Activating GPIO0 with
blue still on produced purple; removing GPIO0 left blue.

The [hardware package](../examples/xs-ssa05-metered.yaml) holds GPIO4 off and
uses inverted GPIO15 for ESPHome connection/warning status. The GPIO0 indicator
follows the relay, which starts with `ALWAYS_OFF`. Temporary diagnostic light
entities are not part of the final profile.

The mains output is relay-switched on/off, not dimmable. The supplied Smart Life
leaflet shows brightness and color commands as generic smart-bulb examples;
those examples do not describe the capabilities of this plug's mains output.

## Metering

The HLW8012 connection uses inverted SEL on GPIO3, CF on GPIO5 and CF1 on GPIO14.
Voltage, current, power and energy since boot are exposed with a **Not calibrated**
diagnostic. The default voltage scale was visibly inaccurate on this sample;
voltage, current and power need reference calibration before quantitative use.
Energy resets at reboot and is not a lifetime total.

Addresses, credentials, device identifiers, binaries and raw logs stay private.

## Acceptance and deployment

The owner confirmed that two physical button presses switched the test load and
red indicator together, with relay clicks. Native and HA on/off state control and
software restart from ON to OFF passed. A controlled mains-cycle test was not run.
HA uses `switch.switch11`; the source is saved in both HA and ESPHome Dashboard
as `switch11.yaml`. The dashboard includes it after Switch10. No matching old
HA entity required removal.
