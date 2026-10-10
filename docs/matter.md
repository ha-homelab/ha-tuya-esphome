# Existing NAS Matter bridge → Google Home and Amazon Alexa

## Use the existing owner

The inspected installation already has **RiDDiX Home Assistant Matter Hub** and
**Home Assistant Matter Server** running in the `ha-infra` namespace on a NAS-backed
k3s worker. The hub uses a dedicated LAN interface named `net1`. Its health endpoint
responded successfully. This project reused that instance, added an exact relay
entity filter for each of eight converted plugs. Seven passed per-unit physical
checks; the latest WP5 reused the established profile with those checks explicitly
waived by the operator. The original two fabrics were preserved when Alexa was
commissioned, and all three were preserved when later plugs were added. No new
bridge or factory reset was used.

Use the current hub's private Web UI endpoint and persistent storage. An older
Portainer stack or a dormant alternative manifest is not evidence that it is the
active owner. Do not run two processes against the same bridge identity/storage.
See the anonymized [deployment record](deployment-record.md).

The path is **ESPHome native API → Home Assistant relay entity → Matter Hub →
Google/Amazon controller**. The separate Matter Server and its WebSocket API are
used when Home Assistant itself controls Matter devices. They do not export
arbitrary HA entities. See [Home Assistant's Matter documentation](https://www.home-assistant.io/integrations/matter/).

## Select entities deliberately

First finish the physical relay/button checks in [GPIO identification](gpio.md).
The initial diagnostic-only firmware has no useful controllable plug to export.

In Home Assistant, create a dedicated entity label such as `matter_plugs` and add
it only to the verified relay entities. In the existing Hub UI, review the bridge's
current include/exclude filters before changing them. Add an `entity_label` filter
for that label, preserving unrelated rules. Check the resulting entity list before
saving. Reload/restart the bridge as required by the installed version after label
changes. Avoid broad filters that unexpectedly publish every household entity.

For a single verified unit, an exact `pattern` filter containing only its relay
entity ID is also suitable. Preserve the existing filters and add that one entry;
do not replace the filter list with a broad `switch.*` rule.

### Replace an existing household role

Identify the old HA device and the new ESPHome device from their private registry
records before reusing a name. Decide whether the old device should be removed or
retained with an explicit `_old` name. Keep a retained entity's original domain;
renaming an old `light` does not convert it into a `switch`.

Assign the new relay its intended stable entity ID before exporting it. Update
active automation, scene, dashboard, floorplan and customization references, plus
external clients and their saved deployment inputs. A change from a `light` to a
`switch` also needs the correct service domain in explicit service calls. Check
that a later deployment or application restart cannot restore the old references.

When several numbered legacy devices are being consolidated into one role,
confirm the complete retirement list with the operator. Inspect the behavior of
every referring automation before changing its target: an old motion-triggered
outlet action must not silently become a command to the replacement curtain
power outlet. Remove obsolete actions explicitly while preserving unrelated
actions, schedule times, delays and conditions. Consolidate duplicate client
controls as well as entity IDs, then verify the saved settings after a normal
save and application restart.

If a plug is already exported, inspect the installed Hub's identity-preserving
rename behavior before changing its HA ID or filter. Record and compare its
endpoint and the bridge's existing fabrics afterward. Reusing a friendly name
alone does not prove continuity. Keep only the intended primary relay in the
filter, avoid duplicate old/new controls, and verify each controller after the
migration without resetting the bridge.

For Alexa, keep the intended bridge on UDP **5540**; the maintained project's
guide identifies this as the reliable port. Do not create a second bridge on an
already-bound address/port. Follow the version-specific
[bridge configuration guide](https://riddix.github.io/home-assistant-matter-hub/getting-started/bridge-configuration).

## Google Home

Have a supported, online Google Matter hub in the same home and a current Google
Home app. The phone assists commissioning; it does not replace the always-on
controller. Google's [Matter preparation guide](https://support.google.com/googlehome/answer/12391458?hl=en)
lists current hub requirements.

Open the existing bridge's commissioning window, then use Google Home's Add
device/Matter flow with the bridge's live QR or manual code. Assign the resulting
plug entities to the desired rooms. If the bridge is already paired with Google,
first check whether the new selected entities appear; do not reset the whole
bridge merely to add a plug.

## Amazon Echo / Alexa

Use an online Matter-capable Echo/eero and the Alexa app registered to the intended
home/account. Open a commissioning window for the same bridge, select Add Device
and the Matter flow in Alexa, then use the currently displayed code. If already
paired, verify the added endpoints before attempting another commissioning.
See [Amazon's Matter integration overview](https://www.developer.amazon.com/docs/alexaplus/smarthome/matter-support.html).

To add a second ecosystem, use the bridge's additional-controller commissioning
or Matter sharing/multi-admin flow. Preserve the first ecosystem's fabric. A code
from an expired window or a factory QR is not automatically valid for every later
pairing. Keep all QR codes, manual codes and fabric identifiers private.

## Network and acceptance checks

The bridge's LAN interface needs working local IPv6 and multicast discovery.
mDNS uses UDP 5353; Matter uses its configured UDP port, normally 5540. An HTTP UI
on TCP 8482 being reachable does not prove the IPv6 Matter path works. In this
installation, an ordinary overlay-only pod interface is not a substitute for the
dedicated LAN interface. Keep phone, controller and advertised bridge addresses
mutually reachable and check wireless client isolation and VLAN policy.
Use the maintained [connectivity troubleshooting guide](https://riddix.github.io/home-assistant-matter-hub/guides/connectivity-issues).

Acceptance is a physical round trip: toggle in Google, verify relay and HA state;
toggle in Alexa, verify both other views; press the plug's button and verify all
views again. Test a plug restart and a bridge restart. Record each ecosystem's
result separately. Do not claim success from a running pod alone.

This ESP8266 Wi-Fi path needs no Thread radio. Existing Thread deployments are
separate. Avoid exposing the same plug through both Matter and another cloud
integration unless duplicate devices are intentional. Only selected on/off
control is the initial target; metering support depends on the bridge/controller.
