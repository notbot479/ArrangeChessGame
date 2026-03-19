"""Chess figure definitions."""

from enum import Enum


class FigureType(Enum):
    """Chess piece types with their string identifiers."""

    QUEEN = "Q"
    BISHOP = "B"
    KNIGHT = "N"
    ROOK = "R"
    KING = "K"
    PAWN = "P"
    AMAZON = "M"  # Queen + Knight combination

    @classmethod
    def values(cls) -> list[str]:
        """Get list of all figure type values."""
        return [figure.value for figure in cls]

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if a string is a valid figure type."""
        return value.upper() in cls.values()

    @classmethod
    def get_default(cls) -> str:
        """Get the default figure type."""
        return cls.QUEEN.value
