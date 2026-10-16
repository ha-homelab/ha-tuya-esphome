# Quality and protocol boundaries

CI runs the publication guard, shell syntax and ShellCheck, real C++ counter
regressions, bounded-staging Python CLI tests and the pinned container's real
TLS1.2 binary-identity PSK exchange. The container test also executes the patched
upstream derivation and rejects session-PSK output. It uses synthetic data and
no hardware. Device commissioning remains separate.

Legacy Tuya conversion includes MD5/CBC compatibility code required by the
upstream protocol and is not presented as a modern secure administrative
channel. Keep it on the documented isolated workbench. The resulting ESPHome
profile uses its own random API/OTA key, separate from conversion. No exhaustive
cryptographic review, full-function coverage percentage or continuity claim is
made here.

The maintainer confirms secure-design and common Python/network vulnerability
knowledge and no external-to-GitHub bug, enhancement or vulnerability reports in
the preceding 12 months. These are human attestations; public issue history and
current dependency/security findings also need review for the badge assessment.

The owned C++ energy-counter tests run with AddressSanitizer and UndefinedBehaviorSanitizer, assertions and debug symbols. CodeQL analyzes owned Python and the compiled C++ implementation on pull requests, main changes and a weekly schedule; upstream sources fetched for the container remain separate dependencies.

The [compiler dependency assessment](compiler-dependency-assessment.md) records the known Starlette advisories and why their HTTP-server preconditions are absent from the pinned command-line build profile.
