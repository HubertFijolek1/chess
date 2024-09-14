def parse_position(pos: str) -> tuple:
    """
    Parses a position string (e.g., 'e2') and converts it to board coordinates.
    """
    col = ord(pos[0].lower()) - ord('a')
    row = 8 - int(pos[1])
    return row, col

def position_to_notation(position: tuple) -> str:
    """
    Converts board coordinates to position string notation (e.g., (6, 3) -> 'd2').
    """
    row, col = position
    col_letter = chr(col + ord('a'))
    row_number = str(8 - row)
    return f"{col_letter}{row_number}"