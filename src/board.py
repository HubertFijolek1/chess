from chess_piece import King, Queen, Bishop, Knight, Rook, Pawn
from constants import WHITE, BLACK

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  # Initialize an 8x8 grid with None
        self.current_turn = WHITE  # White starts first
        self.setup_board()  # Set up the board with initial positions

    def setup_board(self):
        """
        Sets up the board with initial positions for all pieces.
        """
        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        # Set up black pieces
        for col, piece_class in enumerate(back_rank):
            self.grid[0][col] = piece_class(BLACK)
            self.grid[1][col] = Pawn(BLACK)

        # Set up white pieces
        for col, piece_class in enumerate(back_rank):
            self.grid[7][col] = piece_class(WHITE)
            self.grid[6][col] = Pawn(WHITE)

    def display(self):
        """
        Displays the current state of the board with column letters and row numbers.
        """
        print("  a b c d e f g h")  # Print column headers
        for row in range(8):
            row_display = [str(piece) if piece else '.' for piece in self.board[row]]  # Generate row display
            print(f"{8 - row} {' '.join(row_display)} {8 - row}")  # Print row with row numbers on both sides
        print("  a b c d e f g h")  # Print column headers

    def move_piece(self, start, end):
        """
        Moves a piece from the start position to the end position if the move is valid.
        
        Parameters:
        start (tuple): Start position (row, col)
        end (tuple): End position (row, col)
        
        Returns:
        bool: True if the move is successful, False otherwise
        """
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]

        if piece is None:
            print(f"No piece at starting position {start}")
            return False

        if piece.color != self.current_turn:
            print(f"It's {self.current_turn}'s turn, but the piece at {start} is {piece.color}")
            return False  # Move is invalid if it's not the piece's turn

        if not piece.is_valid_move(start, end, self.board):
            print(f"Invalid move for {piece} from {start} to {end}")
            return False  # Move is invalid if the piece cannot legally move to the end position

        self.board[end_row][end_col] = piece  # Move the piece to the new position
        self.board[start_row][start_col] = None  # Remove the piece from the start position
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'  # Switch turns
        return True  # Move was successful