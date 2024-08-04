from chess_piece import King, Queen, Bishop, Knight, Rook, Pawn

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]  # Initialize an 8x8 board with None
        self.current_turn = 'white'  # White starts first
        self.setup_board()  # Set up the board with initial positions

    def setup_board(self):
        """
        Sets up the board with initial positions for all pieces.
        """
        for col in range(8):
            self.board[1][col] = Pawn('black')
            self.board[6][col] = Pawn('white')
        self.board[0][0] = self.board[0][7] = Rook('black')
        self.board[0][1] = self.board[0][6] = Knight('black')
        self.board[0][2] = self.board[0][5] = Bishop('black')
        self.board[0][3] = Queen('black')
        self.board[0][4] = King('black')
        self.board[7][0] = self.board[7][7] = Rook('white')
        self.board[7][1] = self.board[7][6] = Knight('white')
        self.board[7][2] = self.board[7][5] = Bishop('white')
        self.board[7][3] = Queen('white')
        self.board[7][4] = King('white')

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