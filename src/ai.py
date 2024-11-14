import random
from board import Board, Move
from utils import position_to_notation
import logging


class AIPlayer:
    def __init__(self, color: str):
        """
        Initializes the AI player with the specified color.

        Parameters:
            color (str): The color of the AI player ('white' or 'black').
        """
        self.color = color
        logging.info(f"AI Player initialized as {self.color}.")

    def choose_move(self, board: Board) -> tuple:
        """
        Chooses a move for the AI player based on the current board state.

        Parameters:
            board (Board): The current game board.

        Returns:
            tuple: A tuple containing the start and end positions ((start_row, start_col), (end_row, end_col)).
        """
        legal_moves = board.get_all_legal_moves(self.color)
        if not legal_moves:
            return None  # No legal moves available

        chosen_move = random.choice(legal_moves)
        logging.info(f"AI chooses to move from {position_to_notation(chosen_move[0])} to {position_to_notation(chosen_move[1])}.")
        return chosen_move