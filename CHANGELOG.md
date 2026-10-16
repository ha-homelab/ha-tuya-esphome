# Source change notes

Full Git commit IDs identify source snapshots. These notes do not assign new
versions or acceptance to third-party firmware or previously converted devices.

## Development changes

- Remove the pinned upstream session-PSK print from the container runtime and exercise the actual derivation with synthetic inputs.
- Bound firmware-staging input reads and reject FIFO/non-regular inputs; add
  real CLI tests for size/header failures, private output and preservation of
  an existing staged file.
- Define private security intake, contribution tests, conduct and maintainer
  responsibilities while preserving the two-approval repository rule.

## Existing source baseline

- Provide a pinned Tuya conversion runtime, isolated workbench setup, private
  ESPHome key generation and first-image staging.
- Maintain energy-counter migration code and executable C++ regressions.
- Record device-specific conversion and acceptance evidence with explicit
  unresolved tests in ROADMAP.md and docs/deployment-record.md.
