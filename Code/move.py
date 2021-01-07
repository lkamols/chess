from constants import *
"""
Class defining a move, takes a piece to an end location
"""

def pos_to_square(row, col):
    return chr(ord('a') + col) + str(row+1)

class Move:

    def __init__(self, piece, end_row, end_col, 
            kill=NO_KILL, en_passant=False, castle=False):
        self.piece = piece
        self.end_row = end_row
        self.end_col = end_col
        self.kill = kill
        self.en_passant = en_passant
        self.castle = castle

    """
    the move as a string
    """
    def short_representation(self):
        return pos_to_square(self.piece.get_row(), self.piece.get_col()) + \
                pos_to_square(self.end_row, self.end_col)

    """
    full move information as a string
    """
    def to_string(self):
        ret = "%s at %s " % (self.piece.get_name(), pos_to_square(self.piece.get_row(), self.piece.get_col()))
        if self.kill == NO_KILL:
            ret += "moves to "
        else:
            ret += "kills %s at " % (self.kill.get_name())
        ret += pos_to_square(self.end_row, self.end_col)
        return ret
