"""Main application entry point."""

import sys
import logging
from pathlib import Path

from src.config import ConfigLoader, GameSettings
from src.game import ChessGame


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def main() -> None:
    """Main application entry point."""
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    project_root = get_project_root()
    config_path = project_root / "config.txt"
    assets_path = project_root / "assets"

    try:
        settings = ConfigLoader.load(config_path)
    except FileNotFoundError as e:
        logging.error("%s", e)
        logging.info("Please fill in the config file and restart.")
        sys.exit(1)
    except ValueError as e:
        logging.error("Configuration error: %s", e)
        sys.exit(1)

    game = ChessGame(settings, assets_path)
    game.run()


if __name__ == "__main__":
    main()
