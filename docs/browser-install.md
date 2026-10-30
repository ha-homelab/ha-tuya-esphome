# Browser USB installation

For an identified **ESP8266/ESP32** device with safe, electrically isolated
serial access, **[ESPHome Web](https://web.esphome.io/)** replaces the local
command-line flasher. ESPHome Device Builder in Home Assistant can compile your
private configuration and provide the firmware download; you do not need to
install Python or ESPHome on the computer connected to the device.

**This changes the software flashing step only.** A mains-powered plug is not a
USB development board. Do not connect a computer/programmer to a device that is
connected to mains. Opening or modifying mains equipment requires appropriate
competence and safe isolation. Use the existing model-specific hardware guide;
the browser cannot identify a relay pin, verify isolation or make an unknown
board safe to energize.

## Choose the right route

- Verified ESP8266/ESP32 profile and safe serial access: use the browser flow below.
- An already converted device: retain its private configuration and use the
  project's [encrypted update profile](security-profile.md).
- **ME201W CBU / BK7231N:** this is not an ESP chip. Do not use ESP Web Tools or an
  ESP8266 image; follow the [separate CBU guide](me201w-cbu-preparation.md).
- Unidentified module or revision: identify it first using the
  [hardware](hardware.md) and [GPIO](gpio.md) guides. Enclosure/model names alone
  do not select a safe firmware image.

## Browser flow for a verified ESP board

1. In ESPHome Device Builder, select the exact validated model/GPIO profile and
   fill in your own Wi-Fi and unique API encryption credentials. Preserve the
   existing name, entity identities and calibration when migrating. Validate
   before compiling.
2. Choose **Install → Manual download**. For ESP32 choose **Factory format**
   (called **Modern format** in older versions), the
   complete `.factory.bin`; for ESP8266 use the generated firmware `.bin`.
   These files contain private settings. Do not attach them to public issues or
   releases. The project's source release archive is not a flashable image.
3. Establish only the safe, isolated serial connection described by that model's
   guide. Open **[ESPHome Web](https://web.esphome.io/)** in current desktop Chrome
   or Edge and choose **Connect**. Select the device's serial port.
4. Choose **Install** and select the private firmware download. Follow the
   browser's progress and reset prompts. **Prepare for first use** is a generic
   onboarding image, not the chosen plug's relay/indicator configuration.
5. Close the browser serial connection and disconnect the programmer. Complete
   the existing model-specific reassembly, commissioning and acceptance checks.
   A successful write does not verify the relay, button, indicator, meter
   calibration or safe mains operation.

Complete factory ESP32 and ESP8266 images are written from `0x0` by this route.
Do not use an ESP32 application-only/OTA `.bin` for an initial USB installation,
change offsets to bypass an error, or override a chip mismatch.

## Troubleshooting

- **No port:** use a USB data cable, confirm the adapter's driver and OS serial
  permissions, and close other programs holding the port. Use the board's
  documented voltage level and wiring; never improvise from a different model.
- **Cannot connect:** check the documented bootloader procedure with the device
  safely isolated. A browser cannot bypass a missing/incorrect physical connection.
- **Unsupported browser:** open the HTTPS site in a desktop browser with Web
  Serial; an in-app view or iPhone/iPad browser is not this installation path.
- **Image rejected:** recheck chip, board profile and factory-versus-OTA format.
  Do not retry an unrelated image.
- **Flashed but wrong behavior:** keep loads disconnected, return to the verified
  GPIO profile and [troubleshooting guide](troubleshooting.md). Do not infer that
  a successful network connection validates electrical behavior.

Background: [ESP Web Tools](https://esphome.github.io/esp-web-tools/) and
[ESPHome Device Builder](https://esphome.io/guides/getting_started_hassio/).
