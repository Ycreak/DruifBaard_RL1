# Reinforcement Learning
# Leiden University 2021
# Assignment 1
# Philippe Bors S1773585
# Job van der Zwaag S1? :O
# Luuk Nolden S1370898

# RUN AS FOLLOWS:
#   $ python3 main.py <dimension> <--bot_match true>

import sys
import argparse

from PyQt5 import QtWidgets, QtGui, QtCore

from gameboard import QHexagonboard

if __name__ == '__main__':

    # Parse command line arguments:
    p = argparse.ArgumentParser(description="Provide your parameters")
    # Dimension of the board. Mandatory!
    p.add_argument("dimension", type=int, default=6,
                help="lorem ipsum")
    # Whether we play bot match or not
    p.add_argument("--bot_match", type=bool, default=False, dest="bot_match",
                help="if provided, a bot match will be started")

    args = p.parse_args(sys.argv[1:])

    # Do stuff accordingly
    if args.bot_match:
        bot_match = True
    else:
        bot_match = False
    
    # Qt Application
    global app
    app = QtWidgets.QApplication(sys.argv)
    
    global main
    main = QtWidgets.QMainWindow()

    main.setCentralWidget(QHexagonboard(
        dimension = args.dimension,
        bot_match = args.bot_match,
        ))

    main.show()
    sys.exit(app.exec_())