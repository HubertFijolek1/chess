class ChessPiece:
    def __init__(self, color):
        """
        Constructor for the ChessPiece class.
        
        Args:
            color (str): The color of the piece ('white' or 'black').
        """
        self.color = color

    def __str__(self):
        """
        String representation of the piece. This should be overridden by subclasses.
        
        Returns:
            str: The string representation of the piece.
        """
        return 'Piece'

class King(ChessPiece):
    def __str__(self):
        """
        Returns the string representation of the King piece.
        
        Returns:
            str: 'K' for a white king, 'k' for a black king.
        """
        return 'K' if self.color == 'white' else 'k'

    def is_valid_move(self, start, end, board):
        """
        Validate if the move is valid for the King piece.
        King moves one square in any direction.
        
        Args:
            start (tuple): The starting position of the piece (row, col).
            end (tuple): The ending position of the piece (row, col).
            board (list): The current state of the board.
        
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        # Calculate the difference in rows and columns between the start and end positions.
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])
        
        # King moves one square in any direction, so row and column differences must both be <= 1.
        return row_diff <= 1 and col_diff <= 1

class Queen(ChessPiece):
    def __str__(self):
        """
        Returns the string representation of the Queen piece.
        
        Returns:
            str: 'Q' for a white queen, 'q' for a black queen.
        """
        return 'Q' if self.color == 'white' else 'q'

    def is_valid_move(self, start, end, board):
        """
        Validate if the move is valid for the Queen piece.
        Queen moves any number of squares along a row, column, or diagonal.
        
        Args:
            start (tuple): The starting position of the piece (row, col).
            end (tuple): The ending position of the piece (row, col).
            board (list): The current state of the board.
        
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])
        
        # Queen moves horizontally, vertically, or diagonally.
        # So the move is valid if it is a valid rook move or a valid bishop move.
        if row_diff != col_diff and start[0] != end[0] and start[1] != end[1]:
            return False
        
        # Ensure the path between start and end is clear.
        if start[0] == end[0]:  # Horizontal move
            step = 1 if start[1] < end[1] else -1
            for col in range(start[1] + step, end[1], step):
                if board[start[0]][col] is not None:
                    return False
        elif start[1] == end[1]:  # Vertical move
            step = 1 if start[0] < end[0] else -1
            for row in range(start[0] + step, end[0], step):
                if board[row][start[1]] is not None:
                    return False
        else:  # Diagonal move
            row_step = 1 if start[0] < end[0] else -1
            col_step = 1 if start[1] < end[1] else -1
            for i in range(1, row_diff):
                if board[start[0] + i * row_step][start[1] + i * col_step] is not None:
                    return False

        return True

class Rook(ChessPiece):
    def __str__(self):
        """
        Returns the string representation of the Rook piece.
        
        Returns:
            str: 'R' for a white rook, 'r' for a black rook.
        """
        return 'R' if self.color == 'white' else 'r'

    def is_valid_move(self, start, end, board):
        """
        Validate if the move is valid for the Rook piece.
        Rook moves any number of squares along a row or column.
        
        Args:
            start (tuple): The starting position of the piece (row, col).
            end (tuple): The ending position of the piece (row, col).
            board (list): The current state of the board.
        
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        # Check if the move is in the same row or column.
        # Rooks can only move in straight lines horizontally or vertically.
        if start[0] != end[0] and start[1] != end[1]:
            return False

        # Ensure the path between start and end is clear.
        # This involves checking all squares between the start and end positions
        # to ensure there are no pieces in the way.
        
        if start[0] == end[0]:  # Horizontal move
            # Determine the direction of movement.
            # If moving to the right, step is +1. If moving to the left, step is -1.
            step = 1 if start[1] < end[1] else -1
            
            # Loop through all columns between start and end (exclusive) and check if they are empty.
            for col in range(start[1] + step, end[1], step):
                if board[start[0]][col] is not None:
                    return False  # There is a piece in the way.
        else:  # Vertical move
            # Determine the direction of movement.
            # If moving upwards, step is +1. If moving downwards, step is -1.
            step = 1 if start[0] < end[0] else -1
            
            # Loop through all rows between start and end (exclusive) and check if they are empty.
            for row in range(start[0] + step, end[0], step):
                if board[row][start[1]] is not None:
                    return False  # There is a piece in the way.

        # If all checks pass, the move is valid.
        return True

class Bishop(ChessPiece):
    def __str__(self):
        """
        Returns the string representation of the Bishop piece.
        
        Returns:
            str: 'B' for a white bishop, 'b' for a black bishop.
        """
        return 'B' if self.color == 'white' else 'b'

    def is_valid_move(self, start, end, board):
        """
        Validate if the move is valid for the Bishop piece.
        Bishop moves any number of squares diagonally.
        
        Args:
            start (tuple): The starting position of the piece (row, col).
            end (tuple): The ending position of the piece (row, col).
            board (list): The current state of the board.
        
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        # Calculate the difference in rows and columns between the start and end positions.
        # Bishops move diagonally, so the absolute difference between the row and column
        # indices must be the same for a move to be diagonal.
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])
        
        # If the move is not diagonal, it is invalid.
        if row_diff != col_diff:
            return False

        # Ensure the path between start and end is clear.
        # This involves checking all squares along the diagonal path between
        # the start and end positions to ensure there are no pieces in the way.
        
        # Determine the direction of movement.
        # row_step and col_step will be +1 or -1 depending on the direction.
        row_step = 1 if start[0] < end[0] else -1
        col_step = 1 if start[1] < end[1] else -1
        
        # Loop through all squares between start and end (exclusive) and check if they are empty.
        for i in range(1, row_diff):
            if board[start[0] + i * row_step][start[1] + i * col_step] is not None:
                return False  # There is a piece in the way.

        # If all checks pass, the move is valid.
        return True
class Knight(ChessPiece):
    def __str__(self):
        """
        Returns the string representation of the Knight piece.
        
        Returns:
            str: 'N' for a white knight, 'n' for a black knight.
        """
        return 'N' if self.color == 'white' else 'n'

    def is_valid_move(self, start, end, board):
        """
        Validate if the move is valid for the Knight piece.
        Knight moves in an L-shape: two squares in one direction and then one square perpendicular.
        
        Args:
            start (tuple): The starting position of the piece (row, col).
            end (tuple): The ending position of the piece (row, col).
            board (list): The current state of the board.
        
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])
        
        # Knight moves in an L-shape: two squares in one direction and then one square perpendicular.
        # Therefore, the row and column differences must be either (2, 1) or (1, 2).
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

class Pawn(ChessPiece):
    def __str__(self):
        """
        Returns the string representation of the Pawn piece.
        
        Returns:
            str: 'P' for a white pawn, 'p' for a black pawn.
        """
        return 'P' if self.color == 'white' else 'p'

    def is_valid_move(self, start, end, board):
        """
        Validate if the move is valid for the Pawn piece.
        Pawn moves forward one square, with the option to move two squares on their first move.
        Pawns capture diagonally.
        
        Args:
            start (tuple): The starting position of the piece (row, col).
            end (tuple): The ending position of the piece (row, col).
            board (list): The current state of the board.
        
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        direction = 1 if self.color == 'white' else -1
        start_row, start_col = start
        end_row, end_col = end
        
        # Move forward one square
        if start_col == end_col:
            if end_row - start_row == direction:
                return board[end_row][end_col] is None
            # Move forward two squares from starting position
            if (start_row == 1 and self.color == 'black') or (start_row == 6 and self.color == 'white'):
                return end_row - start_row == 2 * direction and board[end_row][end_col] is None
        # Capture diagonally
        if abs(start_col - end_col) == 1 and end_row - start_row == direction:
            return board[end_row][end_col] is not None and board[end_row][end_col].color != self.color
        return False

class Board:
    def __init__(self):
        """
        Initializes the chessboard with pieces in their initial positions.
        Sets the current turn to 'white'.
        """
        self.board = self.create_initial_board()
        self.current_turn = 'white'  # Track the current player's turn

    def create_initial_board(self):
        """
        Creates an 8x8 grid representing the chessboard.
        Places pieces in their starting positions.

        Returns:
            list: 2D list representing the chessboard with pieces.
        """
        board = [[None for _ in range(8)] for _ in range(8)]
        board[0] = [Rook('black'), Knight('black'), Bishop('black'), Queen('black'),
                    King('black'), Bishop('black'), Knight('black'), Rook('black')]
        board[1] = [Pawn('black') for _ in range(8)]
        
        # Place white pieces in the last two rows
        board[6] = [Pawn('white') for _ in range(8)]
        board[7] = [Rook('white'), Knight('white'), Bishop('white'), Queen('white'),
                    King('white'), Bishop('white'), Knight('white'), Rook('white')]
        return board

    def display(self):
        """
        Prints the current state of the chessboard to the console.
        """
        # Print column labels at the top of the board
        print("  a b c d e f g h")
        
        # Enumerate through each row of the board to get both the index and the row content
        for row_index, row in enumerate(self.board):
            # Print row label on the left side (8 - row_index for 1-based index starting from the bottom)
            print(8 - row_index, end=" ")
            
            # Print each piece in the row or a '.' if the square is empty
            for piece in row:
                print('.' if piece is None else str(piece), end=" ")
            print(8 - row_index)
        
        # Print column labels at the bottom of the board
        print("  a b c d e f g h")

    def move_piece(self, start, end):
        """
        Moves a piece from the start position to the end position on the board
        if the move is valid according to the piece's movement rules.

        Args:
            start (tuple): The starting position of the piece (row, col).
            end (tuple): The ending position of the piece (row, col).

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]
        
        # Check if there is a piece at the start position and if it belongs to the current player
        if piece and piece.color == self.current_turn and piece.is_valid_move(start, end, self.board):
            self.board[end_row][end_col] = piece  # Move the piece to the end position
            self.board[start_row][start_col] = None  # Remove the piece from the start position
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'  # Switch turns
            return True
        return False  # Invalid move

def main():
    """
    Main function to create a Board object and handle user input for moves.
    Uses a loop to display the board and process moves.
    """
    board = Board()
    while True:
        board.display()
        move = input(f"{board.current_turn}'s move (e.g., e2 e4): ")
        try:
            start, end = move.split()
            start_pos = parse_position(start)
            end_pos = parse_position(end)
            print(f"Move from {start_pos} to {end_pos}")  # For demonstration
        except ValueError:
            print("Invalid input format, please use the format 'e2 e4'.")

if __name__ == "__main__":
    main()