from abc import ABC, abstractmethod
from constants import WHITE, BLACK
from movement_strategies import (
    KingMovementStrategy,
    QueenMovementStrategy,
    RookMovementStrategy,
    BishopMovementStrategy,
    KnightMovementStrategy,
    PawnMovementStrategy
)


class ChessPiece(ABC):
    def __init__(self, color: str, movement_strategy):
        self.color = color  # Color of the piece (WHITE or BLACK)
        self.movement_strategy = movement_strategy

    @abstractmethod
    def __str__(self) -> str:
        pass

    def is_valid_move(self, start: tuple, end: tuple, board, ignore_checks=False) -> bool:
        """
        Determines if the move from start to end is valid based on the movement strategy.

        Parameters:
            start (tuple): Starting position (row, col).
            end (tuple): Ending position (row, col).
            board (Board): The current game board.
            ignore_checks (bool): If True, ignores checks when validating the move.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return self.movement_strategy.is_valid_move(start, end, board, self, ignore_checks)

    def can_capture_or_move_to(self, end: tuple, board) -> bool:
        """
        Determines if the piece can move to the specified end position, either by moving to an empty square
        or capturing an opponent's piece.

        Parameters:
            end (tuple): The target position (row, col).
            board (Board): The current game board.

        Returns:
            bool: True if the piece can move or capture, False otherwise.
        """
        end_row, end_col = end
        target_piece = board.grid[end_row][end_col]
        if target_piece is None:
            return True  # The end position is empty
        if target_piece.color != self.color:
            return True  # Can capture opponent's piece
        return False  # Cannot capture own piece


class King(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, KingMovementStrategy())

    def __str__(self) -> str:
        return 'K' if self.color == WHITE else 'k'


class Queen(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, QueenMovementStrategy())

    def __str__(self) -> str:
        return 'Q' if self.color == WHITE else 'q'


class Rook(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, RookMovementStrategy())

    def __str__(self) -> str:
        return 'R' if self.color == WHITE else 'r'


class Bishop(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, BishopMovementStrategy())

    def __str__(self) -> str:
        return 'B' if self.color == WHITE else 'b'


class Knight(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, KnightMovementStrategy())

    def __str__(self) -> str:
        return 'N' if self.color == WHITE else 'n'


class Pawn(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, PawnMovementStrategy())

    def __str__(self) -> str:
        return 'P' if self.color == WHITE else 'p'
