# Reinforcement Learning
# Leiden University 2021
# Assignment 1
# Philippe Bors S1773585
# Job van der Zwaag S1? :O
# Luuk Nolden S1370898

import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from gameboard import QHexagonboard

if __name__ == '__main__':

    # Qt Application
    global app
    app = QtWidgets.QApplication(sys.argv)
    
    global main
    main = QtWidgets.QMainWindow()

    main.setCentralWidget(QHexagonboard(
        horizontal = True, 
        rows = 5,
        columns = 5,
        ))

    main.show()
    sys.exit(app.exec_())

