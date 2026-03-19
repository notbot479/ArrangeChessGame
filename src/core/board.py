"""Chess board state management."""

from typing import Optional, TYPE_CHECKING

import pygame as pg

from src.core.tile import Tile
from src.core.movement import MovementCalculator

if TYPE_CHECKING:
    from src.ui.sprite_manager import SpriteManager

Position = tuple[int, int]


class ChessBoard:
    """Manages the chess board state and figure placement."""

    def __init__(
        self,
        surface_size: tuple[int, int],
        board_dimensions: tuple[int, int],
        bar_offset: int = 0,
    ):
        """
        Initialize the chess board.

        Args:
            surface_size: Window size (width, height).
            board_dimensions: Board size (columns, rows).
            bar_offset: Horizontal offset for sidebar.
        """
        self.surface_size = surface_size
        self.board_dimensions = board_dimensions
        self.bar_offset = bar_offset

        self.tiles: list[Tile] = []
        self.placed_figures: dict[Position, str] = {}
        self.movement_calc = MovementCalculator(board_dimensions)

        self._create_tiles()

    @property
    def all_positions(self) -> set[Position]:
        """Get all valid board positions."""
        return {tile.tile_id for tile in self.tiles}

    @property
    def free_positions(self) -> set[Position]:
        """Calculate currently unattacked positions."""
        free = self.all_positions.copy()
        for position, figure in self.placed_figures.items():
            attacked = self.movement_calc.get_attacked_fields(figure, position)
            free -= attacked
        return free

    @property
    def figure_count(self) -> int:
        """Get number of placed figures."""
        return len(self.placed_figures)

    def _create_tiles(self) -> None:
        """Generate all board tiles."""
        columns, rows = self.board_dimensions
        tile_size = self._calculate_tile_size()
        offset_x, offset_y = self._calculate_board_offset(tile_size)

        for col in range(1, columns + 1):
            for row in range(1, rows + 1):
                x = offset_x + self.bar_offset + (row - 1) * tile_size
                y = offset_y + (col - 1) * tile_size

                tile = Tile(
                    x=x,
                    y=y,
                    width=tile_size,
                    height=tile_size,
                    tile_id=(col, row),
                    color=Tile.calculate_chess_color(col, row),
                )
                self.tiles.append(tile)

    def _calculate_tile_size(self) -> float:
        """Calculate optimal tile size to fit the board."""
        width, height = self.surface_size
        columns, rows = self.board_dimensions
        available_width = width - self.bar_offset
        return min(available_width / rows, height / columns)

    def _calculate_board_offset(self, tile_size: float) -> tuple[float, float]:
        """Calculate offset to center the board."""
        width, height = self.surface_size
        columns, rows = self.board_dimensions

        board_width = rows * tile_size
        board_height = columns * tile_size

        offset_x = (width - self.bar_offset - board_width) / 2
        offset_y = (height - board_height) / 2

        return max(0, offset_x), max(0, offset_y)

    def get_tile_at_position(self, x: float, y: float) -> Optional[Tile]:
        """Find tile at screen coordinates."""
        for tile in self.tiles:
            if tile.contains_point(x, y):
                return tile
        return None

    def get_tile_by_id(self, tile_id: Position) -> Optional[Tile]:
        """Find tile by board position."""
        for tile in self.tiles:
            if tile.tile_id == tile_id:
                return tile
        return None

    def can_place_figure(self, figure: str, position: Position) -> bool:
        """Check if figure can be legally placed at position."""
        if position not in self.free_positions:
            return False

        new_attacks = self.movement_calc.get_attacked_fields(figure, position)
        existing_positions = set(self.placed_figures.keys())
        return not bool(new_attacks & existing_positions)

    def place_figure(self, figure: str, position: Position) -> bool:
        """Attempt to place a figure at the given position."""
        tile = self.get_tile_by_id(position)
        if not tile:
            return False

        if tile.figure and tile.figure != "ban":
            return False

        if not self.can_place_figure(figure, position):
            return False

        tile.figure = figure
        self.placed_figures[position] = figure
        return True

    def remove_figure(self, position: Position) -> bool:
        """Remove a figure from the given position."""
        tile = self.get_tile_by_id(position)
        if not tile:
            return False

        if not tile.figure or tile.figure == "ban":
            return False

        del self.placed_figures[position]
        tile.figure = ""
        return True

    def update_attack_display(self, show_attacks: bool) -> None:
        """Update visual display of attacked squares."""
        free = self.free_positions

        for tile in self.tiles:
            if tile.tile_id in self.placed_figures:
                continue

            if show_attacks and tile.tile_id not in free:
                tile.figure = "ban"
            elif tile.figure == "ban":
                tile.figure = ""

            tile.reset_color()

    def draw(self, surface: pg.Surface, sprite_manager: "SpriteManager") -> None:
        """Draw all tiles to the surface."""
        for tile in self.tiles:
            tile.draw(surface, sprite_manager)
