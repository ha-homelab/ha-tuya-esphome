# Troubleshooting by stage

## Slow container startup with repeated hostname warnings

With `--network none`, Docker may omit the container hostname from `/etc/hosts`.
Then upstream calls to `sudo` wait on DNS and print `unable to resolve host`.
The launcher supplies a fixed local hostname and a loopback host entry. This is
separate from a radio failure; verify `AP-ENABLED` and service listeners as well.

## Host cannot install packages

If ordinary HTTPS works but APT repeatedly times out, inspect `apt-config dump`
locally for proxy settings. Our reference installation had a stale proxy address.
Disable only the obsolete entry or test with explicit `Acquire::http::Proxy=DIRECT`
and `Acquire::https::Proxy=DIRECT`. Confirm a successful index refresh before
installing packages. Do not publish proxy URLs; they may contain credentials.

## No Wi-Fi interface

Check `ip -br link`, `sudo rfkill list`, and kernel firmware messages. Missing
board NVRAM and a driver clock timeout were the reference host's failure; see
[the exact-hardware repair](workbench.md#reference-broadcom-repair). USB Wi-Fi is
an alternative only if its Linux driver supports AP mode. A detected radio alone
does not prove that AP mode and network-namespace transfer work.

## AP/namespace setup fails

Check that management uses Ethernet, no other conversion container owns the
radio, and `iw phy` lists AP support. Inspect the launcher's saved Wi-Fi log.
After an interrupted session, inspect the named workbench container before
stopping it; a live flash must not be interrupted accidentally. Once its namespace
is destroyed, verify that the radio has returned with `sudo iw dev`.

The reference Broadcom radio once disappeared when the container was removed
without explicitly returning its PHY first. The launcher now lowers the interface
and uses `nsenter` plus a numeric `phy#<index>` selector to return it to the host
before removal. Numeric selection matters because the host's sysfs view can hide
the moved radio even after entering its network namespace. If an old launcher
already stranded this specific radio, and no flash is running, reloading
`brcmfmac` restored it over the wired management connection. Do not unload an
arbitrary active Wi-Fi driver while management depends on it.

If hostapd rejects a channel, verify the real country/regulatory configuration
and use an allowed 2.4 GHz channel. Do not copy another country's regulatory
settings or broaden the radio's permitted channels.

## Plug never reaches the intermediate loader

Check that only one target is powered, it is fast-blinking, and a secondary phone
remains on `vtrust-flash`. Do not mistake a lease from stock firmware for the
intermediate loader; the upstream process expects the loader at its fixed
conversion-network address. Do not “fix” this by editing the expected address.

Read `smarthack-wifi.log`, `smarthack-udp.log` and `smarthack-psk.log` locally.
Patched Tuya PSK firmware or a non-ESP8266 chip can be incompatible even when the
enclosure matches an earlier successful unit. The
[upstream README](https://github.com/ct-Open-Source/tuya-convert) explains known
limitations. Under this batch's policy, retire a persistently failing unit and
continue; do not initiate a new Tuya cloud registration to diagnose it.

An AWP02L-N in this batch joined the conversion AP but repeatedly presented
PSK identity version `02` with `DECRYPTION_FAILED_OR_BAD_RECORD_MAC`. The
[upstream compatibility notice](https://github.com/ct-Open-Source/tuya-convert#newer-devices)
identifies that version as patched firmware unsupported by this conversion
method. A DHCP association alone is not loader success. Stop the attempt,
retain the existing HA/client configuration, and record that no firmware was
written. Do not publish complete PSK identities or keys from the diagnostic log.

## Experimental ESP8266 alternative to Tuya-Convert

PSK 02 blocking Tuya-Convert does not establish that every wireless route is
impossible. Research checked on 2026-10-10 found Jeremy Salwen's
[ESP8266 CloudCutter write-up](https://github.com/jeremysalwen/cloudcutter-esp8266).
It describes a different vulnerability chain that replaces the device's stored
authentication keys, enabling subsequent server impersonation and conversion.

The upstream CloudCutter `esp8266` branch contains an
[initial implementation dated 2026-01-30](https://github.com/tuya-cloudcutter/tuya-cloudcutter/commit/defb7ba92a228dc8149599a54aadcd37e0e862c6).
That revision is explicitly marked as not ready for public use. Its exploit
contains fixed payload addresses; it is not a universal replacement for the
normal conversion command. No matching AWP02L-N profile or successful test on
this batch's unit has been established. The prepared ESPHome image also must
not be confused with the experimental branch's upgrade-image format.

Treat this as a candidate for firmware-specific investigation, not a confirmed
conversion path. Match the stock firmware and memory layout before adapting
the exploit, and preserve the existing HA/client bindings until an actual
replacement is verified. An explicitly accepted trial sent one experimental
packet to the identified unit in AP mode. Its connection dropped; that does not
establish successful key replacement. Authentication and conversion remain
unverified. Follow the [detailed AWP02L-N procedure](awp02l-n-psk02.md) for isolation,
identity checks, milestone evidence, image-format constraints and cleanup.

A separate [recovery anecdote](https://github.com/ct-Open-Source/tuya-convert/discussions/1177)
reports success after `vtrust-recovery` and `/undo`, but its author could not
reproduce it on other units. It does not establish a general PSK 02 bypass.

## TLS or Python exception before any flash

The container pins Python3.11 and the legacy MQTT API. Its patch imports
`sslpsk3==1.1.1` through the legacy name. Run `tests/test_psk.py` inside the built
container: it establishes a real loopback TLS1.2 session using a non-UTF-8 identity.
A passing import check alone would not establish compatibility. Do not casually
upgrade Python or the PSK dependency in this path.

## Compilation is slow

The small reference Atom host is suitable for the AP and flashing services, but
compilation can take much longer there. Use the [Mac builder workflow](workbench.md#build-on-a-faster-mac),
retain its private PlatformIO cache, and transfer only the finished image to the
Linux workbench. Keep the pinned ESPHome version and device configuration the
same. Initial toolchain downloads are separate from actual compilation time.

## ESPHome image is missing from an already open menu

Stage the image before starting a conversion when possible. If the loader menu
was already open before the image arrived, its displayed choices can be stale.
The pinned upstream script rebuilds the file list when a firmware selection is
declined at its confirmation prompt. Inspect the refreshed names and choose
`esphome-initial.bin`; never assume that an old numeric choice still means the
same file. Keep the plug powered while it is waiting in the loader.

## Final upload stalls after the loader was identified

A YM-WS-1 reached the correct loader, but its first final-image HTTP request
stalled. The web log had no recorded final-image download and the native
ESPHome API was absent. Those observations alone did not prove which bytes
had reached flash, so no automatic write retry was issued.

Stop an abandoned client request and retain its outcome as unconfirmed. Check
the native API, DHCP and loader with bounded read-only requests. Do not reset
the device while an active transfer is making progress. A fresh loader response
must match the same MAC and expected flash size before using its supported
retry path. If ESPHome already responds, verify that image and use normal OTA
for any remaining change instead of repeating the conversion write.

In this case a fresh read confirmed the original intermediate loader. The
staged final image's digest was checked again and one bounded retry completed
successfully. Encrypted API identity and compilation time then confirmed the
intended final image. Keep each write intent and result separate in private
records; a client timeout is neither success nor proof that another write is safe.

## ESPHome binary is rejected or the device disappears

Confirm size, ESP header, architecture and flash layout. Keep the first image
at or below 512 KiB. Check private Wi-Fi credentials, 2.4 GHz availability, router leases,
fallback AP presence and the OTA/API keys. Compilation is not proof of successful
flashing. A new hostname with a MAC suffix is expected. Never post the binary
publicly: it contains the credentials compiled into it.

If the loader is still reachable, follow its supported retry/revert options. If
the unit remains dead, the chosen policy is retirement rather than UART recovery.

## HA connects but the relay does not work

The first image deliberately defines no relay. Finish [GPIO identification](gpio.md).
Do not label a diagnostics-only node as a completed conversion. Wrong inversion,
an unsupported metering chip, or an invalid GPIO map requires a new local YAML.

An LED changing or HA showing `on` is not proof that the output is energized.
For the first unit, GPIO13 input events and GPIO12 state changes were visible,
but the physical output test failed. The XS-SSA01 marking then led to a matching
variant with a GPIO15 relay and an inverted GPIO12 indicator. Retract an incorrect
mapping's verified status and identify the model/output circuit before another
output test. Keep the unit out of Matter until physical switching passes. A load
that also fails directly from the wall cannot be used to establish a plug failure; check that distinction separately.

## The button switches the load, but the indicator stays dark

Check both the hardware pin and the action path. An existing ESPHome plug later
identified as YM-WS-1 had a historical GPIO2 PWM indicator in its configuration,
while the matching observed variant uses an inverted GPIO12 output. Its LED
actions also lived only in a template switch, so a physical button that toggled
the underlying GPIO relay bypassed those actions completely.

The correction uses an internal binary indicator on GPIO12 and attaches its
`light.turn_on` / `light.turn_off` actions to the GPIO relay's `on_turn_on` /
`on_turn_off` triggers. This makes both button and API control follow the same
relay state. Preserve the working relay/button pins and exposed entity identity.
Successful compilation, OTA and API readback do not establish that the corrected
LED is visibly working; record that observation separately.

## Native ESPHome control works, but HA commands have no effect

For the KMC unit, the physical button and a direct encrypted ESPHome command
worked, while HA accepted `switch.turn_on` without changing the relay state.
The device was online. Its address, MAC and relay command key matched a fresh
native API response, and the event log showed no automation reversing the
command. Reloading that one ESPHome entry did not help.

Before migrating the household role, removing and re-adding only the new
ESPHome entry restored HA control. An independent native API connection then
confirmed the HA-commanded off/on/off transitions. The exact underlying cause
was not established. Record the replacement config-entry/entity identifiers in
the private inventory; preserve the original role until control works. Do not
respond to this symptom by guessing new GPIOs or resetting the Matter bridge.

## HA works but Google/Alexa does not

Check in order: relay works in HA; entity appears in the existing bridge's selected
list; bridge is paired to the intended ecosystem; controller is online; IPv6/mDNS
and the bridge UDP port are reachable. A running Matter Server does not replace
Matter Hub. Do not reset working fabrics as an initial troubleshooting action.
If only Alexa commissioning fails, verify the bridge's 5540 port and current
commissioning window. See [the Matter guide](matter.md).

### Alexa still displays “connecting”

An added fabric is an intermediate step; confirm that the bridge also completed
commissioning. In the observed run, the bridge logged a successful
`generalCommissioning.commissioningComplete` response with `errorCode: 0` while
the Alexa app still displayed its connection screen. The operator subsequently
confirmed that all nine selected devices appeared. Once successful completion
is established, check Alexa's device list before repeating pairing or changing
the bridge. Device discovery and actual load control are separate checks.

Read the final protocol outcome rather than treating an isolated earlier log
line as proof of failure. This run included a country-code validation error
before successful commissioning. Keep the full logs private: they can contain
certificates, identifiers and commissioning material.

## Reporting a problem

Report software versions, stage, sanitized error class and the checks already
performed. Remove SSIDs, IPs, MACs, hostnames, tokens, local keys, setup codes,
device IDs and household entity names. Do not attach raw logs, packet captures,
state directories or firmware. Follow [SECURITY.md](../SECURITY.md) for a suspected
credential exposure.
