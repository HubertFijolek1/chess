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
        String representation of the King piece.
        
        Returns:
            str: 'K' for white king, 'k' for black king.
        """
        return 'K' if self.color == 'white' else 'k'

class Queen(ChessPiece):
    def __str__(self):
        """
        String representation of the Queen piece.
        
        Returns:
            str: 'Q' for white queen, 'q' for black queen.
        """
        return 'Q' if self.color == 'white' else 'q'

class Rook(ChessPiece):
    def __str__(self):
        """
        String representation of the Rook piece.
        
        Returns:
            str: 'R' for white rook, 'r' for black rook.
        """
        return 'R' if self.color == 'white' else 'r'

class Bishop(ChessPiece):
    def __str__(self):
        """
        String representation of the Bishop piece.
        
        Returns:
            str: 'B' for white bishop, 'b' for black bishop.
        """
        return 'B' if self.color == 'white' else 'b'

class Knight(ChessPiece):
    def __str__(self):
        """
        String representation of the Knight piece.
        
        Returns:
            str: 'N' for white knight, 'n' for black knight.
        """
        return 'N' if self.color == 'white' else 'n'

class Pawn(ChessPiece):
    def __str__(self):
        """
        String representation of the Pawn piece.
        
        Returns:
            str: 'P' for white pawn, 'p' for black pawn.
        """
        return 'P' if self.color == 'white' else 'p'

class Board:
    def __init__(self):
        """
        Constructor for the Board class.
        Initializes the chessboard by calling the create_initial_board method.
        """
        self.board = self.create_initial_board()

    def create_initial_board(self):
        """
        Creates an 8x8 grid to represent the chessboard.
        Each square on the board is initialized to a ChessPiece object representing
        the pieces in their starting positions.

        Returns:
            list: A 2D list (8x8 grid) representing the chessboard with piece objects.
        """
        # Initialize an empty 8x8 grid
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Place black pieces in the first two rows
        board[0] = [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')]
        board[1] = [Pawn('black') for _ in range(8)]
        
        # Place white pieces in the last two rows
        board[6] = [Pawn('white') for _ in range(8)]
        board[7] = [Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'), Knight('white'), Rook('white')]
        
        return board

    def display(self):
        """
        Prints the current state of the chessboard to the console.
        Empty squares are represented by '.', and pieces are represented
        by their respective placeholders.
        """
        # Print column labels at the top of the board
        print("  a b c d e f g h")
        
        # Enumerate through each row of the board to get both the index and the row content
        for row_index, row in enumerate(self.board):
            # Print row label on the left side (8 - row_index for 1-based index starting from the bottom)
            print(8 - row_index, end=" ")
            
            # Print each piece in the row or a '.' if the square is empty
            for piece in row:
                print('.' if piece is None else piece, end=" ")
            
            # Print row label on the right side (same as the left for symmetry)
            print(8 - row_index)
        
        # Print column labels at the bottom of the board
        print("  a b c d e f g h")

def main():
    """
    Main function to create a Board object and display its initial state.
    This function is executed when the script is run directly.
    """
    board = Board()  # Create a new Board object
    board.display()  # Display the current state of the board

if __name__ == "__main__":
    main()  # Call the main function if this script is executed