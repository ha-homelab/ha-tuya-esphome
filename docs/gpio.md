# GPIO and final device configuration

Do not infer a pin map from a plastic enclosure. The batch's first image is
GPIO-neutral specifically because the operator cannot distinguish the unboxed
models. `esp01_1m` is a compiler board selection, not a verified hardware model.

## Historical AWP04L candidate

A previous, working household configuration had:

- Relay: GPIO12; startup state `ALWAYS_OFF`.
- Button: GPIO13, inverted; pressing toggled the relay.
- Red LED: GPIO0, inverted; blue LED: GPIO15, inverted.
- Metering candidate: HLW8012-compatible driver, inverted select on GPIO3,
  CF on GPIO5, CF1 on GPIO14. The older notes suggested BL0937 hardware.

This map is a **reference for identification**, not a configuration approved for
every unit. Do not copy the old unit's current/voltage calibration coefficients.
They do not establish the new unit's accuracy or even its metering chip.

## Verification sequence

1. Confirm stable Wi-Fi, API and OTA first.
2. Read visible markings and compare a model-specific source if available. Keep
   any photos or serial markings local until sanitized.
3. Work on one unloaded unit. Add only a relay candidate and an explicit
   `restore_mode: ALWAYS_OFF` after evidence supports that pin. Do not bulk-sweep
   GPIOs, drive supply pins, or enable an assumed metering interface.
4. Toggle it from Home Assistant, verify physical switching, then reboot and
   confirm the off state. Stop if behavior is inconsistent.
5. Add and verify the button; check that its polarity and boot behavior are correct.
6. Add LEDs and metering separately. Validate metering against a reference before
   relying on power values for automation.
7. Give the relay an appropriate plug/switch device class and a stable entity ID.
   Record a sanitized, verified model profile only after these checks pass.

Physical validation remains necessary: successful compilation says nothing about
which pin controls a real relay. The owner chose to retire unsuccessful units;
serial recovery and live-board probing are not part of this project.
