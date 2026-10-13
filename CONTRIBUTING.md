# Contributing to keyboard-to-controller-emulator

Thanks for wanting to mash keys into sticks. This project maps keyboard
input to virtual Xbox 360 / DS4 controllers on Windows using ViGEmBus as
the kernel-mode backend. Contributions are welcome — read this first.

## Dev environment

- Windows 10 21H2 / Windows 11 (x64)
- Python 3.11 or 3.12 (3.13 works, but the `vgamepad` wheel lags)
- ViGEmBus driver installed (see `docs/` — not shipped here, grab from upstream)
- Visual Studio 2022 Build Tools if you're touching `native/hook_shim`
- `pip install -r requirements.txt` then `pip install -e .`

## Running locally

```
python -m emulator.bootstrap.app --profile default --verbose
```

The tray icon appears, an overlay window shows live axis state, and the
service bus starts. Bind keys with the editor in `emulator/ui/`.

## Code layout

- `emulator/bootstrap/` — entrypoints, arg parsing, lifecycle
- `emulator/services/` — business logic (mapping, profiles, telemetry)
- `emulator/handlers/` — thin per-input-event handlers
- `emulator/adapters/` — platform glue: Win32, ViGEm, XInput, HID
- `emulator/models/` — dataclasses / pydantic schemas
- `emulator/utils/` — timers, deadzones, curve math
- `emulator/config/` — defaults, schema, migration

## Pull request rules

1. One feature per PR. No drive-by refactors.
2. Any new handler must have a unit test under `tests/`.
3. Do not add a new third-party dep without opening an issue first.
4. Deadzone / curve math changes need a before/after trace in the PR body.
5. Keep the native shim C++17-clean; MSVC `/W4` warnings are errors.

## Commit style

`service(mapping): add radial deadzone for right stick`

Scopes: `bootstrap`, `service`, `handler`, `adapter`, `model`, `util`,
`config`, `native`, `ui`, `test`, `docs`.

## Reporting bugs

Open an issue with: Windows build, Python version, ViGEmBus version, a
copy of `logs/emulator.log` around the failure, and your active profile
TOML if the bug is mapping-related.

## Community

We do not support piracy, RMT, or bypassing anti-cheat in competitive
online games. This is a hobbyist input-remapping tool. If a game bans
you for using a virtual controller, that is on you.