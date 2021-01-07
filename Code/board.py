from piece import *
from constants import *
from move import Move

"""
decides the row based on the colour, inverts black
used for starting positions
"""
def row_conv(colour, row):
    if colour == BLACK:
        return NUM_ROWS - 1 - row
    else:
        return row


class Board:

    def __init__(self):
        #create an array of arrays for the pieces with no pieces
        self._board = []
        for row in range(NUM_ROWS):
            self._board += [[None] * NUM_COLS]
        #then load in all the pieces
        self._load_pieces()
        self._load_board()
        self._en_passant_col = NO_PASSANT #tracker for if there is a double moved pawn just previously


    """
    populate the board with the starting pieces
    """
    def _load_pieces(self):
        #create an array for the pieces to be all stored in
        #each piece will maintain its own index for fast look up
        self._pieces = [[],[]]
        for colour in range(NUM_COLOURS): #takes both WHITE and BLACK
            #first do the pawns
            pawn_row = row_conv(colour, 1)
            for col in range(NUM_COLS):
                self._pieces[colour] += [Piece(colour, "p", col, pawn_row, col)]
            #then add the other pieces
            base_row = row_conv(colour, 0)
            self._pieces[colour] += [Piece(colour, "r",  8, base_row, 0)]
            self._pieces[colour] += [Piece(colour, "n",  9, base_row, 1)]
            self._pieces[colour] += [Piece(colour, "b", 10, base_row, 2)]
            self._pieces[colour] += [Piece(colour, "q", 11, base_row, 3)]
            self._pieces[colour] += [Piece(colour, "k", 12, base_row, 4)]
            self._pieces[colour] += [Piece(colour, "b", 13, base_row, 5)]
            self._pieces[colour] += [Piece(colour, "n", 14, base_row, 6)]
            self._pieces[colour] += [Piece(colour, "r", 15, base_row, 7)]

    """
    given all the pieces, position them on the board
    """
    def _load_board(self):
        for colour in range(NUM_COLOURS):
            for i in range(NUM_PIECES):
                piece = self._pieces[colour][i]
                self._board[piece.get_row()][piece.get_col()] = piece

    """
    print out the board
    """
    def print_board(self):
        #flip the rows because the bottom left is really row zero
        for row in range(NUM_ROWS - 1, -1, -1):
            for col in range(NUM_COLS):
                if self._board[row][col] == None:
                    print("-", end="")
                else:
                    print(self._board[row][col].get_name(), end="")
            #then print a new line for each row
            print("")

    """
    prints out all the pieces and their own knowledge of their position,
    for debugging purposes only
    """
    def print_pieces(self):
        for colour in range(NUM_COLOURS):
            for i in range(NUM_PIECES):
                piece = self._pieces[colour][i]
                if piece == None:
                    print("colour:%d index:%d Dead" % (colour, i))
                else:
                    print("colour:%d index:%d piece:%s row:%d col:%d" %
                            (colour, i, piece.get_name(), piece.get_row(), piece.get_col()))


    """
    return the colour of the square located at the given position
    or NO_COLOUR if there is no piece at the square
    or OFF_BOARD if the given row column pair are not on the board
    """
    def colour_at_square(self, row, col):
        if row < 0 or row >= NUM_ROWS or col < 0 or col >= NUM_COLS:
            return OFF_BOARD
        if self._board[row][col] == None:
            return NO_COLOUR
        else:
            return self._board[row][col].get_colour()

    """
    return the index of the piece at the square at the given position
    this does not contain any colour information, which can be obtained
    with colour_at_square.
    returns NO_PIECE if there is no piece at the square
    """
    def piece_at_square(self, row, col):
        if row < 0 or row >= NUM_ROWS or col < 0 or col >= NUM_COLS:
            return OFF_BOARD
        if self._board[row][col] == None:
            return NO_PIECE
        else:
            return self._board[row][col]


    """
    return the piece of the given colour and index
    """
    def get_piece(self, colour, index):
        return self._pieces[colour][index]

    """
    if the most recent move was a pawn double step, returns the column
    else return NO_PASSANT
    """
    def en_passant_col(self):
        return self._en_passant_col

    """
    execute a move, updating the board to reflect the move
    """
    def execute_move(self, move):
        #first remove the piece from the board
        self._board[move.piece.get_row()][move.piece.get_col()] = None
        #then update the piece's own knowledge of its position
        move.piece.move_to(move.end_row, move.end_col)
        #if it's a kill, remove the killed piece from the game
        if (move.kill):
            killed_piece = self._board[move.end_row][move.end_col]
            killed_piece.set_alive(False)
            #remove the killed piece from the known pieces, never to return
            self._pieces[killed_piece.get_colour()][killed_piece.get_index()] = None
        #then update the board's knowledge of the piece
        self._board[move.end_row][move.end_col] = move.piece

        #handle the en passant memory
        if move.piece.get_letter() == "p" and abs(move.piece.get_row() - move.end_col) == 2:
            self._en_passant_col = move.piece.index
        else:
            self._en_passant_col = NO_PASSANT

    """
    returns all possible moves that can be made by a colour
    """
    def all_possible_moves(self, colour):
        all_moves = []
        for piece in self._pieces[colour]:
            if piece.is_alive():
                all_moves += piece.possible_moves(self)
        return all_moves

    """
    prints all possible moves that can be made by a colour
    """
    def print_all_possible_moves(self, colour):
        all_moves = self.all_possible_moves(colour)
        for move in all_moves:
            print(move.to_string())


if __name__ == "__main__":
    b = Board()
    b.print_board()
    b.print_pieces()
    b.print_all_possible_moves(WHITE)
    """
    p = b._pieces[0][2]
    moves = p.possible_moves(b)
    b.execute_move(moves[0])
    b.print_board()
    b.print_pieces()
    """


