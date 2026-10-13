# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.6.x   | yes       |
| 0.5.x   | security-only |
| < 0.5   | no        |

## Reporting a vulnerability

Email `security@keyboard-to-controller-emulator.dev` (PGP key in
`docs/pgp.txt` — not shipped in this tree). Do not open a public issue
for anything involving: arbitrary code execution via profile TOML,
driver-level privilege escalation, or a crafted `.kbm` recording that
crashes the service bus.

Expect an initial response within 72 hours. We will credit you in the
release notes unless you ask otherwise.

## Scope

In scope:
- `emulator/services/` — mapping engine, profile loader
- `emulator/adapters/vigem_adapter.py` — driver handshake
- `emulator/adapters/win32_input.py` — raw input hook
- `native/hook_shim/` — C++ low-level keyboard hook

Out of scope:
- ViGEmBus itself (report upstream)
- Any anti-cheat interaction — we do not test against, and do not
  support use against, anti-cheat protected titles
- Third-party profiles you downloaded from a Discord

## Threat model

The profile TOML loader treats profile files as untrusted. No eval, no
dynamic import, no shell. If you find a way to get code execution from
a profile, that's a valid CVE.