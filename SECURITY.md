# Security and private data

Do not post credentials or raw operational artifacts in an issue or pull request.
Report suspected vulnerabilities privately through GitHub's **Report a
vulnerability** feature for this repository. If unavailable, do not fall back to
posting secrets publicly; contact a repository maintainer through a private channel.

Excluded material includes Wi-Fi SSIDs/passwords, API/OTA keys, Home Assistant
tokens, Matter QR/manual codes and fabrics, MACs/device identifiers, household
entities, real hostnames/IPs, logs, packet captures, Terraform state, and compiled
firmware. ESPHome binaries embed secrets even when their filenames look harmless.

Examples use documentation addresses and placeholder names. Generate real keys
locally with `scripts/create-secrets.py`; never copy an example key into production.
Keep session folders private. Review both the working tree and Git history before
publishing. `.gitignore` is not a secret scanner.

Docker access is privileged. The conversion container requires the Wi-Fi radio
and network-administration capabilities, so run this on a dedicated trusted
workbench. It receives a temporary network namespace and no Ethernet interface.
The normal ESPHome CLI uses host networking for LAN OTA access; do not expose its
dashboard publicly.

If a credential leaks, revoke/rotate it first and assess affected device firmware
and Matter fabrics. Removing the current file does not erase public Git history.
Never rotate unrelated household credentials or reset fabrics merely to exercise
this project's tests.
