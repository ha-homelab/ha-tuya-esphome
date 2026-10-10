# Linux workbench

## Requirements

A dedicated Linux host needs a wired management connection, a separate Wi-Fi
radio supporting AP mode, Docker, and sudo access. Our reference host is an
AZW Z83 II, x86-64, Debian 12, about 2 GB RAM and 28 GB eMMC. Build one firmware
at a time; the sample sets `compile_process_limit: 1`.

On the router, reserve the host's **Ethernet** MAC under a free hostname and IP.
Check current DHCP leases, static reservations, local DNS and neighbors first.
Use your actual values privately; these are documentation-only examples:

```sh
uci set dhcp.flash_host=host
uci set dhcp.flash_host.name='flash-host'
uci set dhcp.flash_host.mac='02:00:00:00:00:01'
uci set dhcp.flash_host.ip='192.0.2.10'
uci set dhcp.flash_host.dns='1'
uci set dhcp.flash_host.leasetime='infinite'
uci commit dhcp
/etc/init.d/dnsmasq reload
```

The example address is not suitable for a real LAN. Keep the Linux NIC configured
for DHCP so the router remains the address authority. On Debian with ifupdown,
ensure an `iface <ethernet> inet dhcp` stanza actually exists; an `auto` line alone
does not configure the interface. Validate DNS and a second SSH connection before
closing the first session. Do not restart an entire household network to add a
reservation.

## Install

```sh
sudo apt-get update
sudo apt-get install --no-install-recommends \
  git curl ca-certificates docker.io iw rfkill python3-venv tmux usbutils
sudo systemctl enable --now docker
sudo usermod -aG docker,dialout "$USER"
# Open a new login session to acquire the groups.
bash scripts/setup-workbench.sh
python3 scripts/create-secrets.py /opt/tuya-workbench/esphome/secrets.yaml
```

The setup script pins the Tuya source commit, builds the compatibility container,
pulls ESPHome 2026.9.1, and installs launchers under `/opt/tuya-workbench/bin`.
It does not flash anything, overwrite an existing checkout, or create Wi-Fi keys.
Review the sample `.home.arpa` domain and adjust it to the private LAN locally.

## Reference Broadcom repair

The reference host's BCM4345/6 radio initially had no interface. Kernel messages
reported a missing board-specific NVRAM text file, followed by a clock timeout.
The existing firmware binary alone was insufficient. An exact AZW Z83 II NVRAM
file from the [Volumio platform repository](https://github.com/volumio/platform-x86)
restored the radio after reloading `brcmfmac`.

Source revision: `6fdb6b680b0bd3b2d2b4bdc7cacdb006736e0c23`;
archive: `packages-buster/firmware-brcm-sdio-nvram/broadcom-nvram.tar.xz`;
member basename: `brcmfmac43455-sdio.AZW-Z83 II.txt`;
file SHA-256: `c029bda9fe18c5de707811efdb28de75c43e5cf9be72ec85a66c3d845d8f2d40`.

Install board-specific data only on matching hardware. Do not substitute arbitrary
radio calibration files. Set the runtime regulatory region to your actual country.
Reloading the Wi-Fi driver is appropriate only when management uses Ethernet.

## Check the radio

```sh
sudo iw dev
sudo iw phy phy0 info
sudo rfkill list
ip route
```

The launcher passes the whole Wi-Fi PHY into a temporary container network
namespace. Its DHCP, DNS, MQTT and HTTP services operate there. The wired NIC stays
on the host. Exiting the container returns the radio to the host. Set
`WIFI_INTERFACE`, `MANAGEMENT_INTERFACE` and `WORKBENCH_ROOT` if defaults differ.
