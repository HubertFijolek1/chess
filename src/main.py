from board import Board
from utils import parse_position


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