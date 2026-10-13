"""Canonical input event flowing through the service bus.

The Win32 adapter emits these; handlers consume them; nothing downstream
cares whether the origin was a physical keyboard, a macro, or a replay.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EventKind(str, Enum):
    KEY_DOWN = "key_down"
    KEY_UP = "key_up"
    TICK = "tick"
    SHUTDOWN = "shutdown"


@dataclass(frozen=True, slots=True)
class InputEvent:
    kind: EventKind
    scancode: int = 0
    vk_code: int = 0
    timestamp_ns: int = 0
    modifiers: frozenset[str] = frozenset()

    @property
    def is_press(self) -> bool:
        return self.kind is EventKind.KEY_DOWN

    @property
    def is_release(self) -> bool:
        return self.kind is EventKind.KEY_UP