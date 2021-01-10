from game import Game
from player import ConsolePlayer, StockfishPlayer
from constants import *

if __name__ == "__main__":
    while(1):
        g = Game(StockfishPlayer(WHITE, rating=4), StockfishPlayer(BLACK))
        g.play_game()
