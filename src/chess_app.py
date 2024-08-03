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
        Each square on the board is initialized to a placeholder string representing
        the pieces in their starting positions.

        Returns:
            list: A 2D list (8x8 grid) representing the chessboard with piece placeholders.
        """
        # Initialize an empty 8x8 grid
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Place black pieces in the first two rows
        board[0] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        board[1] = ['p' for _ in range(8)]
        
        # Place white pieces in the last two rows
        board[6] = ['P' for _ in range(8)]
        board[7] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        
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