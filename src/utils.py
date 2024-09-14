def parse_position(pos: str) -> tuple:
    """
    Parses a position string (e.g., 'e2') and converts it to board coordinates.
    """
    col = ord(pos[0].lower()) - ord('a')
    row = 8 - int(pos[1])
    return row, col
