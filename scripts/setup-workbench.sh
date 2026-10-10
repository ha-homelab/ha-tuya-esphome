#!/usr/bin/env bash
set -euo pipefail
source_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
base=${WORKBENCH_ROOT:-/opt/tuya-workbench}
revision=a34b2c91862ed855542e8a32a14a9ab7573c4de9

docker info >/dev/null
sudo install -d -o "$(id -u)" -g "$(id -g)" "$base"
mkdir -p "$base"/{bin,esphome,logs,validation}
chmod 700 "$base/esphome" "$base/logs"
if [[ ! -e "$base/tuya-convert" ]]; then
  git init "$base/tuya-convert"
  git -C "$base/tuya-convert" remote add origin https://github.com/ct-Open-Source/tuya-convert.git
  git -C "$base/tuya-convert" fetch --depth 1 origin "$revision"
  git -C "$base/tuya-convert" checkout --detach FETCH_HEAD
fi
actual=$(git -C "$base/tuya-convert" rev-parse HEAD)
[[ "$actual" == "$revision" ]] || { echo 'Unexpected Tuya source revision; inspect the existing checkout.' >&2; exit 1; }
if [[ -n $(git -C "$base/tuya-convert" status --porcelain --untracked-files=no) ]]; then
  echo 'Tuya source has local modifications; inspect before building.' >&2
  exit 1
fi
install -m 0755 "$source_root"/bin/* "$base/bin/"
install -m 0644 "$source_root/tests/test_psk.py" "$base/validation/test_psk.py"
if [[ ! -e "$base/esphome/tuya-plug.yaml" ]]; then
  install -m 0644 "$source_root/examples/tuya-plug.yaml" "$base/esphome/tuya-plug.yaml"
fi
docker build --network=host -t tuya-convert:workbench \
  -f "$source_root/container/Dockerfile" "$base/tuya-convert"
docker run --rm --network none -v "$base/validation:/checks:ro" \
  tuya-convert:workbench python3 /checks/test_psk.py
docker pull ghcr.io/esphome/esphome:2026.9.1
{
  printf 'tuya-convert %s\n' "$revision"
  docker image inspect tuya-convert:workbench --format '{{.Id}}'
  docker image inspect ghcr.io/esphome/esphome:2026.9.1 --format '{{json .RepoDigests}}'
} > "$base/versions.txt"
echo "Ready for local secrets and firmware compilation in $base"
