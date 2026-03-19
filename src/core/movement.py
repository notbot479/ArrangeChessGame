"""Movement and attack pattern calculation for chess pieces."""

from src.core.figures import FigureType

Position = tuple[int, int]
PositionSet = set[Position]


class MovementCalculator:
    """Calculates attack patterns for different chess pieces."""

    def __init__(self, board_size: tuple[int, int]):
        """
        Initialize calculator with board dimensions.

        Args:
            board_size: Tuple of (columns, rows).
        """
        self.columns, self.rows = board_size
        self.max_distance = max(board_size) + 1

    def get_attacked_fields(self, figure: str, position: Position) -> PositionSet:
        """
        Calculate all fields attacked by a figure from a given position.

        Args:
            figure: Figure type identifier (e.g., 'Q', 'N').
            position: Current position as (column, row).

        Returns:
            Set of positions that the figure attacks.
        """
        calculators = {
            FigureType.QUEEN.value: self._queen_attacks,
            FigureType.BISHOP.value: self._bishop_attacks,
            FigureType.KNIGHT.value: self._knight_attacks,
            FigureType.ROOK.value: self._rook_attacks,
            FigureType.KING.value: self._king_attacks,
            FigureType.PAWN.value: self._pawn_attacks,
            FigureType.AMAZON.value: self._amazon_attacks,
        }

        calculator = calculators.get(figure)
        if calculator:
            attacks = calculator(position)
            attacks.add(position)
            return attacks

        return {position}

    def _straight_lines(self, col: int, row: int) -> PositionSet:
        """Generate horizontal and vertical line attacks."""
        attacks: PositionSet = set()
        attacks.update((col, r) for r in range(1, self.rows + 1))
        attacks.update((c, row) for c in range(1, self.columns + 1))
        return attacks

    def _diagonal_lines(self, col: int, row: int) -> PositionSet:
        """Generate diagonal line attacks."""
        attacks: PositionSet = set()
        for i in range(self.max_distance):
            attacks.update(
                [
                    (col + i, row + i),
                    (col - i, row - i),
                    (col + i, row - i),
                    (col - i, row + i),
                ]
            )
        return attacks

    def _queen_attacks(self, position: Position) -> PositionSet:
        """Queen attacks: straight lines + diagonals."""
        col, row = position
        return self._straight_lines(col, row) | self._diagonal_lines(col, row)

    def _rook_attacks(self, position: Position) -> PositionSet:
        """Rook attacks: diagonals only (matches original code behavior)."""
        col, row = position
        return self._diagonal_lines(col, row)

    def _bishop_attacks(self, position: Position) -> PositionSet:
        """Bishop attacks: straight lines only (matches original code behavior)."""
        col, row = position
        return self._straight_lines(col, row)

    def _knight_attacks(self, position: Position) -> PositionSet:
        """Knight attacks: L-shaped moves."""
        col, row = position
        offsets = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        return {(col + dc, row + dr) for dc, dr in offsets}

    def _king_attacks(self, position: Position) -> PositionSet:
        """King attacks: all adjacent squares."""
        col, row = position
        offsets = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        return {(col + dc, row + dr) for dc, dr in offsets}

    def _pawn_attacks(self, position: Position) -> PositionSet:
        """Pawn attacks: diagonal captures in both directions."""
        col, row = position
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return {(col + dc, row + dr) for dc, dr in offsets}

    def _amazon_attacks(self, position: Position) -> PositionSet:
        """Amazon attacks: queen + knight combined."""
        return self._queen_attacks(position) | self._knight_attacks(position)
