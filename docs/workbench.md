# Workbench and firmware builder

## Requirements

A dedicated Linux host needs a wired management connection, a separate Wi-Fi
radio supporting AP mode, Docker, and sudo access. Our reference host is an
AZW Z83 II, x86-64, Debian 12, about 2 GB RAM and 28 GB eMMC. Build one firmware
at a time; the sample limits compilation to two workers. Set
`compile_process_limit: 1` if your host has less available memory.

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
  git curl ca-certificates docker.io iw rfkill python3-venv tmux usbutils util-linux
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

## Build on a faster Mac

The Linux host is required for the conversion AP, but compilation can run on a
different computer. A native Python environment on an Apple Silicon Mac avoids
running the compiler on the small Atom host. Keep the same ESPHome version on
both machines. Docker Desktop is not required for this native build.

Create a private directory **outside this repository**, then copy the local
configuration and its secrets over SSH. Substitute your own SSH target; the
example below is a placeholder. Python 3.12 must already be installed.

```sh
umask 077
mkdir -p "$HOME/Private/tuya-builder"
cd "$HOME/Private/tuya-builder"
export PLATFORMIO_CORE_DIR="$PWD/.platformio"
python3.12 -m venv .venv
.venv/bin/python -m pip install 'esphome==2026.9.1'
scp operator@flash-host:/opt/tuya-workbench/esphome/tuya-plug.yaml .
scp operator@flash-host:/opt/tuya-workbench/esphome/secrets.yaml .
chmod 600 tuya-plug.yaml secrets.yaml
```

Set `esphome.compile_process_limit: 8` in this private YAML if the Mac has
sufficient memory. Keep the Linux copy at its lower limit. Do not change the
device name, API key, Wi-Fi settings, board or flash parameters just to move the
build. The first build downloads its own ESP8266 compiler and framework; later
builds reuse the cache.

Keep `PLATFORMIO_CORE_DIR` set to this private directory for every build. ESPHome
may clear PlatformIO packages when changing Python versions; isolating this
cache prevents interference with other projects' toolchains.

```sh
.venv/bin/esphome compile tuya-plug.yaml
.venv/bin/esptool image-info \
  .esphome/build/tuya-plug/.pioenvs/tuya-plug/firmware.bin
scp .esphome/build/tuya-plug/.pioenvs/tuya-plug/firmware.bin \
  operator@flash-host:/opt/tuya-workbench/esphome/firmware-incoming.bin
```

On the Linux host, stage the transferred image using the checked-out project:

```sh
chmod 600 /opt/tuya-workbench/esphome/firmware-incoming.bin
python3 /opt/tuya-workbench/project/scripts/stage-firmware.py \
  /opt/tuya-workbench/esphome/firmware-incoming.bin
```

The staging script checks the 512 KiB first-image limit and ESP header, then
replaces the served image atomically with mode 0600. Check the actual chip and
flash layout separately. Never commit the transferred binary or build output:
both embed private credentials. After initial conversion, the same Mac can run
encrypted ESPHome OTA uploads directly to the plug on the home LAN.

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
on the host. The launcher explicitly returns the radio before removing the
container; it does not rely on namespace destruction to restore the driver. Set
`WIFI_INTERFACE`, `MANAGEMENT_INTERFACE` and `WORKBENCH_ROOT` if defaults differ.
