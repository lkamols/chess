from abc import ABC, abstractmethod
from constants import *
from move import Move

class Piece(ABC):

    """
    Constructor.
    piece should be "p" - pawn, "r" - rook, "n" - knight, 
                    "b" - bishop, "q" - queen or "k" - king
    """
    def __init__(self, colour, piece, index, row, col):
        self._colour = colour
        self._index = index
        self._letter = piece
        self._moved = False
        self._alive = True
        self._row = row
        self._col = col

    def get_colour(self):
        return self._colour

    def get_index(self):
        return self._index

    def get_moved(self):
        return self._moved

    def get_pos(self):
        return self._row, self._col

    def get_row(self):
        return self._row

    def get_col(self):
        return self._col

    def set_alive(self, alive):
        self._alive = alive

    def is_alive(self):
        return self._alive

    def move_to(self, row, col):
        self._row = row
        self._col = col
        self._moved = True

    """
    get the letter used to describe the piece
    """
    def get_letter(self):
        return self._letter

    """
    get the shorthand identifier of the piece
    """
    def get_name(self):
        #white colour pieces are capitalised
        if (self._colour == WHITE):
            return self._letter.capitalize()
        else:
            return self._letter

    """
    gets all moves along a given direction
    dr is the change in row
    dc is the change in col
    """
    def _moves_along_direction(self, board, dr, dc):
        #start from the current position
        row = self._row
        col = self._col
        possibles = []
        while(True):
            row += dr
            col += dc
            #get the colour of the piece at the square
            colour = board.colour_at_square(row, col)
            #check for if we cannot move to this square
            if colour == self._colour or colour == OFF_BOARD:
                break
            elif colour == NO_COLOUR:
                #if there is no piece there, we can move there
                possibles += [Move(self, row, col, kill=NO_KILL)]
            else: #there is a piece of the opposite colour there
                possibles += [Move(self, row, col, kill=board.piece_at_square(row, col))]
                #we also cannot keep moving along this path
                break
        return possibles

    """
    gets all possible diagonal moves (shared by bishop and queen)
    """
    def _diagonal_moves(self, board):
        possibles = []
        for dr, dc in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            possibles += self._moves_along_direction(board, dr, dc)
        return possibles

    """
    gets all possible straight line moves (shared by rook and queen)
    """
    def _straight_moves(self, board):
        possibles = []
        for dr, dc in [(0,1), (0,-1), (-1,0), (1, 0)]:
            possibles += self._moves_along_direction(board, dr, dc)
        return possibles
   
    """
    returns all possible moves for this piece as a pawn
    """
    def _pawn_moves(self, board):
        possibles = []
        #work our the direction of the pawn, white starts at the bottom
        direction = 1 if self._colour == WHITE else -1
        new_row = self._row + direction
        #can we move directly forward?
        if board.colour_at_square(new_row, self._col) == NO_COLOUR:
            possibles += [Move(self, new_row, self._col, kill=NO_KILL)]
            #can we double move forward?
            if self._moved == False and board.colour_at_square(self._row + 2*direction, self._col) == NO_COLOUR:
                possibles += [Move(self, self._row + 2*direction, self._col, kill=NO_KILL)]
        #next check for the ability to capture on the diagonal
        for side in [1,-1]:
            new_col = self._col + side
            if board.colour_at_square(new_row, new_col) == 1 - self._colour: #the other colour
                possibles += [Move(self, new_row, new_col, kill=board.piece_at_square(new_row, new_col))]
        #then check for the fabled en passant
        if ((self._colour == WHITE and self._row == 4) or 
                (self._colour == BLACK and self._row == 3)):
            for side in [-1,1]:
                new_col = self._col + side
                if board.en_passant_col() == new_col:
                    possibles += [Move(self, new_row, new_col, kill=board.piece_at_square(row, new_col), 
                                        en_passant=True)]
        return possibles

    """
    return all possible moves, does not fully check for legality of moves
    """
    def possible_moves(self, board):
        #no switch statments in python... :(
        if self._letter == "p": #pawn
            return self._pawn_moves(board)
        if self._letter == "r": #rook
            return self._straight_moves(board)
        if self._letter == "b": #bishop
            return self._diagonal_moves(board)
        if self._letter == "q": #queen
            return self._straight_moves(board) + self._diagonal_moves(board)
        #not implemented yet
        return []
