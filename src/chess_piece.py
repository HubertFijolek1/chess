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
        self.has_moved = False  # Track if the piece has moved (important for castling and pawn's first move)

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def symbol(self) -> str:
        """
        Returns the symbol representing the piece.

        Returns:
            str: The symbol of the piece.
        """
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

    def move(self):
        """
        Marks the piece as having moved. Should be called after a successful move.
        """
        self.has_moved = True


class King(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, KingMovementStrategy())

    def __str__(self) -> str:
        return 'K' if self.color == WHITE else 'k'

    def symbol(self) -> str:
        return 'K'


class Queen(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, QueenMovementStrategy())

    def __str__(self) -> str:
        return 'Q' if self.color == WHITE else 'q'

    def symbol(self) -> str:
        return 'Q'


class Rook(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, RookMovementStrategy())

    def __str__(self) -> str:
        return 'R' if self.color == WHITE else 'r'

    def symbol(self) -> str:
        return 'R'


class Bishop(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, BishopMovementStrategy())

    def __str__(self) -> str:
        return 'B' if self.color == WHITE else 'b'

    def symbol(self) -> str:
        return 'B'


class Knight(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, KnightMovementStrategy())

    def __str__(self) -> str:
        return 'N' if self.color == WHITE else 'n'

    def symbol(self) -> str:
        return 'N'


class Pawn(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color, PawnMovementStrategy())

    def __str__(self) -> str:
        return 'P' if self.color == WHITE else 'p'

    def symbol(self) -> str:
        return 'P'