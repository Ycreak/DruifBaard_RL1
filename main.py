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

if __name__ == '__main__':

    board_dimension = 3
    perform_experiments = False
    tourney_rounds = 10

    game = Game(board_dimension, perform_experiments, tourney_rounds)

    test_dimensions = [2, 4, 6, 8, 10] 

    # for dimension in test_dimensions:
    #     game = Game(dimension, perform_experiments, tourney_rounds)
