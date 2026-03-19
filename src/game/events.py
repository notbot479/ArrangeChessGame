"""Event handling for the game."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

import pygame as pg


class EventType(Enum):
    """Types of game events."""

    QUIT = auto()
    CLICK = auto()
    RESIZE = auto()
    NONE = auto()


@dataclass
class GameEvent:
    """Represents a processed game event."""

    type: EventType
    position: Optional[tuple[int, int]] = None


class EventHandler:
    """Processes pygame events into game events."""

    @staticmethod
    def process_events() -> list[GameEvent]:
        """Process all pending pygame events."""
        events = []

        for event in pg.event.get():
            game_event = EventHandler._process_single_event(event)
            if game_event.type != EventType.NONE:
                events.append(game_event)

        return events

    @staticmethod
    def _process_single_event(event: pg.event.Event) -> GameEvent:
        """Process a single pygame event."""
        if event.type == pg.QUIT:
            return GameEvent(type=EventType.QUIT)

        if event.type == pg.MOUSEBUTTONDOWN:
            return GameEvent(
                type=EventType.CLICK,
                position=pg.mouse.get_pos(),
            )

        if event.type == pg.WINDOWRESIZED:
            return GameEvent(type=EventType.RESIZE)

        return GameEvent(type=EventType.NONE)
