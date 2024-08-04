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