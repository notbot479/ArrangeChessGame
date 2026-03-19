"""Main game class."""

from pathlib import Path
from time import sleep
from typing import Optional
import logging

import pygame as pg

from src.config.constants import FPS
from src.config.settings import GameSettings
from src.core.figures import FigureType
from src.core.board import ChessBoard
from src.ui.sprite_manager import SpriteManager
from src.ui.sidebar import FigureSelectionBar
from src.ui.renderer import GameRenderer
from src.game.events import EventHandler, EventType

logger = logging.getLogger(__name__)


class ChessGame:
    """Main game controller."""

    def __init__(self, settings: GameSettings, assets_path: Path):
        """
        Initialize the game.

        Args:
            settings: Game configuration settings.
            assets_path: Path to the assets directory.
        """
        self.settings = settings
        self.assets_path = assets_path
        self.running = False

        self.current_figure = self._get_initial_figure()
        self.max_figures = self._get_max_figures()

        self._init_pygame()
        self._init_components()

    def _get_initial_figure(self) -> str:
        """Determine the initial figure based on settings."""
        if self.settings.is_free_mode:
            return FigureType.get_default()

        mode = self.settings.figure_mode.upper()
        if FigureType.is_valid(mode):
            return mode

        return FigureType.get_default()

    def _get_max_figures(self) -> float:
        """Get the maximum number of figures that can be placed."""
        if self.settings.is_free_mode:
            return float("inf")

        try:
            count = int(input("Number of figures to place: "))
            return max(1, count)
        except ValueError:
            return 8

    def _init_pygame(self) -> None:
        """Initialize pygame and create the window."""
        pg.init()

        bar_size = self.settings.get_bar_size()
        self.window_size = (
            self.settings.screen_width + bar_size,
            self.settings.screen_height,
        )

        self.surface = pg.display.set_mode(self.window_size)
        pg.display.set_caption("Chess Board Visualization")
        self.clock = pg.time.Clock()

    def _init_components(self) -> None:
        """Initialize game components."""
        sprites_path = self.assets_path / "sprites"
        self.sprite_manager = SpriteManager(sprites_path)
        self.sprite_manager.load_all(FigureType.values() + ["empty", "ban"])

        bar_size = self.settings.get_bar_size()
        self.board = ChessBoard(
            surface_size=self.window_size,
            board_dimensions=self.settings.board_dimensions,
            bar_offset=bar_size,
        )

        self.sidebar: Optional[FigureSelectionBar] = None
        if self.settings.is_free_mode:
            self.sidebar = FigureSelectionBar(
                figures=FigureType.values(),
                position=(0, 0),
                size=(bar_size, self.window_size[1]),
            )
            # initialize sidebar selection to current figure
            self.sidebar.set_selected(self.current_figure)

        self.renderer = GameRenderer(self.surface, self.sprite_manager)

    def run(self) -> None:
        """Run the main game loop."""
        self.running = True

        while self.running:
            self._process_events()
            self._update()
            self._render()
            self.clock.tick(FPS)

        pg.quit()

    def _process_events(self) -> None:
        """Process all game events."""
        for event in EventHandler.process_events():
            if event.type == EventType.QUIT:
                self.running = False
            elif event.type == EventType.CLICK and event.position:
                self._handle_click(event.position)

    def _handle_click(self, position: tuple[int, int]) -> None:
        """Handle a mouse click event."""
        x, y = position

        if self.sidebar:
            clicked_figure = self.sidebar.get_clicked_figure(x, y)
            if clicked_figure:
                self.current_figure = clicked_figure
                # inform sidebar of the new selection so it can render a border
                self.sidebar.set_selected(clicked_figure)
                logger.info("Selected: %s", clicked_figure)
                return

        self._handle_board_click(x, y)

    def _handle_board_click(self, x: float, y: float) -> None:
        """Handle a click on the board."""
        tile = self.board.get_tile_at_position(x, y)
        if not tile:
            return

        if tile.figure and tile.figure != "ban":
            if self.board.remove_figure(tile.tile_id):
                logger.info("Removed figure from %s", tile.tile_id)
        else:
            if self.board.place_figure(self.current_figure, tile.tile_id):
                logger.info("Placed %s at %s", self.current_figure, tile.tile_id)
            else:
                logger.warning("Cannot place figure at %s", tile.tile_id)

        self.board.update_attack_display(self.settings.show_ban_fields)

    def _update(self) -> None:
        """Update game state."""
        if self.board.figure_count >= self.max_figures:
            logger.info("\n" + "=" * 40)
            logger.info("SUCCESS! All figures placed!")
            logger.info("=" * 40)
            sleep(3)
            self.running = False

    def _render(self) -> None:
        """Render the current frame."""
        self.renderer.clear()
        self.renderer.draw_board(self.board)
        self.renderer.draw_sidebar(self.sidebar)
        self.renderer.present()
