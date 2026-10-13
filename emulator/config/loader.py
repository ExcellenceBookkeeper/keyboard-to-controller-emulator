"""Config loader.

Reads `%APPDATA%/k2c/config.toml` if present, falls back to defaults.
Profile TOMLs are handled separately by ProfileService — this module
only owns global runtime config.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import tomli

from emulator.config import defaults


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    profile_dir: Path
    tick_hz: int
    deadzone: float
    trigger_threshold: float
    poll_backend: str
    pad_kind: str
    stick_curve: str
    trigger_curve: str


def _config_path() -> Path:
    appdata = os.environ.get("APPDATA")
    base = Path(appdata) if appdata else Path.home() / ".config"
    return base / "k2c" / "config.toml"


def load_config(path: Path | None = None) -> RuntimeConfig:
    cfg_path = path or _config_path()
    raw: dict = {}
    if cfg_path.is_file():
        with cfg_path.open("rb") as fh:
            raw = tomli.load(fh)
    runtime = raw.get("runtime", {})
    return RuntimeConfig(
        profile_dir=Path(runtime.get("profile_dir", defaults.DEFAULT_PROFILE_DIR)),
        tick_hz=int(runtime.get("tick_hz", defaults.DEFAULT_TICK_HZ)),
        deadzone=float(runtime.get("deadzone", defaults.DEFAULT_DEADZONE)),
        trigger_threshold=float(runtime.get("trigger_threshold", defaults.DEFAULT_TRIGGER_THRESHOLD)),
        poll_backend=str(runtime.get("poll_backend", defaults.DEFAULT_POLL_BACKEND)),
        pad_kind=str(runtime.get("pad_kind", defaults.DEFAULT_PAD_KIND)),
        stick_curve=str(runtime.get("stick_curve", defaults.DEFAULT_STICK_CURVE)),
        trigger_curve=str(runtime.get("trigger_curve", defaults.DEFAULT_TRIGGER_CURVE)),
    )