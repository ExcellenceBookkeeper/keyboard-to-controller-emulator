"""Virtual pad state — the single source of truth the adapters push.

Kept mutable and cheap to update: the mapping service writes into it at
tick rate (default 250 Hz), the ViGEm adapter reads it and submits a
report. No allocation per tick.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PadState:
    left_x: float = 0.0
    left_y: float = 0.0
    right_x: float = 0.0
    right_y: float = 0.0
    left_trigger: float = 0.0
    right_trigger: float = 0.0
    buttons: set[str] = field(default_factory=set)
    dirty: bool = True

    def set_axis(self, axis: str, value: float) -> None:
        clamped = max(-1.0, min(1.0, value))
        if getattr(self, axis.lower()) != clamped:
            setattr(self, axis.lower(), clamped)
            self.dirty = True

    def set_trigger(self, trigger: str, value: float) -> None:
        attr = "left_trigger" if trigger == "LT" else "right_trigger"
        clamped = max(0.0, min(1.0, value))
        if getattr(self, attr) != clamped:
            setattr(self, attr, clamped)
            self.dirty = True

    def set_button(self, button: str, pressed: bool) -> None:
        if pressed and button not in self.buttons:
            self.buttons.add(button)
            self.dirty = True
        elif not pressed and button in self.buttons:
            self.buttons.discard(button)
            self.dirty = True