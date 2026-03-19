"""Configuration file loader."""

from pathlib import Path

from src.config.constants import DEFAULT_CONFIG
from src.config.settings import GameSettings


class ConfigLoader:
    """Handles loading and parsing of configuration files."""

    @classmethod
    def load(cls, filepath: Path) -> GameSettings:
        """
        Load configuration from file.

        Args:
            filepath: Path to the configuration file.

        Returns:
            GameSettings instance with loaded values.

        Raises:
            FileNotFoundError: If config doesn't exist (creates default).
            ValueError: If config values are invalid.
        """
        if not filepath.exists():
            cls._create_default(filepath)
            raise FileNotFoundError(f"Config file created at: {filepath}")

        config_dict = cls._parse_file(filepath)
        return cls._create_settings(config_dict)

    @staticmethod
    def _create_default(filepath: Path) -> None:
        """Create default configuration file."""
        filepath.write_text(DEFAULT_CONFIG)

    @staticmethod
    def _parse_file(filepath: Path) -> dict[str, str]:
        """Parse configuration file into dictionary."""
        config_dict = {}
        content = filepath.read_text()

        for line in content.strip().split("\n"):
            line = line.strip()
            if not line or ":" not in line:
                continue

            key, *value_parts = line.split(":")
            value = ":".join(value_parts).strip()
            config_dict[key.strip()] = value

        return config_dict

    @staticmethod
    def _create_settings(config: dict[str, str]) -> GameSettings:
        """Create GameSettings from parsed configuration."""
        try:
            return GameSettings(
                screen_width=int(config.get("screen_width", 700)),
                screen_height=int(config.get("screen_height", 700)),
                tiles_in_row=int(config.get("tiles_in_row", 8)),
                tiles_in_column=int(config.get("tiles_in_column", 8)),
                figure_mode=config.get("figure_mode", "free"),
                show_ban_fields=config.get("show_ban_fields", "True").lower() == "true",
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid configuration value: {e}") from e
