from constants import WHITE, BLACK

class ChessPiece:
    def __init__(self, color: str):
        self.color = color  # Color of the piece (WHITE or BLACK)

    def __str__(self) -> str:
        return 'Piece'  # Default string representation of a piece

    def can_capture_or_move_to(self, end: tuple, board) -> bool:
        """
        Checks if the piece can move to the given end position or capture an opponent's piece there.
        """
        end_row, end_col = end
        target_piece = board.grid[end_row][end_col]
        if target_piece is None:
            return True  # The end position is empty
        if target_piece.color != self.color:
            return True  # Can capture opponent's piece
        return False  # Can't move to a position occupied by own piece

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

class Rook(ChessPiece):
    def is_valid_move(self, start: tuple, end: tuple, board) -> bool:
        """
        Checks if the Rook can move from start to end position.
        """
        start_row, start_col = start
        end_row, end_col = end
        if start_row == end_row or start_col == end_col:
            if board.is_path_clear(start, end) and self.can_capture_or_move_to(end, board):
                return True  # Rook moves any number of squares along a row or column
        return False

class Bishop(ChessPiece):
    def is_valid_move(self, start: tuple, end: tuple, board) -> bool:
        """
        Checks if the Bishop can move from start to end position.
        """
        start_row, start_col = start
        end_row, end_col = end
        if abs(end_row - start_row) == abs(end_col - start_col):
            if board.is_path_clear(start, end) and self.can_capture_or_move_to(end, board):
                return True  # Bishop moves any number of squares diagonally
        return False

class Queen(ChessPiece):
    def is_valid_move(self, start: tuple, end: tuple, board) -> bool:
        """
        Checks if the Queen can move from start to end position.
        """
        start_row, start_col = start
        end_row, end_col = end
        row_diff = end_row - start_row
        col_diff = end_col - start_col
        if abs(row_diff) == abs(col_diff) or start_row == end_row or start_col == end_col:
            if board.is_path_clear(start, end) and self.can_capture_or_move_to(end, board):
                return True  # Queen moves any number of squares along a row, column, or diagonal
        return False

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