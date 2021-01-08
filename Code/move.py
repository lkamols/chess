from constants import *
"""
Class defining a move, takes a piece to an end location
"""

def pos_to_square(row, col):
    return chr(ord('a') + col) + str(row+1)

class Move:

    def __init__(self, piece, start_row, start_col, end_row, end_col, 
            kill=None, en_passant=False, castle=False, promotion=None):
        self.piece = piece
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.kill = kill
        self.en_passant = en_passant
        self.castle = castle
        self.promotion = promotion

    """
    the move as a string
    """
    def short_representation(self):
        string = pos_to_square(self.start_row, self.start_col) + \
                pos_to_square(self.end_row, self.end_col)
        #then if there is a promotion, dictate which promotion it is
        if self.promotion != None:
            string += self.promotion
        return string

    """
    create a duplicate move instance
    """
    def duplicate(self):
        return Move(self.piece, self.start_row, self.start_col, self.end_row, self.end_col,
                self.kill, self.en_passant, self.castle, self.promotion)

    """
    full move information as a string
    """
    def to_string(self):
        ret = "%s at %s " % (self.piece.get_name(), pos_to_square(self.start_row, self.start_col))
        if self.kill == None:
            ret += "moves to "
        else:
            ret += "kills %s at " % self.kill.get_name()
        ret += pos_to_square(self.end_row, self.end_col)
        if self.promotion != None:
            ret += " promoting to %s " % self.promotion
        ret += " (%s)" % self.short_representation()
        return ret
