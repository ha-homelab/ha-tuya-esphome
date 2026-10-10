# AWP02L-N with patched Tuya PSK 02: experimental procedure

This is the procedure for an AWP02L-N that reaches the conversion network but
cannot complete Tuya-Convert's TLS handshake. It is an experimental investigation,
not a verified AWP02L-N conversion recipe. Follow the ordinary
[conversion guide](conversion.md) for devices that already work with Tuya-Convert.

## Status and scope

On 2026-10-10, the observed unit made ten PSK identity `02` attempts, all ending
in `DECRYPTION_FAILED_OR_BAD_RECORD_MAC`. No intermediate loader started and no
replacement firmware was transferred. A later experiment connected to the same
unit's open AP, checked its identity, and sent one 256-byte packet from the
pinned ESP8266 CloudCutter branch. The Wi-Fi connection subsequently dropped.
Neither packet delivery nor that disconnection establishes that the exploit
worked. Authentication with the replacement key and firmware installation have
not yet been verified.

The owner chose a wireless-only attempt, no factory-firmware backup, and retirement
of an unsuccessful unit rather than serial recovery. That decision is specific
to this batch. Keep the load disconnected throughout pairing and experimental
steps. The experiment may alter stored credentials even though it does not send
an ESPHome image; retaining the old HA configuration does not guarantee that
the old LocalTuya connection will still work afterward.

## 1. Identify the failure before choosing this path

1. Check the ordinary session's private Wi-Fi and PSK logs. A stock-firmware DHCP
   lease is not evidence that the intermediate loader is running.
2. Distinguish repeated PSK `02`/bad-record-MAC failures from no association, a
   missing Python dependency, or a TLS runtime crash. This procedure concerns
   the first case.
3. Save the model, source versions, failure class and whether any firmware bytes
   were served in a private per-unit record. Do not upload raw identities or logs.
4. Stop the ordinary conversion session and return its radio to the host before
   starting another session. Do not run both conversion methods on the same PHY.
5. Keep existing HA entities, automations, scripts, desktop settings and Matter
   filters in place until the replacement is working.

[Tuya-Convert's compatibility notice](https://github.com/ct-Open-Source/tuya-convert#newer-devices)
describes this limitation of its own method. It is not evidence that all later
wireless research is inapplicable.

## 2. Pin and inspect the experimental source

The [author's ESP8266 write-up](https://github.com/jeremysalwen/cloudcutter-esp8266)
explains an alternative based on changing stored authentication material. The
implementation examined here is the upstream CloudCutter `esp8266` branch at
[`defb7ba92a228dc8149599a54aadcd37e0e862c6`](https://github.com/tuya-cloudcutter/tuya-cloudcutter/commit/defb7ba92a228dc8149599a54aadcd37e0e862c6).
Upstream explicitly describes this revision as unfinished.

Create a private workspace outside this repository. These commands only fetch
and inspect source; they do not operate the plug:

```sh
umask 077
mkdir -p "$HOME/Private/awp02l-n-experiment"
cd "$HOME/Private/awp02l-n-experiment"
git clone --branch esp8266 --single-branch \
  https://github.com/tuya-cloudcutter/tuya-cloudcutter.git source
git -C source checkout --detach defb7ba92a228dc8149599a54aadcd37e0e862c6
git -C source rev-parse HEAD
git -C source status --short
```

Review `src/cloudcutter/exploit.py`, `src/cloudcutter/crypto/pskcontext.py`,
`src/cloudcutter/__main__.py`, and `src/setup_apmode.sh` before execution. The
payload uses fixed addresses. A model label, a common ESP8266 chip, or a similarly
named CloudCutter profile does not establish a matching stock-firmware layout.
No validated AWP02L-N profile has been established for this unit.

The session used a private harness around that exact upstream payload. The
harness is not part of this public repository, and `bin/tuya-convert` does not
implement this experimental path. The steps below describe the required controls
and evidence; they are not a claim that running the unmodified CloudCutter menu
will convert this model. A trial without a matched layout must be recorded as an
explicitly accepted, unverified experiment, not as a supported profile.

## 3. Prepare the host and isolate the radio

Use the wired Linux workbench from [host setup](workbench.md). The experimental
runtime also needs a station-mode DHCP client such as `udhcpc`; its Python path
uses `requests` and both `Crypto` and `Cryptodome` imports. Our derived runtime
kept Python 3.11 and sslpsk3 1.1.1, with requests 2.32.5 and pycryptodome 3.23.0.
Build dependencies before disconnecting the radio from the host.

1. Confirm that SSH management and the default route use Ethernet.
2. Create a dedicated long-lived container with `--network none`. Mount only the
   private experiment directory and run the reviewed tools there.
3. Move the dedicated Wi-Fi PHY into that container's network namespace. Bring up
   its loopback and Wi-Fi interface. Do not move the Ethernet interface.
4. Run the station DHCP client inside that namespace. A plug's built-in AP subnet
   can overlap the management LAN; do not install its route on the host.
5. Keep the container alive until the radio has explicitly been returned during
   cleanup. Record the container name, PID and numeric PHY index privately.

The existing [radio launcher](../bin/tuya-convert) demonstrates namespace entry
and PHY return for the ordinary workflow. An experimental launcher must retain
those controls while starting the experimental station/AP services instead.
Do not invoke an upstream host-network setup script on the management host.

## 4. Connect to the intended plug in AP mode

1. Disconnect the load and put this plug into **slow-blinking AP mode**. It is a
   different mode from the fast blinking used in the ordinary workflow. On this
   unit, another long button hold after fast pairing exposed its own Wi-Fi AP.
2. The phone may stay on the home network. It does not need to join
   `vtrust-flash` for this step.
3. Scan from the isolated radio and select the exact target BSSID. Compare it
   privately with the device identity recorded before the attempt. Some ESP8266
   station/AP addresses differ in the locally administered bit; do not accept
   an unrelated address just because the SSID looks like SmartLife.
4. Join that AP, obtain a DHCP lease inside the namespace, and check the connected
   BSSID again. Confirm that the gateway's neighbor entry belongs to the same
   target. Stop if identity is ambiguous or more than one target matches.
5. Save the association and lease privately. Use the observed gateway rather than
   a hard-coded household address.

## 5. Make one recorded attempt

Before network transmission, dry-run the exact source with its send function
replaced by a recorder. The pinned payload used here produced one 256-byte UDP
datagram for port 6669. Record the source revision, length and digest; unexpected
output requires inspection before proceeding.

Immediately before sending, recheck the connected BSSID and gateway identity.
Send only the reviewed payload to this plug, once, and save an attempt marker
before transmission. Keep the returned device configuration private, including
all generated or assigned keys. The harness must refuse an automatic repeat
when a prior attempt marker exists. If the process fails after transmission,
inspect the evidence rather than treating an exception as proof nothing was sent.

Keep these milestones separate:

- **Packet sent:** the local UDP send returned. The target's behavior is unknown.
- **AP disconnected or restarted:** a reaction was observed. It may be a reboot,
  a crash, or a mode change; it does not prove credential replacement.
- **Replacement-key authentication passed:** the intended physical device
  completed a TLS handshake using the expected experimental key, with a decoded
  application request. This is evidence for the bypass stage.
- **ESPHome installed:** a correctly packaged image was accepted, the same device
  rebooted, and its encrypted ESPHome API identifies the expected firmware.
- **Role migrated:** HA control and the applicable hardware checks passed before
  any production references were moved.

After a disconnection, rescan for the same device. If necessary, power-cycle only
that unloaded plug and restore AP mode; this is not authorization to resend the
exploit. Do not require an `A-` SSID as proof: the examined ESP8266 payload does
not establish that the generic CloudCutter AP-renaming behavior applies.

## 6. Validate the bypass before serving firmware

Once the same target is reachable again, configure it to join a temporary AP
inside the isolated namespace and run a server using the expected replacement
PSK. Keep this network disconnected from the Internet. Record the handshake and
decoded request without printing credentials to a public terminal transcript.
Do not offer an update image during this authentication-only check.

The branch's PSK 02 path uses the configured key directly. Its generated device
configuration is not evidence that the device actually stored those values.
An existing LocalTuya local key is also not interchangeable with a cloud TLS PSK
or authentication key. If the same bad-record-MAC failures continue, record the
bypass as unverified/failed and stop automatic attempts.

The firmware-transfer step remains unresolved for this unit. The experimental
branch validates an upgrade container, including a `55 AA 55 AA` UG format;
the prepared ESPHome image is a raw ESP8266 image beginning with `E9`.
Renaming it to `_ug.bin` does not package it correctly. Before serving anything,
establish the target's upgrade format, flash layout, size limit, checksum and
destination offsets, or use a separately verified compatible intermediate loader.
Do not send the branch's bundled test firmware solely because its filename says
ESP8266. No packaging or loader route is claimed as validated here.

## 7. Complete conversion and migration only after those gates pass

Build on the faster Mac if available, using the pinned ESPHome version and
private credentials. Keep a per-unit copy of the image and its digest; multiple
configurations can otherwise overwrite the same build output. The uninstalled
AWP02L-N candidate in this session is 428,224 bytes, but its size and successful
compilation do not establish compatibility with the experimental updater.

Published AWP02L-N variants use GPIO15 for the relay and GPIO13 for the button,
but their LEDs differ. Do not copy a WP5 indicator map based on appearance. Keep
unverified LED outputs unassigned, then follow [GPIO identification](gpio.md).

After encrypted ESPHome API access, identity verification and the agreed hardware
acceptance checks, migrate the role under one stable descriptive name and entity
ID. Update HA automations, scripts, dashboards and device/entity references;
remove only the positively identified obsolete LocalTuya device. Update both
the installed desktop client's settings and every persisted source used by its
deployment scripts. Preserve unrelated devices with similar names. Finally add
only the relay to the existing [Matter Hub](matter.md), retaining its controller
fabrics. Record any explicitly deferred checks as pending.

## 8. Clean up and record the result

Stop any experimental DHCP, DNS, HTTP, TLS and AP processes after establishing
that no firmware transfer is active. While the container still exists, lower its
Wi-Fi interface and return the numeric PHY to the host namespace. For a recorded
container PID and PHY index, the return operations are:

```sh
sudo nsenter -t "$experiment_pid" -n ip link set "$experiment_wifi" down
sudo nsenter -t "$experiment_pid" -n iw "phy#$experiment_phy_index" set netns 1
```

Verify that the host can see the radio before removing the container. Restore
managed mode if it was left in AP mode, and check that wired SSH remains reachable.
Do not destroy the namespace first and rely on the driver to recover the PHY.

Keep raw logs, DHCP data, MACs, keys, compiled images and capture files outside
Git with private permissions. Publish only the model, exact tool revision,
sanitized failure class and highest verified milestone. Update the
[deployment record](deployment-record.md) and [task list](../ROADMAP.md) without
counting an unverified experiment as a converted plug.
