from abc import ABC, abstractmethod
from constants import WHITE, BLACK

class MovementStrategy(ABC):
    @abstractmethod
    def is_valid_move(self, start: tuple, end: tuple, board, piece) -> bool:
        pass

class KingMovementStrategy(MovementStrategy):
    def is_valid_move(self, start: tuple, end: tuple, board, piece) -> bool:
        start_row, start_col = start
        end_row, end_col = end
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        return max(row_diff, col_diff) == 1 and piece.can_capture_or_move_to(end, board)

class QueenMovementStrategy(MovementStrategy):
    def is_valid_move(self, start: tuple, end: tuple, board, piece) -> bool:
        start_row, start_col = start
        end_row, end_col = end
        row_diff = end_row - start_row
        col_diff = end_col - start_col
        if abs(row_diff) == abs(col_diff) or start_row == end_row or start_col == end_col:
            if board.is_path_clear(start, end) and piece.can_capture_or_move_to(end, board):
                return True
        return False

class RookMovementStrategy(MovementStrategy):
    def is_valid_move(self, start: tuple, end: tuple, board, piece) -> bool:
        start_row, start_col = start
        end_row, end_col = end
        if start_row == end_row or start_col == end_col:
            if board.is_path_clear(start, end) and piece.can_capture_or_move_to(end, board):
                return True
        return False

class BishopMovementStrategy(MovementStrategy):
    def is_valid_move(self, start: tuple, end: tuple, board, piece) -> bool:
        if abs(start[0] - end[0]) == abs(start[1] - end[1]):
            if board.is_path_clear(start, end) and piece.can_capture_or_move_to(end, board):
                return True
        return False

class KnightMovementStrategy(MovementStrategy):
    def is_valid_move(self, start: tuple, end: tuple, board, piece) -> bool:
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])
        if row_diff * col_diff == 2 and piece.can_capture_or_move_to(end, board):
            return True
        return False

class PawnMovementStrategy(MovementStrategy):
    def is_valid_move(self, start: tuple, end: tuple, board, piece) -> bool:
        start_row, start_col = start
        end_row, end_col = end

        # Determine direction and starting row based on color
        direction = -1 if piece.color == WHITE else 1
        start_row_standard = 6 if piece.color == WHITE else 1

        # Move forward
        if start_col == end_col:
            if end_row == start_row + direction and board.grid[end_row][end_col] is None:
                return True  # Move one square forward
            if start_row == start_row_standard and end_row == start_row + 2 * direction:
                if board.grid[start_row + direction][start_col] is None and board.grid[end_row][end_col] is None:
                    return True  # Move two squares forward from starting position

        # Capture diagonally
        if abs(end_col - start_col) == 1 and end_row == start_row + direction:
            target_piece = board.grid[end_row][end_col]
            if target_piece is not None and target_piece.color != piece.color:
                return True  # Capture opponent's piece

        return False  # Invalid move
