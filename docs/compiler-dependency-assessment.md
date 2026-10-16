# Compiler dependency assessment — 2026-10-16

The supported command-line compiler is ESPHome 2026.9.1 with PlatformIO Core
6.1.19 on Python 3.12. Its dependency constraints install Starlette 0.52.1,
which has the following known advisories. This is not a clean whole-environment
scan and no dependency-scanner suppression is installed.

- [GHSA-82w8-qh3p-5jfq](https://github.com/advisories/GHSA-82w8-qh3p-5jfq) (2026-06-15, high): Starlette: request.form() limits silently ignored for application/x-www-form-urlencoded enable DoS.
- [GHSA-86qp-5c8j-p5mr](https://github.com/advisories/GHSA-86qp-5c8j-p5mr) (2026-06-04, medium): Starlette has missing Host header validation that poisons request.url.path, bypassing path-based security checks.
- [GHSA-jp82-jpqv-5vv3](https://github.com/advisories/GHSA-jp82-jpqv-5vv3) (2026-06-15, low): Starlette: Unvalidated request path concatenated into authority poisons request.url.hostname.
- [GHSA-wqp7-x3pw-xc5r](https://github.com/advisories/GHSA-wqp7-x3pw-xc5r) (2026-06-15, high): Starlette: SSRF and NTLM credential theft via UNC paths in StaticFiles on Windows.
- [GHSA-x746-7m8f-x49c](https://github.com/advisories/GHSA-x746-7m8f-x49c) (2026-06-15, medium): Starlette: Arbitrary HTTP method dispatched to `HTTPEndpoint` attributes via `getattr`.

All five require incoming HTTP requests processed by Starlette. The supported
`esphome config` / `esphome compile` / serial-upload workflow does not start
PlatformIO Home, the ESPHome dashboard, or another ASGI service. In particular:

- [ESPHome toolchain.py](https://github.com/esphome/esphome/blob/0b2b16e664ecfc0add37f3435db1c2140b8a687e/esphome/platformio/toolchain.py)
  selects the PlatformIO `run -d` command through its runner.
- [PlatformIO cli.py](https://github.com/platformio/platformio-core/blob/15b8859aee4731fe4c5c6b06f74972535601eeb2/platformio/cli.py)
  lazily imports the selected command. The `run` command does not select Home.
- [Home's separate server entry point](https://github.com/platformio/platformio-core/blob/15b8859aee4731fe4c5c6b06f74972535601eeb2/platformio/home/cli.py)
  invokes [home/run.py](https://github.com/platformio/platformio-core/blob/15b8859aee4731fe4c5c6b06f74972535601eeb2/platformio/home/run.py),
  where the ASGI application and Uvicorn listener are created.
- [compat.py](https://github.com/platformio/platformio-core/blob/15b8859aee4731fe4c5c6b06f74972535601eeb2/platformio/compat.py)
  imports `starlette.concurrency` only as a Python-before-3.9 fallback; the
  supported Python 3.12 environment uses `asyncio.to_thread` instead.

The installed versions of those source files were byte-compared with these
immutable upstream revisions. A real runner `run --help` import trace contained
no Starlette, PlatformIO Home or ESPHome dashboard module. Complete synthetic
firmware compilation and invalid-key rejection also passed. Partial subprocess
traces during compilation agreed with the source graph; they are not claimed
as exhaustive dynamic coverage.

The vulnerable HTTP handlers are therefore not reachable in this command-line
profile. Do not reuse this assessment for PlatformIO Home, ESPHome dashboard,
Python below 3.9, a different dependency version, or an independently exposed
HTTP service. Reassess these advisories when any of those assumptions changes.
Retain the compiler constraints until an upstream-supported dependency update
has been validated; replacing Starlette with a version outside PlatformIO's
constraints without testing is not an established remediation.
