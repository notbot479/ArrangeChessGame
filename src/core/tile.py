"""Tile representation for the chess board."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import pygame as pg

from src.config.constants import Colors

if TYPE_CHECKING:
    from src.ui.sprite_manager import SpriteManager

Color = tuple[int, int, int]


@dataclass
class Tile:
    """Represents a single tile on the chess board."""

    x: float
    y: float
    width: float
    height: float
    tile_id: tuple[int, int] = (0, 0)
    color: Color = field(default_factory=lambda: Colors.WHITE)
    figure: str = ""

    @property
    def rect(self) -> pg.Rect:
        """Get pygame Rect for this tile."""
        return pg.Rect(self.x, self.y, self.width, self.height)

    @property
    def size(self) -> tuple[int, int]:
        """Get tile size as integer tuple."""
        return int(self.width), int(self.height)

    @property
    def center(self) -> tuple[float, float]:
        """Get center point of the tile."""
        return self.x + self.width / 2, self.y + self.height / 2

    def contains_point(self, x: float, y: float) -> bool:
        """Check if a point is within this tile's bounds."""
        return (
            self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        )

    def draw(self, surface: pg.Surface, sprite_manager: "SpriteManager") -> None:
        """Draw the tile and its figure to the surface."""
        pg.draw.rect(surface, self.color, self.rect)

        sprite_name = self.figure if self.figure else "empty"
        sprite = sprite_manager.get_scaled(sprite_name, self.size)
        surface.blit(sprite, self.rect)

    def reset_color(self) -> None:
        """Reset tile to its natural chess board color."""
        self.color = self.calculate_chess_color(*self.tile_id)

    @staticmethod
    def calculate_chess_color(col: int, row: int) -> Color:
        """Calculate alternating chess board color for position."""
        if (col + row) % 2 == 0:
            return Colors.WHITE
        return Colors.BLACK
