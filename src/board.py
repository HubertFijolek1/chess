from chess_piece import King, Queen, Rook, Bishop, Knight, Pawn
from constants import WHITE, BLACK
from piece_factory import PieceFactory
from utils import parse_position, position_to_notation
import logging

logging.basicConfig(level=logging.INFO)

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  # Initialize an 8x8 grid with None
        self.current_turn = WHITE  # White starts first
        self.setup_board()  # Set up the board with initial positions
        self.game_over = False  # Flag to indicate if the game has ended

    def setup_board(self) -> None:
        """
        Sets up the board with initial positions for all pieces.
        """
        back_rank_symbols = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

        # Set up black pieces
        for col, symbol in enumerate(back_rank_symbols):
            self.grid[0][col] = PieceFactory.create_piece(symbol, BLACK)
            self.grid[1][col] = PieceFactory.create_piece('P', BLACK)

        # Set up white pieces
        for col, symbol in enumerate(back_rank_symbols):
            self.grid[7][col] = PieceFactory.create_piece(symbol, WHITE)
            self.grid[6][col] = PieceFactory.create_piece('P', WHITE)

    def display(self) -> None:
        """
        Displays the current state of the board with column letters and row numbers.
        """
        print("  a b c d e f g h")  # Print column headers
        for row in range(8):
            row_display = [str(piece) if piece else '.' for piece in self.grid[row]]  # Generate row display
            print(f"{8 - row} {' '.join(row_display)} {8 - row}")  # Print row with row numbers on both sides
        print("  a b c d e f g h")  # Print column headers

    def is_in_check(self, color: str) -> bool:
        """
        Determines if the king of the given color is in check.
        """
        king_position = None

        # Find the king's position
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_position = (row, col)
                    break
            if king_position:
                break

        if not king_position:
            logging.error(f"{color.capitalize()} king not found on the board!")
            return False  # King not found; should not happen

        # Check if any opposing piece can move to the king's position
        opponent_color = BLACK if color == WHITE else WHITE
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece is not None and piece.color == opponent_color:
                    if piece.is_valid_move((row, col), king_position, self, ignore_checks=True):
                        return True  # King is in check
        return False  # King is not in check

    def move_piece(self, start: tuple, end: tuple) -> bool:
        """
        Moves a piece from the start position to the end position if the move is valid and doesn't put own king in check.
        """
        start_row, start_col = start
        end_row, end_col = end
        piece = self.grid[start_row][start_col]

        if piece is None:
            start_notation = position_to_notation(start)
            print(f"No piece at starting position {start_notation}")
            return False

        if piece.color != self.current_turn:
            start_notation = position_to_notation(start)
            print(f"It's {self.current_turn}'s turn, but the piece at {start_notation} is {piece.color}")
            return False  # It's not the player's turn

        if not piece.is_valid_move(start, end, self):
            start_notation = position_to_notation(start)
            end_notation = position_to_notation(end)
            print(f"Invalid move for {piece} from {start_notation} to {end_notation}")
            return False  # The move is not valid for this piece

        # Simulate the move
        captured_piece = self.grid[end_row][end_col]
        self.grid[end_row][end_col] = piece
        self.grid[start_row][start_col] = None

        # Check if the move puts own king in check
        if self.is_in_check(piece.color):
            # Undo the move
            self.grid[start_row][start_col] = piece
            self.grid[end_row][end_col] = captured_piece
            print("Cannot move into check.")
            return False

        # Move is valid; log the capture if any
        if captured_piece is not None:
            logging.info(f"{piece} captures {captured_piece} at {position_to_notation(end)}")

        # Update the board state
        self.current_turn = BLACK if self.current_turn == WHITE else WHITE  # Switch turns
        return True  # Move was successful
