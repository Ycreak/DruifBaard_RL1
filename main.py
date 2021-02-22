# Reinforcement Learning
# Leiden University 2021
# Assignment 1
# Philippe Bors S1773585
# Job van der Zwaag S1893378
# Luuk Nolden S1370898

# RUN AS FOLLOWS:
#   $ python3 main.py

import sys
from PyQt5 import QtWidgets, QtGui, QtCore

# from gameboard import QGameboard
from game import Game

class MyBot():
    """Bot Class. Has all info a bot needs. Can be given to the Bot class in bot.py
    """    
    def __init__(self, name, algorithm, search_depth=-1, use_dijkstra=False,
            id_time_limit=0, use_tt=False):
        self.name = name
        self.rating = 25
        self.search_depth = search_depth
        self.use_dijkstra = use_dijkstra
        self.algorithm = algorithm

        self.id_time_limit = id_time_limit
        self.use_tt = use_tt

if __name__ == '__main__':

    board_dimension = 5
    perform_experiments = False

    # Algorithms for the bots
    # self.bot1 = MyBot('ab3D', 'alphabeta', search_depth=3, use_dijkstra=False, use_tt=False, id_time_limit = 1)
    bot1 = MyBot('rnd', 'random')
    bot2 = MyBot('ab3R', 'alphabeta', search_depth=3, use_dijkstra=False, use_tt=False, id_time_limit=0)
    bot3 = MyBot('ab3D', 'alphabeta', search_depth=3, use_dijkstra=True, use_tt=False, id_time_limit=0)
    bot4 = MyBot('ab4D', 'alphabeta', search_depth=4, use_dijkstra=True, use_tt=False, id_time_limit=0)

    game = Game(board_dimension, perform_experiments, bot1, bot2, bot3, bot4)

