FROM python:3.11-slim-bookworm

# Keep the legacy Tuya protocol on Python 3.11; it uses ssl.wrap_socket.
RUN apt-get update && apt-get install -y --no-install-recommends \
      bash git iw rfkill dnsmasq hostapd screen curl mosquitto haveged \
      net-tools openssl libssl-dev build-essential sudo coreutils grep \
      iproute2 iputils-ping procps ncurses-bin ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir \
      paho-mqtt==1.6.1 tornado==6.5.10 sslpsk3==1.1.1 pycryptodomex==3.23.0

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
