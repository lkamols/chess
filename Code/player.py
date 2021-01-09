from abc import ABC, abstractmethod
from constants import *

"""
abstract class for a player, handles picking moves etc
"""
class Player(ABC):

    def __init__(self, colour):
        self._colour = colour
    
    """
    select a move from the possible moves dictionary and return the choice
    """
    @abstractmethod
    def make_move(self, board, legal_moves):
        pass

    
    @abstractmethod
    def choose_promotion(self):
        pass

"""
concrete implementation of a player, who chooses moves from the command line
"""
class ConsolePlayer(Player):

    def __init__(self, colour):
        super().__init__(colour)

    def make_move(self, board, legal_moves):
        #get the user to 
        selection = ""
        while selection not in legal_moves:
            selection = input("%s move: " % ("Black" if self._colour == BLACK else "White"))
            if selection == "all":
                print(board.print_all_legal_moves(self._colour))
        return legal_moves[selection]

    def choose_promotion(self):
        pass
