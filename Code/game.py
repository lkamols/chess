from board import Board
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
            legal_moves = self._b.all_legal_moves_dict(self._turn)

            #check for if there are no possible moves and the game is over
            if len(legal_moves) == 0:
                #must decide if this is checkmate or stalemate
                if self._b.is_check(1 - self._turn):
                    print("Checkmate, %s wins!" % ("white" if self._turn == BLACK else "black"))
                    return self._turn
                else:
                    print("Stalemate!")
                    return STALEMATE

            #get the player to select a move
            selected_move = active_player.make_move(self._b, legal_moves)
            #need to do some processing here for promotions and castles

            #then update the board with the move made
            self._b.execute_move(selected_move)


            #switch player
            self._turn = 1 - self._turn
