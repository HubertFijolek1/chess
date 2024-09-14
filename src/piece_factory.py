from chess_piece import King, Queen, Rook, Bishop, Knight, Pawn
from constants import WHITE, BLACK

class PieceFactory:
    @staticmethod
    def create_piece(symbol: str, color: str):
        piece_classes = {
            'K': King,
            'Q': Queen,
            'R': Rook,
            'B': Bishop,
            'N': Knight,
            'P': Pawn
        }
        piece_class = piece_classes.get(symbol.upper())
        if piece_class:
            return piece_class(color)
        else:
            raise ValueError(f"Unknown piece symbol: {symbol}")
