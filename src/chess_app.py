class ChessPiece:
    def __init__(self, color):
        self.color = color  # Color of the piece ('white' or 'black')

    def __str__(self):
        return 'Piece'  # Default string representation of a piece

    def can_move_to(self, end, board):
        """
        Checks if the piece can move to the given end position.
        
        Parameters:
        end (tuple): End position (row, col)
        board (list): Current state of the board
        
        Returns:
        bool: True if the move is valid, False otherwise
        """
        end_row, end_col = end
        if board[end_row][end_col] is None:
            return True  # Move is valid if the end position is empty
        if board[end_row][end_col].color != self.color:
            return True  # Move is valid if capturing an opponent's piece
        return False  # Move is invalid if the end position has a piece of the same color

class King(ChessPiece):
    def __str__(self):
        return 'K' if self.color == 'white' else 'k'  # String representation for King

    def is_valid_move(self, start, end, board):
        """
        Checks if the King can move from start to end position.
        
        Parameters:
        start (tuple): Start position (row, col)
        end (tuple): End position (row, col)
        board (list): Current state of the board
        
        Returns:
        bool: True if the move is valid, False otherwise
        """
        start_row, start_col = start
        end_row, end_col = end
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        return max(row_diff, col_diff) == 1 and self.can_move_to(end, board)  # King moves one square in any direction

class Queen(ChessPiece):
    def __str__(self):
        return 'Q' if self.color == 'white' else 'q'  # String representation for Queen

    def is_valid_move(self, start, end, board):
        """
        Checks if the Queen can move from start to end position.
        
        Parameters:
        start (tuple): Start position (row, col)
        end (tuple): End position (row, col)
        board (list): Current state of the board
        
        Returns:
        bool: True if the move is valid, False otherwise
        """
        start_row, start_col = start
        end_row, end_col = end
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        if row_diff == col_diff or start_row == end_row or start_col == end_col:
            return self.can_move_to(end, board)  # Queen moves any number of squares along a row, column, or diagonal
        return False

class Bishop(ChessPiece):
    def __str__(self):
        return 'B' if self.color == 'white' else 'b'  # String representation for Bishop

    def is_valid_move(self, start, end, board):
        """
        Checks if the Bishop can move from start to end position.
        
        Parameters:
        start (tuple): Start position (row, col)
        end (tuple): End position (row, col)
        board (list): Current state of the board
        
        Returns:
        bool: True if the move is valid, False otherwise
        """
        start_row, start_col = start
        end_row, end_col = end
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        return row_diff == col_diff and self.can_move_to(end, board)  # Bishop moves any number of squares diagonally

class Knight(ChessPiece):
    def __str__(self):
        return 'N' if self.color == 'white' else 'n'  # String representation for Knight

    def is_valid_move(self, start, end, board):
        """
        Checks if the Knight can move from start to end position.
        
        Parameters:
        start (tuple): Start position (row, col)
        end (tuple): End position (row, col)
        board (list): Current state of the board
        
        Returns:
        bool: True if the move is valid, False otherwise
        """
        start_row, start_col = start
        end_row, end_col = end
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        return row_diff * col_diff == 2 and self.can_move_to(end, board)  # Knight moves in an L-shape (2, 1) or (1, 2)

class Rook(ChessPiece):
    def __str__(self):
        return 'R' if self.color == 'white' else 'r'  # String representation for Rook

    def is_valid_move(self, start, end, board):
        """
        Checks if the Rook can move from start to end position.
        
        Parameters:
        start (tuple): Start position (row, col)
        end (tuple): End position (row, col)
        board (list): Current state of the board
        
        Returns:
        bool: True if the move is valid, False otherwise
        """
        start_row, start_col = start
        end_row, end_col = end
        if start_row == end_row or start_col == end_col:
            return self.can_move_to(end, board)  # Rook moves any number of squares along a row or column
        return False

class Pawn(ChessPiece):
    def __str__(self):
        return 'P' if self.color == 'white' else 'p'  # String representation for Pawn

    def is_valid_move(self, start, end, board):
        """
        Checks if the Pawn can move from start to end position.
        
        Parameters:
        start (tuple): Start position (row, col)
        end (tuple): End position (row, col)
        board (list): Current state of the board
        
        Returns:
        bool: True if the move is valid, False otherwise
        """
        start_row, start_col = start
        end_row, end_col = end

        # Determine direction based on color
        direction = -1 if self.color == 'white' else 1
        # Determine starting row based on color
        start_row_standard = 6 if self.color == 'white' else 1

        if start_col == end_col:
            if end_row == start_row + direction:
                return board[end_row][end_col] is None  # Move one square forward if the end position is empty
            if start_row == start_row_standard and end_row == start_row + 2 * direction:
                # Move two squares forward from starting position if both intermediate and end positions are empty
                return board[end_row][end_col] is None and board[start_row + direction][start_col] is None

        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            # Move diagonally if capturing an opponent's piece
            return board[end_row][end_col] is not None and board[end_row][end_col].color != self.color
        
        return False

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

def parse_position(pos):
    """
    Parses a position in standard chess notation (e.g., 'e2') into row and column indices.
    
    Parameters:
    pos (str): Position in standard chess notation
    
    Returns:
    tuple: (row, col) indices
    """
    col = ord(pos[0]) - ord('a')  # Convert column letter to index (0-7)
    row = 8 - int(pos[1])  # Convert row number to index (0-7)
    return row, col

def main():
    """
    Main function to run the chess game. Continuously prompts the user for moves and updates the board.
    """
    board = Board()  # Create a new board
    while True:
        board.display()  # Display the current board
        move = input(f"{board.current_turn}'s move (e.g., e2 e4): ")  # Prompt user for move
        try:
            start, end = move.split()  # Split the input into start and end positions
            start_pos = parse_position(start)  # Parse start position
            end_pos = parse_position(end)  # Parse end position
            if not board.move_piece(start_pos, end_pos):  # Attempt to move the piece
                print("Invalid move, try again.")
        except ValueError:
            print("Invalid input format, please use the format 'e2 e4'.")  # Handle incorrect input format

if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly