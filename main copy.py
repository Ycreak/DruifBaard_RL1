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

# from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# from PyQt5.QtWidgets import QApplication,QLineEdit,QWidget,QFormLayout
# from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
# from PyQt5.QtCore import Qt

import sys

from gameboard import QHexagonboard

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Hex")


        layout = QVBoxLayout()
        widgets = [
            QCheckBox,
            # QComboBox,
            # QDateEdit,
            # QDateTimeEdit,
            # QDial,
            # QDoubleSpinBox,
            # QFontComboBox,
            # QLCDNumber,
            # QLabel,
            # QLineEdit,
            # QProgressBar,
            # QPushButton,
            QRadioButton,
            # QSlider,
            # QSpinBox,
            # QTimeEdit
            ]

        for w in widgets:
            layout.addWidget(w())

        layout.addWidget(QHexagonboard(
            dimension = 3,
            bot_match = True,
            ))

    #     widget = QCheckBox()
    #     widget.setCheckState(Qt.Checked)

    #     # For tristate: widget.setCheckState(Qt.PartiallyChecked)
    #     # Or: widget.setTriState(True)
    #     widget.stateChanged.connect(self.show_state)

    #     self.setCentralWidget(widget)


    # def show_state(self, s):
    #     print(s == Qt.Checked)
    #     print(s)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

if __name__ == '__main__':

    # Parse command line arguments:
    p = argparse.ArgumentParser(description="Provide your parameters")
    p.add_argument("dimension", type=int, default=6,
                help="input file with one verse of poetry per line. Optionally, the verse can be "
                        "preceded by a unique index and a tab (set -input_index to True in this case)")
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
    
    app = QApplication(sys.argv)

    window = MainWindow()



    window.show() # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec_()



        # # Qt Application
        # global app
        # app = QtWidgets.QApplication(sys.argv)
        
        # global main
        # main = QtWidgets.QMainWindow()
        # main.setWindowTitle("QLineEdit Example")
        # main.setCentralWidget(QHexagonboard(
        #     dimension = args.dimension,
        #     bot_match = bot_match,
        #     ))

        # main.show()
        # sys.exit(app.exec_())

