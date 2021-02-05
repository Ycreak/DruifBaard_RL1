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

    overlays = []

    overlay1brush = QtGui.QBrush(QtGui.QColor(0,255,0,150))
    overlay1pen = QtGui.QPen(QtGui.QColor(0,255,0), 3)

    overlay1dict = {
        "Brush": overlay1brush,
        "Pen": overlay1pen,
        "Positions": [
            [5,5],
            ],
        }

    overlays.append(overlay1dict)

    # Qt Application
    global app
    app = QtWidgets.QApplication(sys.argv)
    
    global main
    main = QtWidgets.QMainWindow()

    main.setCentralWidget(QHexagonboard(
        # horizontal = True, 
        rows = 20, #6 * 2, 
        columns = 10, # 6 / 2,
        overlays = overlays,
        ))

    main.show()
    sys.exit(app.exec_())

