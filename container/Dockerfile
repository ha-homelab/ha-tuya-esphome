FROM python:3.11-slim-bookworm@sha256:94a8fee35252d06ab75856f15f12c7bae67b10e8a6da93c7fded82b2610926cd

# Keep the legacy Tuya protocol on Python 3.11; it uses ssl.wrap_socket.
RUN apt-get update && apt-get install -y --no-install-recommends \
      bash git iw rfkill dnsmasq hostapd screen curl mosquitto haveged \
      net-tools openssl libssl-dev build-essential sudo coreutils grep \
      iproute2 iputils-ping procps ncurses-bin ca-certificates \
    && rm -rf /var/lib/apt/lists/*
# This named context contains only our reviewed container dependency files.
COPY --from=workbench-locks requirements-build.lock requirements-runtime.lock /opt/dependencies/
RUN pip install --no-cache-dir --require-hashes --only-binary=:all: -r /opt/dependencies/requirements-build.lock \
    && pip install --no-cache-dir --require-hashes --no-build-isolation \
      --only-binary=:all: --no-binary=paho-mqtt,sslpsk3 -r /opt/dependencies/requirements-runtime.lock

COPY . /usr/bin/tuya-convert
WORKDIR /usr/bin/tuya-convert
# sslpsk3's 1.x API supports Tuya's binary PSK identity on Python 3.11.
RUN sed -i 's/^import sslpsk$/import sslpsk3 as sslpsk/' scripts/psk-frontend.py
# Session PSKs are protocol secrets, never diagnostic output.
RUN python -c 'from pathlib import Path; p = Path("scripts/psk-frontend.py"); s = p.read_text(); old = "print(\"PSK: %s\" % hexlify(psk).decode())"; assert s.count(old) == 1; p.write_text(s.replace(old, "pass  # Session PSK deliberately not logged"))'
# The operator explicitly chose to skip stock firmware backups. Keep only
# session logs/device metadata in the directory the upstream calls backups.
RUN sed -i \
      -e 's|if ! curl -JOm 90 http://[0-9.]*/backup; then|if ! true; then|' \
      -e 's/Fetching firmware backup/Skipping firmware backup at operator request/' \
      start_flash.sh
RUN ! grep -Eq 'curl.*http://.*/backup' start_flash.sh \
    && grep -q '^import sslpsk3 as sslpsk$' scripts/psk-frontend.py
ENV TERM=xterm
CMD ["bash", "./start_flash.sh"]
