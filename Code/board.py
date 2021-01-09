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
        self._moves = [] #track all the moves that have taken place

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
            self._pieces[colour] += [Piece(colour, "r", ROOKQ_ID, base_row, 0)]
            self._pieces[colour] += [Piece(colour, "n", KNIGHTQ_ID, base_row, 1)]
            self._pieces[colour] += [Piece(colour, "b", BISHOPQ_ID, base_row, 2)]
            self._pieces[colour] += [Piece(colour, "q", QUEEN_ID, base_row, 3)]
            self._pieces[colour] += [Piece(colour, "k", KING_ID, base_row, 4)]
            self._pieces[colour] += [Piece(colour, "b", BISHOPQ_ID, base_row, 5)]
            self._pieces[colour] += [Piece(colour, "n", KNIGHTQ_ID, base_row, 6)]
            self._pieces[colour] += [Piece(colour, "r", ROOKQ_ID, base_row, 7)]

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
    returns the most recent move made on the board, this is important
    for en passant
    returns None if there is no last move (i.e we are at the first move)
    """
    def last_move(self):
        if len(self._moves) > 0:
            return self._moves[-1]
        else:
            return None

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
    move the rook with the castle
    """
    def castle_rook_move(self, move):
        #first collect the correct rook to move
        rook = self._pieces[move.piece.get_colour()][move.castle]
        #then determine where to move it to
        if move.castle == ROOKK_ID:
            end_col = 5
        elif move.castle == ROOKQ_ID:
            end_col = 3
        else:
            raise ValueError("move is not a castle")
        #first update the board with that knowledge
        self._board[rook.get_row()][rook.get_col()] = None
        self._board[rook.get_row()][end_col] = rook
        #now update the rook's knowledge of its own position
        rook.move_to(rook.get_row(), end_col)

    """
    undoes the rook move associated with a castle
    """
    def undo_castle_rook_move(self, move):
        #first collect the correct rook to move
        rook = self._pieces[move.piece.get_colour()][move.castle]
        #then determine where to move it to
        if move.castle == ROOKK_ID:
            end_col = 7
        elif move.castle == ROOKQ_ID:
            end_col = 0
        else:
            raise ValueError("move is not a castle")
        #first update the board with that knowledge
        self._board[rook.get_row()][rook.get_col()] = None
        self._board[rook.get_row()][end_col] = rook
        #now update the rook's knowledge of its own position
        rook.move_to(rook.get_row(), end_col, undo=True)

    """
    execute a move, updating the board to reflect the move
    """
    def execute_move(self, move):
        #check for castling and do the rook moves if so
        if move.castle != NO_CASTLE:
            self.castle_rook_move(move)
        #first remove the piece from the board
        self._board[move.start_row][move.start_col] = None
        #then update the piece's own knowledge of its position
        move.piece.move_to(move.end_row, move.end_col)
        #check for a promotion, and if there is a promotion, change the piece
        if move.promotion != None:
            move.piece.set_letter(move.promotion)
        #if it's a kill, remove the killed piece from the game
        if move.kill != None:
            move.kill.set_alive(False)
            self._board[move.kill.get_row()][move.kill.get_col()] = None
        #then update the board's knowledge of the piece
        self._board[move.end_row][move.end_col] = move.piece

        self._moves += [move]

    """
    undoes a move, updating the board to the state it was before the move
    """
    def undo_move(self):
        move = self.last_move()
        #check for castling and undo the rook move if required
        if move.castle != NO_CASTLE:
            self.undo_castle_rook_move(move)
        #first remove the piece from the board at it's current location
        self._board[move.end_row][move.end_col] = None
        #then update the pieces own knowledge of the board
        move.piece.move_to(move.start_row, move.start_col, undo=True)
        #if the piece was promoted, undo the promotion
        if move.promotion != None:
            move.piece.set_letter('p') #return it to being a pawn
        #if a piece was killed by this move, resurrect it
        if move.kill != None:
            move.kill.set_alive(True)
            self._board[move.kill.get_row()][move.kill.get_col()] = move.kill
        #place the piece back where it started
        self._board[move.start_row][move.start_col] = move.piece
        #remove the move from the list of moves
        self._moves.pop() 

    """
    returns all LEGAL moves a player can make, this is different from possible
    moves, in that this does not allow a player to move into check
    """
    def all_legal_moves(self, colour):
        legal_moves = []
        for piece in self._pieces[colour]:
            if piece.is_alive():
                legal_moves += piece.legal_moves(self)
        return legal_moves

    """
    determines if a given move is LEGAL, slightly different from possible,
    in that it determines whether this move ends up in check
    """
    def is_move_legal(self, move):
        #do a couple of preliminary checks for castling
        if move.castle != NO_CASTLE and self.castle_checks(move) == False:
            return False #we cannot perform this castle, even if it ends legally
        #first try executing the move
        self.execute_move(move)
        #then evaluate whether the other player now has check
        legal = True
        if self.is_check(1 - move.piece.get_colour()):
            legal = False
        #then undo the fake move
        self.undo_move()
        return legal

    """
    additional checks for if a castle is legal, checks for:
    - if the king is currently in check
    - if the king would move through check
    """
    def castle_checks(self, move):
        #check that the king isn't currently in check
        if self.is_check(1 - move.piece.get_colour()):
            return False
        #generate a fake move to see if the king moves through check
        #the location of this can be determined by if we are doing a kingside
        #or queenside castle
        if move.castle == ROOKQ_ID:
            move_through = Move(move.piece, move.start_row, move.start_col,
                    move.end_row, move.start_col - 1)
        elif move.castle == ROOKK_ID:
            move_through = Move(move.piece, move.start_row, move.start_col,
                    move.end_row, move.start_col + 1)
        else:
            raise ValueError("should not check castling when the move is not a castle")
        #then check if we move through check
        return self.is_move_legal(move_through)

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
    returns all legal moves that can be made by a colour,
    linked to a dictionary associated with the UCI handle
    """
    def all_legal_moves_dict(self, colour):
        all_moves = self.all_legal_moves(colour)
        #construct a dictionary using the shorthands
        d = {}
        for move in all_moves:
            d[move.short_representation()] = move
        return d

    """
    prints all possible moves that can be made by a colour
    """
    def print_all_possible_moves(self, colour):
        all_moves = self.all_possible_moves(colour)
        for move in all_moves:
            print(move.to_string())

    """
    prints all the legal moves that can be made by a colour
    """
    def print_all_legal_moves(self, colour):
        legal_moves = self.all_legal_moves(colour)
        for move in legal_moves:
            print(move.to_string())

    """
    determines whether the given colour could kill the king in one move
    with the current board
    checking works with possible moves, not legal moves, as check basically
    defines a legal move, and working with legal moves would infinite loop
    """
    def is_check(self, colour):
        all_moves = self.all_possible_moves(colour)
        #check all moves for potential king kills
        for move in all_moves:
            if move.kill != None and move.kill.get_index() == KING_ID:
                return True
        return False


