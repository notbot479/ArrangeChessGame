"""Sprite loading and management."""

from pathlib import Path
from typing import Optional

import pygame as pg


class SpriteManager:
    """Handles loading, caching, and scaling of sprites."""

    def __init__(self, sprites_directory: Path):
        """
        Initialize sprite manager.

        Args:
            sprites_directory: Path to directory containing sprite images.
        """
        self.sprites_dir = sprites_directory
        self._cache: dict[str, pg.Surface] = {}
        self._scaled_cache: dict[tuple[str, int, int], pg.Surface] = {}
        self._fallback: Optional[pg.Surface] = None

    def load_all(self, sprite_names: list[str]) -> None:
        """Pre-load all required sprites."""
        self._load_fallback()
        for name in sprite_names:
            self._load_sprite(name)

    def _load_fallback(self) -> None:
        """Load the fallback sprite for missing images."""
        fallback_path = self.sprites_dir / "ban.png"
        if fallback_path.exists():
            self._fallback = pg.image.load(str(fallback_path)).convert_alpha()

    def _load_sprite(self, name: str) -> pg.Surface:
        """Load a single sprite by name."""
        if name in self._cache:
            return self._cache[name]

        sprite_path = self.sprites_dir / f"{name}.png"

        try:
            sprite = pg.image.load(str(sprite_path)).convert_alpha()
        except pg.error:
            if self._fallback:
                sprite = self._fallback
            else:
                raise FileNotFoundError(
                    f"Sprite not found: {sprite_path} (and no fallback available)"
                )

        self._cache[name] = sprite
        return sprite

    def get(self, name: str) -> pg.Surface:
        """Get a sprite by name."""
        if name in self._cache:
            return self._cache[name]
        return self._load_sprite(name)

    def get_scaled(self, name: str, size: tuple[int, int]) -> pg.Surface:
        """Get a sprite scaled to the specified size."""
        cache_key = (name, size[0], size[1])

        if cache_key in self._scaled_cache:
            return self._scaled_cache[cache_key]

        original = self.get(name)
        scaled = pg.transform.scale(original, size)
        self._scaled_cache[cache_key] = scaled

        return scaled

    def clear_scaled_cache(self) -> None:
        """Clear the scaled sprite cache."""
        self._scaled_cache.clear()
