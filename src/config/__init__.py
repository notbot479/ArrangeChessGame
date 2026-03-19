"""Configuration module."""

from src.config.constants import Colors, DEFAULT_CONFIG, FPS, BAR_SPACING
from src.config.settings import GameSettings
from src.config.loader import ConfigLoader

__all__ = [
    "Colors",
    "DEFAULT_CONFIG",
    "FPS",
    "BAR_SPACING",
    "GameSettings",
    "ConfigLoader",
]
