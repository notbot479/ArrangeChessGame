"""Game rendering utilities."""

from typing import Optional

import pygame as pg

from src.config.constants import Colors
from src.core.board import ChessBoard
from src.ui.sprite_manager import SpriteManager
from src.ui.sidebar import FigureSelectionBar


class GameRenderer:
    """Handles all game rendering operations."""

    def __init__(
        self,
        surface: pg.Surface,
        sprite_manager: SpriteManager,
    ):
        """
        Initialize the renderer.

        Args:
            surface: Pygame surface to render to.
            sprite_manager: Sprite manager for loading images.
        """
        self.surface = surface
        self.sprite_manager = sprite_manager

    def clear(self) -> None:
        """Clear the screen with background color."""
        self.surface.fill(Colors.WINDOW_BACKGROUND)

    def draw_board(self, board: ChessBoard) -> None:
        """Draw the chess board."""
        board.draw(self.surface, self.sprite_manager)

    def draw_sidebar(self, sidebar: Optional[FigureSelectionBar]) -> None:
        """Draw the figure selection sidebar if present."""
        if sidebar:
            sidebar.draw(self.surface, self.sprite_manager)

    def present(self) -> None:
        """Present the rendered frame to the screen."""
        pg.display.flip()
