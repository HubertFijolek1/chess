from chess_piece import King, Queen, Rook, Bishop, Knight, Pawn
from constants import WHITE, BLACK
from piece_factory import PieceFactory
from utils import parse_position, position_to_notation
import logging
from collections import defaultdict
from copy import deepcopy
import pickle  # Import pickle for serialization
import os  # For file existence checks


logging.basicConfig(level=logging.INFO)


class Move:
    def __init__(self, start, end, piece, captured_piece, special_move=None, promotion_piece=None):
        self.start = start  # Tuple (row, col)
        self.end = end      # Tuple (row, col)
        self.piece = piece  # ChessPiece object that moved
        self.captured_piece = captured_piece  # ChessPiece object that was captured, if any
        self.special_move = special_move  # String indicating special move type ('en_passant', 'castling', 'promotion', etc.)
        self.promotion_piece = promotion_piece  # The piece to which a pawn was promoted, if any


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  # Initialize an 8x8 grid with None
        self.current_turn = WHITE  # White starts first
        self.setup_board()  # Set up the board with initial positions
        self.game_over = False  # Flag to indicate if the game has ended
        self.last_move = None  # Track the last move made (start, end)
        self.move_counter = 0  # For the fifty-move rule
        self.position_history = defaultdict(int)  # For threefold repetition
        self.move_history = []  # Stack to track move history for undo functionality
        self.update_position_history()  # Initialize position history

    def setup_board(self) -> None:
        """
        Sets up the board with initial positions for all pieces.
        """
        back_rank_symbols = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

        # Set up black pieces
        for col, symbol in enumerate(back_rank_symbols):
            self.grid[0][col] = PieceFactory.create_piece(symbol, BLACK)
            self.grid[1][col] = PieceFactory.create_piece('P', BLACK)

        # Set up white pieces
        for col, symbol in enumerate(back_rank_symbols):
            self.grid[7][col] = PieceFactory.create_piece(symbol, WHITE)
            self.grid[6][col] = PieceFactory.create_piece('P', WHITE)

    def display(self) -> None:
        """
        Displays the current state of the board with column letters and row numbers.
        """
        print("  a b c d e f g h")  # Print column headers
        for row in range(8):
            row_display = [str(piece) if piece else '.' for piece in self.grid[row]]  # Generate row display
            print(f"{8 - row} {' '.join(row_display)} {8 - row}")  # Print row with row numbers on both sides
        print("  a b c d e f g h")  # Print column headers

    def is_in_check(self, color: str) -> bool:
        """
        Determines if the king of the given color is in check.

        Parameters:
            color (str): The color of the king to check ('white' or 'black').

        Returns:
            bool: True if the king is in check, False otherwise.
        """
        king_position = None

        # Find the king's position
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_position = (row, col)
                    break
            if king_position:
                break

        if not king_position:
            logging.error(f"{color.capitalize()} king not found on the board!")
            return False  # King not found; should not happen

        # Check if any opposing piece can move to the king's position
        opponent_color = BLACK if color == WHITE else WHITE
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece is not None and piece.color == opponent_color:
                    if piece.is_valid_move((row, col), king_position, self, ignore_checks=True):
                        return True  # King is in check
        return False  # King is not in check

    def has_legal_moves(self, color: str) -> bool:
        """
        Checks if the player of the given color has any legal moves left.

        Parameters:
            color (str): The color of the player ('white' or 'black').

        Returns:
            bool: True if the player has at least one legal move, False otherwise.
        """
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece is not None and piece.color == color:
                    for dest_row in range(8):
                        for dest_col in range(8):
                            if piece.is_valid_move((row, col), (dest_row, dest_col), self):
                                # Simulate the move
                                captured_piece = self.grid[dest_row][dest_col]
                                original_piece = self.grid[row][col]
                                self.grid[dest_row][dest_col] = piece
                                self.grid[row][col] = None

                                # Check if the move would leave the king in check
                                if not self.is_in_check(color):
                                    # Undo the move
                                    self.grid[row][col] = original_piece
                                    self.grid[dest_row][dest_col] = captured_piece
                                    return True  # Found at least one legal move

                                # Undo the move
                                self.grid[row][col] = original_piece
                                self.grid[dest_row][dest_col] = captured_piece
        return False  # No legal moves found

    def is_checkmate(self, color: str) -> bool:
        """
        Determines if the player of the given color is in checkmate.

        Parameters:
            color (str): The color of the player to check ('white' or 'black').

        Returns:
            bool: True if the player is in checkmate, False otherwise.
        """
        if self.is_in_check(color) and not self.has_legal_moves(color):
            return True
        return False

    def is_stalemate(self, color: str) -> bool:
        """
        Determines if the player of the given color is in stalemate.

        Parameters:
            color (str): The color of the player to check ('white' or 'black').

        Returns:
            bool: True if the player is in stalemate, False otherwise.
        """
        if not self.is_in_check(color) and not self.has_legal_moves(color):
            return True
        return False

    def is_fifty_move_rule(self) -> bool:
        """
        Determines if the fifty-move rule applies.

        Returns:
            bool: True if fifty moves have been made without any pawn movement or captures, False otherwise.
        """
        return self.move_counter >= 100  # 100 half-moves equal 50 full moves

    def is_threefold_repetition(self) -> bool:
        """
        Determines if the threefold repetition rule applies.

        Returns:
            bool: True if the same position has occurred three times with the same player to move, False otherwise.
        """
        return self.position_history[self.serialize_board()] >= 3

    def is_draw(self) -> bool:
        """
        Determines if any draw condition applies.

        Returns:
            bool: True if the game is a draw, False otherwise.
        """
        return self.is_fifty_move_rule() or self.is_threefold_repetition()

    def is_square_under_attack(self, position: tuple, by_color: str) -> bool:
        """
        Determines if a given square is under attack by any piece of the specified color.

        Parameters:
            position (tuple): The position to check (row, col).
            by_color (str): The color of the attacking pieces ('white' or 'black').

        Returns:
            bool: True if the square is under attack, False otherwise.
        """
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece is not None and piece.color == by_color:
                    if piece.is_valid_move((row, col), position, self, ignore_checks=True):
                        return True
        return False

    def get_all_legal_moves(self, color: str) -> list:
        """
        Retrieves all legal moves for the given color.

        Parameters:
            color (str): The color of the player ('white' or 'black').

        Returns:
            list: A list of tuples representing legal moves in the format ((start_row, start_col), (end_row, end_col)).
        """
        legal_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece is not None and piece.color == color:
                    for dest_row in range(8):
                        for dest_col in range(8):
                            if piece.is_valid_move((row, col), (dest_row, dest_col), self):
                                # Simulate the move
                                captured_piece = self.grid[dest_row][dest_col]
                                original_piece = self.grid[row][col]
                                self.grid[dest_row][dest_col] = piece
                                self.grid[row][col] = None

                                # Handle en passant capture
                                special_move = None
                                if isinstance(piece, Pawn) and (dest_col != col) and captured_piece is None:
                                    direction = 1 if piece.color == WHITE else -1
                                    captured_pawn_pos = (dest_row + direction, dest_col)
                                    captured_pawn = self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]]
                                    if isinstance(captured_pawn, Pawn) and captured_pawn.color != piece.color:
                                        captured_piece = captured_pawn
                                        special_move = 'en_passant'
                                        self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]] = None

                                # Handle castling
                                if isinstance(piece, King) and abs(dest_col - col) == 2:
                                    special_move = 'castling'

                                # Check if the move would leave the king in check
                                if not self.is_in_check(color):
                                    legal_moves.append(((row, col), (dest_row, dest_col)))

                                # Undo the move
                                self.grid[row][col] = original_piece
                                self.grid[dest_row][dest_col] = captured_piece

                                # Restore captured pawn if en passant was simulated
                                if special_move == 'en_passant' and captured_piece is not None:
                                    self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]] = captured_pawn

        return legal_moves

    def promote_pawn(self, color: str, position: tuple) -> None:
        """
        Promotes a pawn at the given position to a chosen piece.

        Parameters:
            color (str): The color of the pawn to promote.
            position (tuple): The position of the pawn (row, col).

        Returns:
            ChessPiece: The newly promoted piece.
        """
        while True:
            choice = input("Promote pawn to (Q/R/B/N): ").upper()
            if choice in ['Q', 'R', 'B', 'N']:
                new_piece = PieceFactory.create_piece(choice, color)
                self.grid[position[0]][position[1]] = new_piece
                new_piece.move()  # Mark the new piece as moved if necessary
                logging.info(f"Pawn promoted to {new_piece} at {position_to_notation(position)}")
                # Reset move counter after promotion
                self.move_counter = 0
                return new_piece
            else:
                print("Invalid choice. Please select Q, R, B, or N.")

    def move_piece(self, start: tuple, end: tuple) -> bool:
        """
        Moves a piece from the start position to the end position if the move is valid and doesn't put own king in check.
        After a successful move, checks if the opponent's king is in checkmate or if a draw condition is met.

        Parameters:
            start (tuple): Starting position (row, col).
            end (tuple): Ending position (row, col).

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        start_row, start_col = start
        end_row, end_col = end
        piece = self.grid[start_row][start_col]

        if piece is None:
            start_notation = position_to_notation(start)
            print(f"No piece at starting position {start_notation}")
            return False

        if piece.color != self.current_turn:
            start_notation = position_to_notation(start)
            print(f"It's {self.current_turn}'s turn, but the piece at {start_notation} is {piece.color}")
            return False  # It's not the player's turn

        if not piece.is_valid_move(start, end, self):
            start_notation = position_to_notation(start)
            end_notation = position_to_notation(end)
            print(f"Invalid move for {piece} from {start_notation} to {end_notation}")
            return False  # The move is not valid for this piece

        # Prepare move record
        captured_piece = self.grid[end_row][end_col]
        special_move = None
        promotion_piece = None

        # Handle en passant capture
        if isinstance(piece, Pawn):
            if (end_col != start_col) and (captured_piece is None):
                # This is an en passant capture
                direction = 1 if piece.color == WHITE else -1
                captured_pawn_pos = (end_row + direction, end_col)
                captured_pawn = self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]]
                if isinstance(captured_pawn, Pawn) and captured_pawn.color != piece.color:
                    captured_piece = captured_pawn
                    self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]] = None
                    special_move = 'en_passant'
                    logging.info(f"{piece} captures {captured_piece} en passant at {position_to_notation(captured_pawn_pos)}")
                    # Reset move counter after capture
                    self.move_counter = 0
                else:
                    # Not a valid en passant capture
                    print("Invalid en passant capture.")
                    return False

        # Handle castling
        if isinstance(piece, King):
            if abs(end_col - start_col) == 2:
                # Castling move
                if end_col == start_col + 2:
                    # Kingside castling
                    rook_start = (start_row, 7)
                    rook_end = (start_row, 5)
                elif end_col == start_col - 2:
                    # Queenside castling
                    rook_start = (start_row, 0)
                    rook_end = (start_row, 3)
                else:
                    return False  # Invalid castling move

                rook = self.grid[rook_start[0]][rook_start[1]]
                if isinstance(rook, Rook):
                    self.grid[rook_end[0]][rook_end[1]] = rook
                    self.grid[rook_start[0]][rook_start[1]] = None
                    rook.move()  # Mark the rook as moved
                    logging.info(f"{rook} moved from {position_to_notation(rook_start)} to {position_to_notation(rook_end)}")
                    special_move = 'castling'
                else:
                    # No rook to castle with
                    print("No rook available for castling.")
                    # Undo the king move
                    self.grid[start_row][start_col] = piece
                    self.grid[end_row][end_col] = captured_piece
                    return False

        # Handle pawn promotion
        if isinstance(piece, Pawn):
            promotion_row = 0 if piece.color == WHITE else 7
            if end_row == promotion_row:
                promotion_piece = self.promote_pawn(piece.color, (end_row, end_col))
                special_move = 'promotion'

        # Record the current state for undo
        move_record = Move(
            start=start,
            end=end,
            piece=piece,
            captured_piece=captured_piece,
            special_move=special_move,
            promotion_piece=promotion_piece
        )
        self.move_history.append(move_record)

        # Move the piece
        self.grid[end_row][end_col] = piece
        self.grid[start_row][start_col] = None

        # Handle pawn promotion (if not already handled)
        if isinstance(piece, Pawn) and promotion_piece:
            self.grid[end_row][end_col] = promotion_piece

        # Mark the piece as having moved
        piece.move()

        # Update the last move
        self.last_move = (start, end)

        # Update move counter
        if isinstance(piece, Pawn) or captured_piece is not None:
            self.move_counter = 0  # Reset counter on pawn move or capture
        else:
            self.move_counter += 1

        # Update position history
        self.update_position_history()

        # Move is valid; log the capture if any
        if captured_piece is not None and not (isinstance(piece, Pawn) and special_move == 'en_passant'):
            logging.info(f"{piece} captures {captured_piece} at {position_to_notation(end)}")

        # Switch turns
        self.current_turn = BLACK if self.current_turn == WHITE else WHITE  # Switch turns

        # Check for draw conditions
        if self.is_fifty_move_rule():
            print("Draw by fifty-move rule.")
            logging.info("Game ended in a draw by fifty-move rule.")
            self.game_over = True
            return True  # Move was successful

        if self.is_threefold_repetition():
            print("Draw by threefold repetition.")
            logging.info("Game ended in a draw by threefold repetition.")
            self.game_over = True
            return True  # Move was successful

        # Check for checkmate or stalemate
        opponent_color = BLACK if piece.color == WHITE else WHITE
        if self.is_checkmate(opponent_color):
            print(f"Checkmate! {piece.color.capitalize()} wins!")
            logging.info(f"Game ended in checkmate. {piece.color.capitalize()} wins!")
            self.game_over = True
        elif self.is_stalemate(opponent_color):
            print(f"Stalemate! The game is a draw.")
            logging.info("Game ended in a stalemate.")
            self.game_over = True
        elif self.is_in_check(opponent_color):
            print(f"Check to {opponent_color}!")

        return True  # Move was successful

    def undo_move(self) -> bool:
        """
        Undoes the last move made.

        Returns:
            bool: True if a move was undone successfully, False otherwise.
        """
        if not self.move_history:
            print("No moves to undo.")
            return False

        last_move = self.move_history.pop()

        # Move the piece back to the start position
        self.grid[last_move.start[0]][last_move.start[1]] = last_move.piece
        self.grid[last_move.end[0]][last_move.end[1]] = last_move.captured_piece

        # Handle special moves
        if last_move.special_move == 'en_passant':
            direction = 1 if last_move.piece.color == WHITE else -1
            captured_pawn_pos = (last_move.end[0] + direction, last_move.end[1])
            self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]] = last_move.captured_piece
        elif last_move.special_move == 'castling':
            # Move the rook back to its original position
            if last_move.end[1] == 5:
                # Kingside castling
                rook_start = (last_move.start[0], 7)
                rook_end = (last_move.start[0], 5)
            elif last_move.end[1] == 3:
                # Queenside castling
                rook_start = (last_move.start[0], 0)
                rook_end = (last_move.start[0], 3)
            else:
                print("Invalid castling undo state.")
                return False
            rook = self.grid[rook_end[0]][rook_end[1]]
            self.grid[rook_start[0]][rook_start[1]] = rook
            self.grid[rook_end[0]][rook_end[1]] = None
            rook.has_moved = False
        elif last_move.special_move == 'promotion':
            # Replace the promoted piece with a pawn
            self.grid[last_move.end[0]][last_move.end[1]] = None
            self.grid[last_move.start[0]][last_move.start[1]] = Pawn(last_move.piece.color)

        # Restore the move counter
        if isinstance(last_move.piece, Pawn) or last_move.captured_piece is not None:
            # If the last move was a pawn move or capture, reset the move counter appropriately
            # This simplistic approach resets the counter; for more accuracy, more tracking is needed
            self.move_counter = 0
        else:
            self.move_counter -= 1 if self.move_counter > 0 else 0

        # Restore the position history
        current_serialized = self.serialize_board()
        self.position_history[current_serialized] -= 1

        # Switch turns back
        self.current_turn = BLACK if self.current_turn == WHITE else WHITE

        # Clear game_over if it was set by the last move
        self.game_over = False

        logging.info(f"Undo move: {last_move.piece} from {position_to_notation(last_move.start)} to {position_to_notation(last_move.end)}")
        print("Last move undone.")

        return True

    def save_game(self, filename: str) -> bool:
        """
        Saves the current game state to a file.

        Parameters:
            filename (str): The name of the file to save the game state.

        Returns:
            bool: True if the game was saved successfully, False otherwise.
        """
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self, file)
            logging.info(f"Game saved to {filename}.")
            print(f"Game successfully saved to {filename}.")
            return True
        except Exception as e:
            logging.error(f"Failed to save game to {filename}: {e}")
            print(f"Failed to save game to {filename}.")
            return False

    def load_game(self, filename: str) -> bool:
        """
        Loads a game state from a file.

        Parameters:
            filename (str): The name of the file to load the game state from.

        Returns:
            bool: True if the game was loaded successfully, False otherwise.
        """
        if not os.path.exists(filename):
            print(f"Save file '{filename}' does not exist.")
            return False
        try:
            with open(filename, 'rb') as file:
                loaded_board = pickle.load(file)
            # Restore all attributes
            self.grid = loaded_board.grid
            self.current_turn = loaded_board.current_turn
            self.game_over = loaded_board.game_over
            self.last_move = loaded_board.last_move
            self.move_counter = loaded_board.move_counter
            self.position_history = loaded_board.position_history
            self.move_history = loaded_board.move_history
            logging.info(f"Game loaded from {filename}.")
            print(f"Game successfully loaded from {filename}.")
            return True
        except Exception as e:
            logging.error(f"Failed to load game from {filename}: {e}")
            print(f"Failed to load game from {filename}.")
            return False

    def serialize_board(self) -> str:
        """
        Serializes the current board state into a string for comparison.

        Returns:
            str: A string representation of the current board state.
        """
        board_str = ""
        for row in self.grid:
            for piece in row:
                board_str += str(piece) if piece else "."
            board_str += "/"
        board_str += self.current_turn
        return board_str

    def update_position_history(self):
        """
        Serializes the current board state and updates the position history.
        """
        serialized = self.serialize_board()
        self.position_history[serialized] += 1

    def get_all_legal_moves(self, color: str) -> list:
        """
        Retrieves all legal moves for the given color.

        Parameters:
            color (str): The color of the player ('white' or 'black').

        Returns:
            list: A list of tuples representing legal moves in the format ((start_row, start_col), (end_row, end_col)).
        """
        legal_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece is not None and piece.color == color:
                    for dest_row in range(8):
                        for dest_col in range(8):
                            if piece.is_valid_move((row, col), (dest_row, dest_col), self):
                                # Simulate the move
                                captured_piece = self.grid[dest_row][dest_col]
                                original_piece = self.grid[row][col]
                                self.grid[dest_row][dest_col] = piece
                                self.grid[row][col] = None

                                # Handle en passant capture
                                special_move = None
                                if isinstance(piece, Pawn) and (dest_col != col) and captured_piece is None:
                                    direction = 1 if piece.color == WHITE else -1
                                    captured_pawn_pos = (dest_row + direction, dest_col)
                                    captured_pawn = self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]]
                                    if isinstance(captured_pawn, Pawn) and captured_pawn.color != piece.color:
                                        captured_piece = captured_pawn
                                        special_move = 'en_passant'
                                        self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]] = None

                                # Handle castling
                                if isinstance(piece, King) and abs(dest_col - col) == 2:
                                    special_move = 'castling'

                                # Check if the move would leave the king in check
                                if not self.is_in_check(color):
                                    legal_moves.append(((row, col), (dest_row, dest_col)))

                                # Undo the move
                                self.grid[row][col] = original_piece
                                self.grid[dest_row][dest_col] = captured_piece

                                # Restore captured pawn if en passant was simulated
                                if special_move == 'en_passant' and captured_piece is not None:
                                    self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]] = captured_pawn

        return legal_moves