from board import Board
from ai import AIPlayer
from utils import parse_position, position_to_notation
from constants import WHITE, BLACK
import logging

logging.basicConfig(level=logging.INFO)


def main():
    """
    Main function to run the chess game. Continuously prompts the user for moves and updates the board.
    Ends the game when a checkmate, stalemate, or draw condition is detected.
    Allows players to undo the last move, save the game, or load a saved game using specific commands.
    Supports Human vs. Human and Human vs. AI game modes.
    """
    board = Board()  # Create a new board

    # Choose game mode
    while True:
        mode = input("Select game mode:\n1. Human vs Human\n2. Human vs AI\nEnter 1 or 2: ").strip()
        if mode == '1':
            ai_player = None
            print("Human vs Human selected.")
            break
        elif mode == '2':
            ai_color = ''
            while ai_color.lower() not in ['white', 'black']:
                ai_color = input("Should AI play as white or black? ").strip().lower()
                if ai_color not in ['white', 'black']:
                    print("Invalid choice. Please enter 'white' or 'black'.")
            ai_player = AIPlayer(ai_color, depth=3)  # You can adjust depth for difficulty
            print(f"Human vs AI selected. AI is playing as {ai_player.color}.")
            break
        else:
            print("Invalid selection. Please enter 1 or 2.")

    while not board.game_over:
        board.display()  # Display the current board

        # Determine if it's AI's turn
        if ai_player and board.current_turn == ai_player.color:
            print("AI is thinking...")
            move = ai_player.choose_move(board)
            if move is None:
                # AI has no legal moves
                if board.is_in_check(ai_player.color):
                    print(f"Checkmate! {WHITE if ai_player.color == BLACK else BLACK} wins!")
                    logging.info(f"Game ended in checkmate. {'White' if ai_player.color == BLACK else 'Black'} wins!")
                else:
                    print("Stalemate! The game is a draw.")
                    logging.info("Game ended in a stalemate.")
                board.game_over = True
                break
            success = board.move_piece(move[0], move[1])
            if not success:
                print("AI attempted an invalid move. This should not happen.")
                board.game_over = True
            continue

        # Prompt user for input
        move_input = input(f"{board.current_turn.capitalize()}'s move (e.g., e2 e4), 'undo', 'save <filename>', or 'load <filename>': ").strip()

        if move_input.lower() == 'undo':
            if board.undo_move():
                print("Move undone.")
            else:
                print("Cannot undo move.")
            continue
        elif move_input.lower().startswith('save '):
            parts = move_input.split()
            if len(parts) != 2:
                print("Invalid save command format. Use 'save <filename>'.")
                continue
            filename = parts[1]
            board.save_game(filename)
            continue
        elif move_input.lower().startswith('load '):
            parts = move_input.split()
            if len(parts) != 2:
                print("Invalid load command format. Use 'load <filename>'.")
                continue
            filename = parts[1]
            if board.load_game(filename):
                print("Game loaded successfully.")
            else:
                print("Failed to load game.")
            continue

        # Parse move input
        try:
            start, end = move_input.strip().split()  # Split the input into start and end positions
            start_pos = parse_position(start)  # Parse start position
            end_pos = parse_position(end)  # Parse end position
            if not board.move_piece(start_pos, end_pos):  # Attempt to move the piece
                print("Invalid move, try again.")
        except ValueError:
            print("Invalid input format, please use the format 'e2 e4', 'undo', 'save <filename>', or 'load <filename>'.")


if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly