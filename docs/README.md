# Documentation

Operating notes for converting Tuya-based Wi-Fi plugs and switches to ESPHome with a
pinned `tuya-convert` revision, an isolated-radio launcher and a local firmware builder.
Every procedure separates observed facts from unverified expectations and requires
electrically isolated serial access before any mains-powered device is opened.

## Start here

- [Hardware and scope](hardware.md) — the current batch, what the labels do and do not establish, and the identification policy.
- [Workbench and firmware builder](workbench.md) — the dedicated Linux host, isolated radio, Docker requirements and private secret generation.
- [Convert one plug](conversion.md) — building the first GPIO-neutral image and running the conversion access point.
- [GPIO and final device configuration](gpio.md) — assigning relay, button and indicator pins only after controlled output checks.
- [Browser USB installation](browser-install.md) — compiling in ESPHome Device Builder and flashing from ESPHome Web without a local toolchain.

## Device records

- [SWP1-PW2-V5 / TYWE3S](swp1-pw2-v5.md) — the verified serial conversion, confirmed pin map and factory backup that identified them.
- [AWP02L-N with patched Tuya PSK 02](awp02l-n-psk02.md) — an experimental procedure for a unit that could not complete the Tuya-Convert handshake.
- [GREFIC CZ-U201](grefic-cz-u201.md) — an owner-reported two-outlet ESP8266 variant that accepted the ordinary handshake.
- [KMC 30608 Smart Tap](kmc-30608.md) — conversion plus metering calibration and per-sample acceptance for a three-outlet strip.
- [RMD-SS01S00A / TYWE3S wall switch](rmd-ss01.md) — a wall switch conversion with encrypted API control, OTA and HA migration.
- [Supernight CV01](supernight-cv01.md) — a two-outlet metered plug identified by FCC ID and converted with Tuya-Convert.
- [XS-SSA05 metered plug](xs-ssa05.md) — the metered plug sample whose encrypted native API matched the loader identity.
- [TanTan WP3](wp3-migration.md) — identification of a LocalTuya light entity and its migration to an ESPHome relay switch.
- [ME201W / CBU preparation](me201w-cbu-preparation.md) — the BK7231N water-level sensor and its wired UART preparation, not yet converted.
- [ME201W / CBU: подготовка к проводной прошивке](me201w-cbu-preparation.ru.md) — the Russian edition of the same preparation record.

## Migration and integration

- [Tasmota SP20 to ESPHome with metering continuity](tasmota-sp20-migration.md) — carrying Tasmota metering calibration and cumulative counters into ESPHome.
- [Existing NAS Matter bridge → Google Home and Amazon Alexa](matter.md) — reusing an existing Matter hub and filtering relay entities for voice assistants.

## Operations and evidence

- [Troubleshooting by stage](troubleshooting.md) — container startup, package installation, radio, handshake and flashing failures in the order they appear.
- [Anonymized deployment record](deployment-record.md) — the dated record of what was observed on the reference host, with private details omitted.
- [Quality and protocol boundaries](quality.md) — which CI checks use synthetic data and why legacy protocol compatibility code is not modern security.
- [Encrypted USB provisioning profile](security-profile.md) — provisioning a verified ESP8266 profile over trusted serial access with encrypted API and OTA afterwards.
- [CI dependency updates](ci-dependency-updates.md) — the Renovate preset, SHA-pin comments and the rules for reviewing grouped dependency changes.
- [Compiler dependency assessment](compiler-dependency-assessment.md) — the advisories in the pinned ESPHome and PlatformIO dependency set as of 2026-10-16.

## SWP1-PW2-V5 translations

The verified serial conversion guide in the other supported languages. Every edition
links back to the English source.

- [العربية](swp1-pw2-v5.ar.md)
- [বাংলা](swp1-pw2-v5.bn.md)
- [Čeština](swp1-pw2-v5.cs.md)
- [Deutsch](swp1-pw2-v5.de.md)
- [Español](swp1-pw2-v5.es.md)
- [فارسی](swp1-pw2-v5.fa.md)
- [Français](swp1-pw2-v5.fr.md)
- [עברית](swp1-pw2-v5.he.md)
- [हिन्दी](swp1-pw2-v5.hi.md)
- [Bahasa Indonesia](swp1-pw2-v5.id.md)
- [Italiano](swp1-pw2-v5.it.md)
- [日本語](swp1-pw2-v5.ja.md)
- [한국어](swp1-pw2-v5.ko.md)
- [Nederlands](swp1-pw2-v5.nl.md)
- [Polski](swp1-pw2-v5.pl.md)
- [Português](swp1-pw2-v5.pt.md)
- [Русский](swp1-pw2-v5.ru.md)
- [ไทย](swp1-pw2-v5.th.md)
- [Türkçe](swp1-pw2-v5.tr.md)
- [Українська](swp1-pw2-v5.uk.md)
- [Tiếng Việt](swp1-pw2-v5.vi.md)
- [简体中文](swp1-pw2-v5.zh-Hans.md)
- [繁體中文](swp1-pw2-v5.zh-Hant.md)
