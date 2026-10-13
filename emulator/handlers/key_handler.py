"""Translates raw key events into axis/button mutations.

This handler owns no state beyond the active key set. It is the only
place that knows how a KeyChord matches against live modifiers.
"""

from __future__ import annotations

from emulator.models.input_event import InputEvent
from emulator.models.pad_state import PadState
from emulator.services.mapping_service import MappingService


class KeyHandler:
    def __init__(self, mapping: MappingService) -> None:
        self._mapping = mapping
        self._active: set[str] = set()

    def handle(self, event: InputEvent, state: PadState) -> None:
        if event.is_press:
            self._active.add(self._key_name(event))
        elif event.is_release:
            self._active.discard(self._key_name(event))
        else:
            return
        self._mapping.recompute(self._active, event.modifiers, state)

    @staticmethod
    def _key_name(event: InputEvent) -> str:
        return f"vk:{event.vk_code:02x}"
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>