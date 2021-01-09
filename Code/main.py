from game import Game
from player import ConsolePlayer, StockfishPlayer
from constants import *

if __name__ == "__main__":
    while(1):
        g = Game(ConsolePlayer(WHITE), ConsolePlayer(BLACK))
        g.play_game()
