"""Figure selection sidebar component."""

from typing import Optional

import pygame as pg

from src.config.constants import Colors, BAR_SPACING
from src.core.tile import Tile
from src.ui.sprite_manager import SpriteManager


class FigureSelectionBar:
    """Sidebar UI for selecting chess figures."""

    BORDER_WIDTH = 2
    BORDER_COLOR = Colors.RED

    def __init__(
        self,
        figures: list[str],
        position: tuple[int, int],
        size: tuple[int, int],
    ):
        """
        Initialize the figure selection bar.

        Args:
            figures: List of figure type identifiers.
            position: Top-left position (x, y).
            size: Bar size (width, height).
        """
        self.figures = figures
        self.position = position
        self.size = size
        self.spacing = BAR_SPACING

        self.background = self._create_background()
        self.buttons: list[Tile] = []
        self._create_buttons()
        self.selected = None

    def _create_background(self) -> Tile:
        """Create the bar background tile."""
        x, y = self.position
        width, height = self.size

        return Tile(
            x=x + self.spacing,
            y=y + self.spacing,
            width=width - 2 * self.spacing,
            height=height - 2 * self.spacing,
            color=Colors.BAR_BACKGROUND,
        )

    def _create_buttons(self) -> None:
        """Create figure selection buttons."""
        bar_width = self.size[0] - 2 * self.spacing
        bar_height = self.size[1] - 2 * self.spacing

        button_count = len(self.figures)
        vertical_space = bar_height // (button_count * 2 + 1)
        max_button_size = bar_width // 3 + self.spacing

        button_size = min(max_button_size, vertical_space)
        button_x = self.spacing + (bar_width - button_size) // 2

        for index, figure in enumerate(self.figures):
            button_y = self.spacing + vertical_space * (2 * index + 1)

            button = Tile(
                x=button_x,
                y=button_y,
                width=button_size,
                height=button_size,
                color=Colors.WHITE,
                figure=figure,
            )
            self.buttons.append(button)

    def get_clicked_figure(self, x: float, y: float) -> Optional[str]:
        """Get the figure type if a button was clicked."""
        for button in self.buttons:
            if button.contains_point(x, y):
                return button.figure
        return None

    def set_selected(self, figure: Optional[str]) -> None:
        """Mark a figure as selected in the sidebar.

        Args:
            figure: Figure identifier or None to clear selection.
        """
        self.selected = figure

    def draw(self, surface: pg.Surface, sprite_manager: SpriteManager) -> None:
        """Draw the sidebar and all buttons."""
        self.background.draw(surface, sprite_manager)
        for button in self.buttons:
            button.draw(surface, sprite_manager)

            # Draw a visible border for the selected button
            if self.selected and button.figure == self.selected:
                border_rect = button.rect.inflate(self.BORDER_WIDTH, self.BORDER_WIDTH)
                pg.draw.rect(
                    surface, self.BORDER_COLOR, border_rect, width=self.BORDER_WIDTH
                )
