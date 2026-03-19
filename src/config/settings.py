"""Game settings data structure."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GameSettings:
    """Immutable game settings loaded from configuration."""

    screen_width: int
    screen_height: int
    tiles_in_row: int
    tiles_in_column: int
    figure_mode: str
    show_ban_fields: bool

    @property
    def window_size(self) -> tuple[int, int]:
        """Get window dimensions as tuple."""
        return self.screen_width, self.screen_height

    @property
    def board_dimensions(self) -> tuple[int, int]:
        """Get board dimensions (columns, rows)."""
        return self.tiles_in_column, self.tiles_in_row

    @property
    def is_free_mode(self) -> bool:
        """Check if game is in free figure selection mode."""
        return self.figure_mode.lower() == "free"

    def get_bar_size(self) -> int:
        """Calculate sidebar size based on mode."""
        if self.is_free_mode:
            return max(self.window_size) // 4
        return 0
