"""Default runtime configuration.

Values here are the fallback when no user TOML is present. Do not put
machine-specific paths in this module — those belong in user_profile.toml.
"""

from __future__ import annotations

from pathlib import Path

DEFAULT_PROFILE_DIR: Path = Path.home() / ".config" / "k2c" / "profiles"
DEFAULT_TICK_HZ: int = 250
DEFAULT_DEADZONE: float = 0.08
DEFAULT_TRIGGER_THRESHOLD: float = 0.15
DEFAULT_POLL_BACKEND: str = "win32_rawinput"
DEFAULT_PAD_KIND: str = "xbox360"

# Curve preset names — resolved in emulator.utils.curves
DEFAULT_STICK_CURVE: str = "linear"
DEFAULT_TRIGGER_CURVE: str = "linear"

# Telemetry
TELEMETRY_WINDOW_SECONDS: int = 30
TELEMETRY_MAX_SAMPLES: int = 250 * 30