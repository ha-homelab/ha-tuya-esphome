# Source versions and maintenance

The full Git commit SHA identifies each source snapshot. Clone/download that
revision from GitHub over verified HTTPS and record it with the separate pinned
upstream Tuya commit and ESPHome version. Never disable certificate validation.
[CHANGELOG.md](CHANGELOG.md) records source changes; it does not create new
upstream firmware versions or retroactively accept untested hardware.

Use reviewed pull requests with the independent approvals required by the current
branch rules, resolved findings and passing checks. Preserve the baseline container PSK test, ShellCheck, C++
energy regressions and Python staging tests. New major functionality requires
automated tests and documentation. Include known CVE/GHSA identifiers and upgrade
instructions with security fixes. Do not overwrite published source identity.

Workbench setup needs a supported Linux host, Docker and a dedicated Wi-Fi
interface; follow [the setup guide](docs/workbench.md). Installing a newer
workbench source does not authorize flashing a device. Preserve private local
configuration and investigate pinned-source changes before rerunning setup.
Rollback uses a previously reviewed source and compatible private configuration.
Physical relay/boot/measurement acceptance remains device-specific and must not
be inferred from compilation, the badge or another similar enclosure.

Generated firmware, logs and credentials are private. Release only public source
and synthetic test artifacts. Account/access continuity is currently not assured
within one week; [governance](GOVERNANCE.md) records this limitation.
