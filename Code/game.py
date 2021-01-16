from chessboard import Board
from constants import *

class Game:


    """
    constructor
    player1 and player2 are both Player objects, defining how moves will be made for each of them
    display determines how to display the board
    """
    def __init__(self, playerW, playerB, display=True):
        self._b = Board()
        self._turn = WHITE
        self._players = [playerW, playerB] #just so we can index to each player
        self._display = display

    """
    play a game of chess with the given players and display mechanism
    """
    def play_game(self):
        #continuous loop until an end condition is reached
        while(True):
            #show the display to the terminal if it is wanted
            if self._display:
                self._b.print_board()

            active_player = self._players[self._turn]

            #check for any game endings
            game_ending = self._b.game_end(self._turn)
            if game_ending == CHECKMATE:
                print("Checkmate! %s wins!" % ("White" if self._turn == BLACK else "Black"))
                return CHECKMATE
            elif game_ending == STALEMATE:
                print("Stalemate!")
                return STALEMATE
            elif game_ending == INSUFFICIENT_MATERIAL:
                print("Draw by insufficient material")
                return INSUFFICIENT_MATERIAL
            elif game_ending == FIFTY_MOVE_RULE:
                print("Draw by fifty move rule")
                return FIFTY_MOVE_RULE
            elif game_ending == REPETITION:
                print("Draw by repetition")
                return REPETITION
            
            #the game is not over, get the player to select a move
            legal_moves = self._b.all_legal_moves_dict(self._turn)
            selected_move = active_player.make_move(self._b, legal_moves)

            #then update the board with the move made
            self._b.execute_move(selected_move)

            #say whether we are in check or not
            if self._b.is_check(self._turn):
                print("Check!")

            #switch player
            self._turn = 1 - self._turn
