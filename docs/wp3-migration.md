# TanTan WP3: identification and switch migration

## Observed conversion and handover

The operator identified this plug as **TanTan WP3**, previously managed through
LocalTuya as a light entity. It now runs ESPHome as an ordinary relay switch,
with HA and desktop references migrated and real motion control verified.
The marking alone does not establish another unit's GPIO variant or firmware
compatibility.

An ESPHome 2026.9.1 input-only image was built privately: 424,448 bytes, with
GPIO4 and GPIO13 exposed as debounced active-low button candidates. It assigns
no relay or indicator outputs and disables UART logging. Building that image
does not establish successful installation or physical button identity. Its
checksum, DOUT/40 MHz header and staged-file digest were checked.

The operator reported rapid blinking and a phone connected to the conversion
AP, including a reconnect after the workbench had not observed a station. That
report and a selected Wi-Fi network on the phone are not proof of association
at the workbench. A later loader read matched the expected physical identity
and reported ESP8266 bootloader version 4, normal boot and 1 MiB flash. The stock
flash mode was QIO; the staged ESPHome image uses DOUT.

A private 1 MiB stock-firmware backup was saved for this attempt. The input-only
image then installed in 8,000 ms. Encrypted API readback matched the target's
physical identity, ESPHome 2026.9.1 and the probe's exact compilation timestamp.
This establishes the installed diagnostic firmware, not relay operation.

One controlled short button press produced GPIO13 press/release events while
GPIO4 stayed unchanged. This matches the button assignment in the catalog's
older WP3 template; it does not by itself prove the relay or indicator pins.
The final candidate image was 440,480 bytes with a valid checksum and DOUT,
40 MHz, 1 MiB flash settings. Encrypted ESPHome OTA uploaded it in 4.32 seconds;
the full update took 4.34 seconds. Native API readback matched the physical
identity, version and compilation timestamp, exposed one relay switch and one
physical-button sensor, and no longer exposed either probe entity.

Encrypted API on/off commands changed the reported relay state as expected. A
software restart was requested while the relay reported ON; the device
reconnected with the same final build and reported OFF. This verifies the
commanded state after software restart, not the physical contacts or transient
behavior while booting.

Two later physical button presses produced matching button events and reported
relay states OFF, ON, OFF through the encrypted API. This confirms the installed
button-to-relay control path. The operator confirmed relay clicks and that both
the indicator and connected light switched on and off with those presses. This
verifies the observed GPIO15 relay, GPIO13 button and inverted GPIO2 indicator
mapping for this unit. The conversion container, AP and dedicated session
were then closed.

This is the fourteenth Tuya-to-ESPHome firmware conversion and the eighth with
its own physical button/load acceptance. The operator later moved the plug to
its installed position, disconnecting and reconnecting mains power. A later
HA readback found the ESPHome relay available and OFF. HA migration and reloads
overlapped that move, so availability-history gaps are not attributed solely to
the physical power interruption. Boot transients and an on-to-off physical
power-cycle test were not measured; the software ON-to-OFF restart check above
is separate evidence.

The desktop handover is complete: all six persisted configuration files match
their reviewed edits, and the running native client shows the canonical switch
available and OFF with the intended label and placement. The other related
control, unrelated plugins and authentication were preserved. Its HA, HA MQTT
and gateway connections were live, and no actuator commands were sent during
this configuration verification.

The operator initially reported that the motion sensor did not switch on the
load after relocation. The loaded HA automation still called `light.turn_on`
on the retired entity. After the automation reload and old-entity removal, a
natural sensor OFF-to-ON event triggered the rule and the new switch changed
from OFF to ON about 0.13 seconds later. The sensor event, automation run and
switch state carried the matching parent/automation contexts, and the operator
confirmed that motion control worked. No synthetic trigger was used, and the
sensor and manual-override helper were unchanged. This verifies the live motion
path.

The completed HA audit scanned 2,456 active files and found no retired-entity
references. The migrated files matched their intended content, and unrelated
source files and LocalTuya devices were unchanged. The old device identity was
absent. Automations, scripts, the group, Lovelace and the floorplan were updated.
The canonical switch appeared in the existing mixed group alongside
its other two members, and the motion rule remained enabled with the
manual-override helper preserved. Final ESPHome source and private secret
references were persisted in both active configuration locations. HA remained
running throughout; this handover required no HA restart.

## Second sample

A later plug marked WP3 was identified from its former LocalTuya identity and
converted under its existing numbered spare-switch name. The loader identity
matched and reported 1 MiB flash. A complete private post-loader backup was
retained; it is not a pristine factory image.

The 424,432-byte input-only image installed in 7,045 ms. Encrypted API readback
matched its identity and build. A short owner-confirmed press produced a
GPIO13 active-low pulse lasting approximately 0.200 seconds; GPIO4 did not
change. The corresponding GPIO15 relay and inverted GPIO2 indicator profile
was then installed as a 440,480-byte ESPHome 2026.9.1 image using encrypted OTA.

Native relay commands and a software restart from ON to OFF passed. The owner
confirmed that two short button presses switched the connected lamp and
indicator on and off with relay clicks. The final observation log did not
capture both button cycles, so that physical acceptance rests on the owner's
report; it is separate from the recorded input-probe and native API checks.
Controlled mains-cycle and boot-transient measurements remain unperformed.

HA adopted the ESPHome relay under the same numbered entity ID, preserving its
existing dashboard row. Final source and unique credentials were saved and
read back in HA and ESPHome Dashboard. The matched LocalTuya record was removed
without changing the other device configurations. HA service ON/OFF checks
passed and left the relay OFF. This is the twenty-first firmware
conversion and fourteenth plug with individual physical button/load acceptance.

## Confirm each milestone

1. Observe the secondary station in the workbench's AP station list, then
   distinguish that station from the target plug. Confirm the target joins in
   the intended pairing mode. Follow [pairing troubleshooting](troubleshooting.md#plug-never-reaches-the-intermediate-loader)
   if it never reaches the loader.
2. Match the intermediate loader's identity against the private LocalTuya and
   network inventory. Read its flash size before selecting an image; keep all
   identity values out of public documentation.
3. Record the write result and check the installed image through the encrypted
   native API. Observe controlled button presses with the input-only image.
   Do not infer the relay GPIO from the button GPIO or the WP3 enclosure.
4. Apply only an identified hardware profile, replacing the probe definitions.
   Record the relay, button and indicator pins and polarities independently.
   Test the real load and button behavior, and distinguish those observations
   from commanded switch state and indicator state. Record startup behavior
   separately, following the [GPIO verification sequence](gpio.md#verification-sequence).
5. Complete HA and client migration only after the replacement is verified.
   Keep unfinished milestones pending rather than treating a successful build,
   Wi-Fi lease or API connection as complete acceptance.

The output package below is installed and passed the observed button/load and
indicator checks. Input-only firmware does not guarantee an electrically
de-energized outlet.

## Distinguish the documented variants

The [TanTan WP3 template catalog](https://templates.blakadder.com/tantan_WP3.html)
lists two mappings. Its older template, described as purchased before February
2020, uses GPIO13 for the button, GPIO15 for the relay and inverted LED channels
on GPIO2 and GPIO0. The other template uses GPIO4 for the button, GPIO14 for the
relay and inverted LED channels on GPIO2 and GPIO12.

The observed button, load and indicator behavior match the older template's
GPIO15 relay and inverted GPIO2 indicator. The installed profile uses an
`ALWAYS_OFF` relay, a debounced active-low pull-up button, and an internal binary indicator that
follows the relay's callbacks for both button and API commands. GPIO0 remains
unassigned. No claim about manufacture date or every WP3 revision follows from
the observations on this unit.

The matching package is [`wp3-gpio15.yaml`](../examples/wp3-gpio15.yaml).
Include it with the GPIO-neutral base after identifying a matching variant;
remove the button probes and do not combine it with another hardware package.
The exposed relay is a switch, while the indicator is internal. It does not
publish a dimmable light or the unused second indicator channel.

The public package passed ESPHome 2026.9.1 configuration validation and a
separate build using generated test credentials. That example image was
440,528 bytes, below the 512 KiB initial-image limit, with a valid ESP8266
checksum and DOUT/40 MHz/1 MiB header. It was not flashed; the installed image
size above refers to the private device configuration. A successful example
build does not add physical acceptance evidence.

## Preserve behavior when changing the HA entity domain

Renaming a LocalTuya light to an ESPHome switch requires more than replacing an
entity ID. Maintain the exact old-to-new mapping privately, using one canonical
`switch.*` entity and the operator's requested display name. Preserve unrelated
devices, schedules, conditions, delays and manual-override helpers.

- Inspect automations, scripts, scenes, templates, customizations and Lovelace
  definitions for direct references and indirect group membership.
- Update domain-specific service calls as well as their targets. If a
  `light.turn_on` or `light.turn_off` action also controls genuine lights, retain
  those light targets and handle the relay with the corresponding switch
  action. Do not transfer brightness, color or transition parameters to a relay.
- Remove the relay from light-only groups without removing the remaining
  lights. Preserve the intended on/off behavior through suitable switch or
  domain-neutral actions, then check callers of the changed group.
- Check desktop bindings and persisted client configuration for both the old
  entity ID and its light-specific behavior. A control for this relay must use
  switch services and must not offer unsupported dimming or color controls.
- Validate the saved HA configuration and reload only the affected domains.
  Read back the new entity, effective automation/script targets, dashboard
  configuration and deployed client bindings. A source edit alone does not
  prove that a running client adopted it.
- Retire only the matched old LocalTuya device after dependent references have
  migrated. Audit active source and persisted configuration for stale
  references, and save the final ESPHome YAML and private secret references.

Any future Matter exposure must select only the canonical relay and preserve
the existing bridge endpoints and fabrics. Firmware installation, HA adoption,
client adoption and controller load tests are separate results; record only
those actually verified.

## Private evidence and public follow-up

Keep loader details, device/network identifiers, credentials, build artifacts,
raw logs and actual household entity names in the private per-unit directory.
Public follow-ups should report observed pins and polarity, firmware version
and size, installation outcome, physical tests performed or explicitly deferred,
and migration/readback outcomes. Claim a hardware revision only when identified.
Update [the deployment record](deployment-record.md) and the conversion count
only when supported by those results.
