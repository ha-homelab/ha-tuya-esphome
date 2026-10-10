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

## HA works but Google/Alexa does not

Check in order: relay works in HA; entity appears in the existing bridge's selected
list; bridge is paired to the intended ecosystem; controller is online; IPv6/mDNS
and the bridge UDP port are reachable. A running Matter Server does not replace
Matter Hub. Do not reset working fabrics as an initial troubleshooting action.
If only Alexa commissioning fails, verify the bridge's 5540 port and current
commissioning window. See [the Matter guide](matter.md).

## Reporting a problem

Report software versions, stage, sanitized error class and the checks already
performed. Remove SSIDs, IPs, MACs, hostnames, tokens, local keys, setup codes,
device IDs and household entity names. Do not attach raw logs, packet captures,
state directories or firmware. Follow [SECURITY.md](../SECURITY.md) for a suspected
credential exposure.
