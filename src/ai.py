import random
from board import Board, Move
from utils import position_to_notation
import logging

logging.basicConfig(level=logging.INFO)


class AIPlayer:
    def __init__(self, color: str, depth: int = 3):
        """
        Initializes the AI player with the specified color and search depth.

        Parameters:
            color (str): The color of the AI player ('white' or 'black').
            depth (int): The maximum depth the Minimax algorithm will explore.
        """
        self.color = color
        self.depth = depth
        logging.info(f"AI Player initialized as {self.color} with depth {self.depth}.")

    def choose_move(self, board: Board) -> tuple:
        """
        Chooses a move for the AI player based on the current board state using the Minimax algorithm.

        Parameters:
            board (Board): The current game board.

        Returns:
            tuple: A tuple containing the start and end positions ((start_row, start_col), (end_row, end_col)).
        """
        logging.info("AI is calculating the best move using Minimax...")
        best_score = float('-inf') if self.color == WHITE else float('inf')
        best_move = None
        legal_moves = board.get_all_legal_moves(self.color)

        for move_coords in legal_moves:
            move = self.create_move_object(move_coords, board)
            board.move_piece(move.start, move.end)
            score = self.minimax(board, self.depth - 1, float('-inf'), float('inf'), False)
            board.undo_move()

            if self.color == WHITE:
                if score > best_score:
                    best_score = score
                    best_move = move_coords
            else:
                if score < best_score:
                    best_score = score
                    best_move = move_coords

        if best_move is None and legal_moves:
            best_move = random.choice(legal_moves)  # Fallback to random move

        if best_move:
            logging.info(f"AI chooses to move from {position_to_notation(best_move[0])} to {position_to_notation(best_move[1])} with score {best_score}.")
        else:
            logging.info("AI has no valid moves to make.")
        return best_move

    def create_move_object(self, move_coords: tuple, board: Board) -> Move:
        """
        Creates a Move object from move coordinates.

        Parameters:
            move_coords (tuple): A tuple containing the start and end positions ((start_row, start_col), (end_row, end_col)).
            board (Board): The current game board.

        Returns:
            Move: A Move object representing the move.
        """
        start, end = move_coords
        piece = board.grid[start[0]][start[1]]
        captured_piece = board.grid[end[0]][end[1]]
        # Simplistic move object creation; may need to handle special moves
        return Move(start, end, piece, captured_piece)

    def minimax(self, board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool) -> int:
        """
        The Minimax algorithm with Alpha-Beta Pruning.

        Parameters:
            board (Board): The current game board.
            depth (int): The remaining depth to search.
            alpha (float): The best already explored option along the path to the maximizer.
            beta (float): The best already explored option along the path to the minimizer.
            is_maximizing (bool): True if the current layer is maximizing, False otherwise.

        Returns:
            int: The evaluation score of the board.
        """
        if depth == 0 or board.game_over:
            return board.evaluate_board(self.color)

        if is_maximizing:
            max_eval = float('-inf')
            moves = board.get_all_legal_moves(self.color)
            for move_coords in moves:
                move = self.create_move_object(move_coords, board)
                board.move_piece(move.start, move.end)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.undo_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            opponent_color = BLACK if self.color == WHITE else WHITE
            min_eval = float('inf')
            moves = board.get_all_legal_moves(opponent_color)
            for move_coords in moves:
                move = self.create_move_object(move_coords, board)
                board.move_piece(move.start, move.end)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.undo_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval