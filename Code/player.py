from abc import ABC, abstractmethod
from constants import *
import subprocess

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

    

"""
concrete implementation of a player, who chooses moves from the command line
"""
class ConsolePlayer(Player):

    def __init__(self, colour):
        super().__init__(colour)

    def make_move(self, board, legal_moves):
        #get the user to enter their move into the console
        selection = ""
        while selection not in legal_moves:
            selection = input("%s move: " % ("Black" if self._colour == BLACK else "White"))
            if selection == "all":
                print(board.print_all_legal_moves(self._colour))
        return legal_moves[selection]

"""
concrete implementation of a player, which is controlled by a stockfish engine
"""
class StockfishPlayer(Player):

    def __init__(self, colour, rating=20, thinktime=1000):
        super().__init__(colour)
        #start up the stockfish engine
        self._engine = subprocess.Popen(
                'stockfish',
                universal_newlines = True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                bufsize=1,
        )
        self._thinktime = thinktime
        #then do the initial handshake
        #first read the initial line sent by stockfish and discard it
        self._engine.stdout.readline()
        #then check if the process is ready
        self._engine.stdin.write("isready\n")
        response = self._engine.stdout.readline().strip()
        if response != "readyok":
            raise Exception("stockfish is not ready")
        #ensure that stockfish is working in uci
        self._engine.stdin.write("uci\n")
        while response != "uciok":
            response = self._engine.stdout.readline().strip()

        #then set the difficulty
        self._engine.stdin.write("setoption name Skill Level value %d\n" % rating)


    """
    select a move by sending stockfish the current board and then
    letting it choose the best move
    """
    def make_move(self, board, legal_moves):
        #first send the current game board to stockfish
        self._engine.stdin.write("position fen %s\n" % board.fen())
        #then ask the engine to make a decision, using the thinktime
        self._engine.stdin.write("go movetime %d\n" % self._thinktime)

        #then receive the response, there will be some extra stuff, wait for "bestmove" line
        response = [""]
        while response[0] != "bestmove":
            response = self._engine.stdout.readline().strip().split()
        #the chosen move comes after the bestmove text
        chosen = response[1]
        print("%s move: %s" % ("Black" if self._colour == BLACK else "White", chosen))
        return legal_moves[chosen]
