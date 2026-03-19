"""Application constants."""

from typing import Final

Color = tuple[int, int, int]


class Colors:
    """Color definitions used throughout the application."""

    WHITE: Final[Color] = (255, 255, 255)
    BLACK: Final[Color] = (0, 0, 0)
    RED: Final[Color] = (255, 0, 0)
    BAR_BACKGROUND: Final[Color] = (125, 85, 165)
    WINDOW_BACKGROUND: Final[Color] = (140, 100, 180)


DEFAULT_CONFIG: Final[str] = """screen_width: 700
screen_height: 700
tiles_in_row: 8
tiles_in_column: 8
figure_mode: free
show_ban_fields: True"""

# Game settings
FPS: Final[int] = 60
BAR_SPACING: Final[int] = 10
