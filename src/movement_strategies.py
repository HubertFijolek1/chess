from abc import ABC, abstractmethod
from constants import WHITE, BLACK
from chess_piece import Rook  # Import Rook for type checking


class MovementStrategy(ABC):
    @abstractmethod
    def is_valid_move(self, start: tuple, end: tuple, board, piece, ignore_checks=False) -> bool:
        pass


class KingMovementStrategy(MovementStrategy):
    def is_valid_move(self, start, end, board, piece, ignore_checks=False):
        start_row, start_col = start
        end_row, end_col = end
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        # Standard one-square move
        if max(row_diff, col_diff) == 1 and piece.can_capture_or_move_to(end, board):
            return True

        # Castling
        if not piece.has_moved and row_diff == 0 and col_diff == 2:
            # Determine castling direction
            if end_col == start_col + 2:
                # Kingside castling
                rook_start = (start_row, 7)
                rook_end = (start_row, 5)
            elif end_col == start_col - 2:
                # Queenside castling
                rook_start = (start_row, 0)
                rook_end = (start_row, 3)
            else:
                return False  # Invalid castling move

            rook = board.grid[rook_start[0]][rook_start[1]]
            if not isinstance(rook, Rook) or rook.has_moved:
                return False  # Rook has moved or is not present

            # Check if squares between king and rook are empty
            step = 1 if rook_end[1] > start_col else -1
            for col in range(start_col + step, rook_end[1], step):
                if board.grid[start_row][col] is not None:
                    return False  # Path is not clear

            # Check if squares king passes through are not under attack
            for col in range(start_col, end_col + step, step):
                if board.is_square_under_attack((start_row, col), BLACK if piece.color == WHITE else WHITE):
                    return False  # Square is under attack

            return True  # Castling is valid

        return False  # Invalid move


class QueenMovementStrategy(MovementStrategy):
    def is_valid_move(self, start, end, board, piece, ignore_checks=False):
        start_row, start_col = start
        end_row, end_col = end
        row_diff = end_row - start_row
        col_diff = end_col - start_col
        if abs(row_diff) == abs(col_diff) or start_row == end_row or start_col == end_col:
            if board.is_path_clear(start, end) and piece.can_capture_or_move_to(end, board):
                return True
        return False


class RookMovementStrategy(MovementStrategy):
    def is_valid_move(self, start, end, board, piece, ignore_checks=False):
        start_row, start_col = start
        end_row, end_col = end
        if start_row == end_row or start_col == end_col:
            if board.is_path_clear(start, end) and piece.can_capture_or_move_to(end, board):
                return True
        return False


class BishopMovementStrategy(MovementStrategy):
    def is_valid_move(self, start, end, board, piece, ignore_checks=False):
        if abs(start[0] - end[0]) == abs(start[1] - end[1]):
            if board.is_path_clear(start, end) and piece.can_capture_or_move_to(end, board):
                return True
        return False


class KnightMovementStrategy(MovementStrategy):
    def is_valid_move(self, start, end, board, piece, ignore_checks=False):
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])
        if row_diff * col_diff == 2 and piece.can_capture_or_move_to(end, board):
            return True
        return False


class PawnMovementStrategy(MovementStrategy):
    def is_valid_move(self, start: tuple, end: tuple, board, piece, ignore_checks=False) -> bool:
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
                intermediate_row = start_row + direction
                if board.grid[intermediate_row][start_col] is None and board.grid[end_row][end_col] is None:
                    return True  # Move two squares forward from starting position

        # Capture diagonally
        if abs(end_col - start_col) == 1 and end_row == start_row + direction:
            target_piece = board.grid[end_row][end_col]
            if target_piece is not None and target_piece.color != piece.color:
                return True  # Capture opponent's piece

            # En Passant Capture
            if target_piece is None:
                # Check if en passant is possible
                last_move = board.last_move
                if last_move:
                    last_start, last_end = last_move
                    last_piece = board.grid[last_end[0]][last_end[1]]
                    if isinstance(last_piece, Pawn) and last_piece.color != piece.color:
                        # Check if the pawn moved two squares forward in the last move
                        if abs(last_end[0] - last_start[0]) == 2:
                            # Check if the pawn is adjacent to this pawn
                            if last_end[0] == start_row and last_end[1] == end_col:
                                return True  # En Passant is valid

        return False  # Invalid move