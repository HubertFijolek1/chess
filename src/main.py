from board import Board
from utils import parse_position, position_to_notation
from constants import WHITE, BLACK
import logging

logging.basicConfig(level=logging.INFO)


def main():
    """
    Main function to run the chess game. Continuously prompts the user for moves and updates the board.
    Ends the game when a checkmate, stalemate, or draw condition is detected.
    Allows players to undo the last move, save the game, or load a saved game using specific commands.
    """
    board = Board()  # Create a new board
    while not board.game_over:
        board.display()  # Display the current board
        move = input(f"{board.current_turn.capitalize()}'s move (e.g., e2 e4), 'undo', 'save <filename>', or 'load <filename>': ").strip()
        if move.lower() == 'undo':
            if board.undo_move():
                print("Move undone.")
            else:
                print("Cannot undo move.")
            continue
        elif move.lower().startswith('save '):
            parts = move.split()
            if len(parts) != 2:
                print("Invalid save command format. Use 'save <filename>'.")
                continue
            filename = parts[1]
            board.save_game(filename)
            continue
        elif move.lower().startswith('load '):
            parts = move.split()
            if len(parts) != 2:
                print("Invalid load command format. Use 'load <filename>'.")
                continue
            filename = parts[1]
            if board.load_game(filename):
                print("Game loaded successfully.")
            else:
                print("Failed to load game.")
            continue
        try:
            start, end = move.strip().split()  # Split the input into start and end positions
            start_pos = parse_position(start)  # Parse start position
            end_pos = parse_position(end)  # Parse end position
            if not board.move_piece(start_pos, end_pos):  # Attempt to move the piece
                print("Invalid move, try again.")
        except ValueError:
            print("Invalid input format, please use the format 'e2 e4', 'undo', 'save <filename>', or 'load <filename>'.")


if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly