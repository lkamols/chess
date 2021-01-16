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
        self._moves = 0
        self._alive = True
        self._row = row
        self._col = col

    def get_colour(self):
        return self._colour

    def get_index(self):
        return self._index

    def has_moved(self):
        return self._moves != 0

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

    """
    move the piece to a new (row, col) location
    undo - set true if the move is an undo (for tracking move numbers)
    """
    def move_to(self, row, col, undo=False):
        self._row = row
        self._col = col
        if undo:
            self._moves -= 1
        else:
            self._moves += 1

    """
    get the letter used to describe the piece
    """
    def get_letter(self):
        return self._letter

    """
    change the type of the piece, used for promoting pawns
    """
    def set_letter(self, letter):
        self._letter = letter

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
                possibles += [Move(self, self._row, self._col, row, col, kill=None)]
            else: #there is a piece of the opposite colour there
                possibles += [Move(self, self._row, self._col, row, col, kill=board.piece_at_square(row, col))]
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
    determine if moving a set distance is allowed.
    if so, return a list containing just the move
    else return an empty list
    dr - distance moved in rows
    dc - distance moved in cols
    """
    def _test_move(self, board, dr, dc):
        new_row = self._row + dr
        new_col = self._col + dc
        end_square_colour = board.colour_at_square(new_row, new_col)
        if end_square_colour == self._colour or end_square_colour == OFF_BOARD:
            return []
        elif end_square_colour == NO_PIECE:
            return [Move(self, self._row, self._col, new_row, new_col, kill=None)]
        else:
            return [Move(self, self._row, self._col, new_row, new_col, kill=board.piece_at_square(new_row, new_col))]
   
    """
    determine all the possible moves for the knight
    """
    def _knight_moves(self, board):
        possibles = []
        for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
            possibles += self._test_move(board, dr, dc)
        return possibles

    """
    determine all possible moves for the king
    """
    def _king_moves(self, board):
        possibles = []
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr != 0 or dc != 0:
                    possibles += self._test_move(board, dr, dc)
        #now check for castling, the following criteria must be met for a castle to occur
        #the king and the rook must not have moved
        #there must be no pieces inbetween the rook and the king 
        #(this is 2 spaces kingside, 3 spaces queenside)
        #the king must not be in check, move through check or into check
        #(the check based problems are LEGAL problems and should be handled in legality checks not
        # in with these possible checks)
        for direction in [-1,1]:
            #determine which rook, the king starts on the right so positive is kingside castle
            rookID = ROOKQ_ID if direction == -1 else ROOKK_ID
            #now check all the criteria
            if (not self.has_moved() and not board.get_piece(self._colour, rookID).has_moved() and
                    board.colour_at_square(self._row, self._col + direction) == NO_COLOUR and
                    board.colour_at_square(self._row, self._col + 2*direction) == NO_COLOUR and
                    (direction == 1 or board.colour_at_square(self._row, self._col + 3*direction))):
                #if all the criteria are met, add the castle as a move
                possibles += [Move(self, self._row, self._col, self._row, self._col + 2*direction, castle=rookID)]
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
            possibles += [Move(self, self._row, self._col, new_row, self._col, kill=None)]
            #can we double move forward?
            if not self.has_moved() and board.colour_at_square(self._row + 2*direction, self._col) == NO_COLOUR:
                possibles += [Move(self, self._row, self._col, self._row + 2*direction, self._col, kill=None)]
        #next check for the ability to capture on the diagonal
        for side in [1,-1]:
            new_col = self._col + side
            if board.colour_at_square(new_row, new_col) == 1 - self._colour: #the other colour
                possibles += [Move(self, self._row, self._col, new_row, new_col, kill=board.piece_at_square(new_row, new_col))]
        #then check for the fabled en passant
        if ((self._colour == WHITE and self._row == 4) or 
                (self._colour == BLACK and self._row == 3)):
            for side in [-1,1]:
                attacked_col = self._col + side
                previous_move = board.last_move() #this should not be null as we know our pawn has moved
                #check for if a pawn has moved just ready for the en passant
                if previous_move.piece.get_letter() == "p" and previous_move.end_row == self._row and \
                        previous_move.end_col == attacked_col and \
                        abs(previous_move.start_row - previous_move.end_row) == 2:
                    possibles += [Move(self, self._row, self._col, 
                            self._row + direction, attacked_col, kill=previous_move.piece)]
        #ALSO NEED TO HANDLE PROMOTIONS HERE, NEED TO ADD MULTIPLE MOVES IN HERE
        #next handle the possibility of promotion
        if len(possibles) != 0 and possibles[0].end_row in [0,7]:
            promotions = []
            for move in possibles:
                for option in ["r", "n", "q", "b"]: #any promotion can be to 4 different pieces
                    new_move = move.duplicate()
                    new_move.promotion = option
                    promotions += [new_move]
            return promotions
        else: #there was no promotions, don't need to flesh it out, just accept it
            return possibles

    """
    return all possible moves, does not fully check for legality of moves
    """
    def possible_moves(self, board):
        #no switch statments in python... :(
        if self._letter == "p": #pawn
            return self._pawn_moves(board)
        elif self._letter == "r": #rook
            return self._straight_moves(board)
        elif self._letter == "b": #bishop
            return self._diagonal_moves(board)
        elif self._letter == "q": #queen
            return self._straight_moves(board) + self._diagonal_moves(board)
        elif self._letter == "n": #knight
            return self._knight_moves(board)
        elif self._letter == "k": #king
            return self._king_moves(board)
        else:
            raise ValueError("piece not one of defined pieces")


    """
    returns all LEGAL moves, checks for legality of all possible moves
    """
    def legal_moves(self, board):
        possibles = self.possible_moves(board)
        legals = []
        for move in possibles:
            if board.is_move_legal(move):
                legals += [move]
        return legals

