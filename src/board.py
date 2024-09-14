from chess_piece import ChessPiece
from constants import WHITE, BLACK
from piece_factory import PieceFactory

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  # Initialize an 8x8 grid with None
        self.current_turn = WHITE  # White starts first
        self.setup_board()  # Set up the board with initial positions

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


    def is_path_clear(self, start: tuple, end: tuple) -> bool:
        """
        Checks if the path between start and end positions is clear (no pieces in between).
        """
        start_row, start_col = start
        end_row, end_col = end
        delta_row = end_row - start_row
        delta_col = end_col - start_col

        step_row = (delta_row // abs(delta_row)) if delta_row != 0 else 0
        step_col = (delta_col // abs(delta_col)) if delta_col != 0 else 0

        current_row = start_row + step_row
        current_col = start_col + step_col

        while (current_row, current_col) != (end_row, end_col):
            if self.grid[current_row][current_col] is not None:
                return False  # Path is blocked
            current_row += step_row
            current_col += step_col

        return True  # Path is clear

    def move_piece(self, start: tuple, end: tuple) -> bool:
        """
        Moves a piece from the start position to the end position if the move is valid.
        """
        start_row, start_col = start
        end_row, end_col = end
        piece = self.grid[start_row][start_col]

        if piece is None:
            print(f"No piece at starting position {start}")
            return False

        if piece.color != self.current_turn:
            print(f"It's {self.current_turn}'s turn, but the piece at {start} is {piece.color}")
            return False  # It's not the player's turn

        if not piece.is_valid_move(start, end, self):
            print(f"Invalid move for {piece} from {start} to {end}")
            return False  # The move is not valid for this piece

        self.grid[end_row][end_col] = piece  # Move the piece to the new position
        self.grid[start_row][start_col] = None  # Remove the piece from the start position
        self.current_turn = BLACK if self.current_turn == WHITE else WHITE  # Switch turns
        return True  # Move was successful