# Reinforcement Learning
# Leiden University 2021
# Assignment 1
# Philippe Bors S1773585
# Job van der Zwaag S1? :O
# Luuk Nolden S1370898

import sys
import argparse

from PyQt5 import QtWidgets, QtGui, QtCore

from gameboard import QHexagonboard

if __name__ == '__main__':

    # Parse command line arguments:
    p = argparse.ArgumentParser(description="Provide your parameters")
    # p.add_argument("input", type=argparse.FileType("r"),
    #             help="input file with one verse of poetry per line. Optionally, the verse can be "
    #                     "preceded by a unique index and a tab (set -input_index to True in this case)")
    # p.add_argument("output", type=argparse.FileType("w"),
    #             help="output file name (should end with .json)")
    # p.add_argument("meter", type=str, choices=list(Meter.METERS.keys()),
    #             help="meter to scan the text with")
    # p.add_argument("-manual_file", type=str, default=None,
    #             help="file from which to read manual scansions and to which to write lines that "
    #                     "require manual scansions")
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
        dimension = 6,
        bot_match = bot_match, #FIXME: wont display window when botmatch and dimension > 5
        ))

    main.show()
    sys.exit(app.exec_())

