"""Pydantic schema for profile TOML.

Anything loaded from disk is validated against these models before it
touches the mapping engine. Unknown keys are rejected — this is the
first line of defense against a malformed or hostile profile.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class KeyChord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    keys: tuple[str, ...] = Field(min_length=1, max_length=4)

    @field_validator("keys")
    @classmethod
    def _lowercase(cls, v: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(k.lower() for k in v)


class AxisBinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    axis: str = Field(pattern=r"^(LS|RS)_(X|Y)$")
    positive: KeyChord | None = None
    negative: KeyChord | None = None
    curve: str = "linear"
    deadzone: float | None = None


class TriggerBinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trigger: str = Field(pattern=r"^(LT|RT)$")
    key: KeyChord
    curve: str = "linear"
    threshold: float | None = None


class ButtonBinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    button: str = Field(pattern=r"^[A-Z][A-Z0-9_]{1,15}$")
    key: KeyChord
    turbo_hz: int | None = Field(default=None, ge=1, le=30)


class ProfileSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=48)
    pad_kind: str = Field(default="xbox360", pattern=r"^(xbox360|dualshock4)$")
    tick_hz: int = Field(default=250, ge=60, le=1000)
    axes: list[AxisBinding] = Field(default_factory=list)
    triggers: list[TriggerBinding] = Field(default_factory=list)
    buttons: list[ButtonBinding] = Field(default_factory=list)