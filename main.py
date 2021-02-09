# Reinforcement Learning
# Leiden University 2021
# Assignment 1
# Philippe Bors S1773585
# Job van der Zwaag S1? :O
# Luuk Nolden S1370898

# RUN AS FOLLOWS:
#   $ python3 main.py

import sys
import argparse

from PyQt5 import QtWidgets, QtGui, QtCore

# from gameboard import QGameboard
from game import Game

if __name__ == '__main__':

    # Qt Application
    global app
    app = QtWidgets.QApplication(sys.argv)
    
    global main
    main = QtWidgets.QMainWindow()

    main.setCentralWidget(Game(
        # Parameters
        ))

    main.show()
    sys.exit(app.exec_())