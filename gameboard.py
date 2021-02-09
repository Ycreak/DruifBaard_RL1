# Based on https://pypi.org/project/pyqt-gameboard/

# Library Imports
import sys, math
import collections
import random 
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from trueskill import Rating, quality_1vs1, rate_1vs1

# Class Imports
# from bot import Bot
# from evaluate import Evaluate
# from game import Game

class QGameboard(QtWidgets.QGraphicsView):
    """This class handles the entire gameboard and exports it as a QT5 widget.

    Args:
        QtWidgets (QtWidget): Screen stuff handle thingy.
    """    
    def __init__(self):
        QtWidgets.QGraphicsView.__init__(self)

        self.board_dimension = 6

        # Board parameters. Provided by the class caller (main.py).
        self.rows = self.board_dimension
        self.columns = self.board_dimension
        self.size = 4
        # Default parameters
        self.deltaF = 1.0 # Used in WheelEvent
        self.center = None # Used to put hexagons relatively on the screen
        self.shiftfocus = QtCore.QPointF(0, 0) # Same
        # Tuples that map coordinates to tiles
        self.map_coordinates_by_tile = {}
        self.map_tile_by_coordinates = {}
        # Board and widget building
        self.scene = QtWidgets.QGraphicsScene()
        self.Build_board_scene()
        self.setScene(self.scene)
        # Tile data
        self.selected_tile = None
        self.adjacent_tiles = None
        self.target_tile = None
        # For our offset specific! (90 degree angle)
        self.adjacent_offset = [
            [0,-1], # topleft
            [1,-1], # topright
            [1,0],  # right
            [0,1],  # bottomright
            [-1,1],  # bottomleft
            [-1,0], # left     
        ]
        # Data for bots
        self.board = self.Create_numpy_board(self.rows, self.columns)
        # Colours
        self.yellow = [255,255,0]
        self.red = [255,0,0]

    def mousePressEvent(self, event):
        """This functions listens for mouse activity. Calls functions accordingly

        Args:
            event ([type]): mouse event
        """

        # Get position (of pixel clicked)
        position = self.mapToScene(event.pos())
        # Associated tile graphic_item
        new_selected_tile = self.scene.itemAt(position, QtGui.QTransform())
        # Update numpy board
        coordinates = self.Get_tile_grid_location(new_selected_tile)       

        # Play a human move, followed by a bot move. THIS IS FOR TESTING ONLY
        if not self.eval.Check_board_full(self.board):
            if self.Legal_move(self.board, coordinates[0], coordinates[1]):
                print('Legal move.', coordinates)
                self.Paint_tile(new_selected_tile, self.yellow)
                self.board = self.Update_numpy_board(self.board, coordinates[0], coordinates[1]) #TODO: row, col replace with tile
                
                # Check if game over
                if self.eval.Check_winning(self.board, 'player1'):
                    print('THE GAME IS OVER: HUMAN WON')            
                
                elif not self.eval.Check_board_full(self.board):
                    self.board = self.Do_bot_move(self.board, self.bot1, self.red, 'player2', 0)

                    if self.eval.Check_winning(self.board, 'player2'):
                        print('THE GAME IS OVER: BOT WON') 

            else:
                print('ILLEGAL MOVE DETECTED. PLEASE TRY AGAIN.')
        else:
            print('BOARD IS FULL')

    def Create_numpy_board(self, rows, columns):
        """Creates numpy matrix that represents the board

        Args:
            rows (int): [description]
            columns (int): [description]

        Returns:
            board: numpy array
        """        
        board = np.zeros(shape=(rows + 1, columns + 1), dtype=int)
        
        return board

    def Update_numpy_board(self, board, row, col, player='player1'):
        """Updates the numpy board with the given player token on the given location

        Args:
            board (numpy array): [description]
            row (int): 
            col (int): [description]
            player (string, optional): [description]. Defaults to 'player1'.

        Returns:
            board: updated board with move made
        """        
        if player == 'player2':
            code = 2
        else:
            code = 1
        
        board[row,col] = code

        return board

    def Legal_move(self, board, row, col):
        """Checks if the given move is possible

        Args:
            board (np array): [description]
            row (int): [description]
            col (int): [description]

        Returns:
            bool: whether the move is possible
        """        
        if board[row, col] != 0:
            return False
        else: 
            return True

    def Paint_tile(self, tile, colour):
        """Paints the tile provided the colour provided

        Args:
            tile ([type]): [description]
            colour (list): [description]
        """        
        r = colour[0]
        g = colour[1]
        b = colour[2]

        brush = QtGui.QBrush(QtGui.QColor(r,g,b,255))
 
        tile.setBrush(brush)
        tile.update()  

    def wheelEvent(self, event):
        """Allows for zoom in and out

        Args:
            event ([type]): [description]
        """        
        # Get delta of mousewheel scroll, default is 120 pixels, we devide by 1200 to return 0.10 
        # to get the zoom factor
        delta = event.angleDelta()
        self.deltaF = 1 + float(delta.y() / 1200)
        self.scale(self.deltaF, self.deltaF)

    def Build_board_scene(self):
        """       
        Creates a gameboard of rows and columns of hexagons of a sepecific
        size. 

        the default board consists of a number of hexagons that touch at the horizontal tip. 
        The offset hexagons in between them, offset above and below, are in
        a different row. This means that 4 columns already look like a board
        with 8 columns as the offset hexes are not counted for the same row.

        Overlays will be created according to the 'overlays' parameter
        this is a list containing dicts of all overlays, which contains per overlay (dictionary)
        - the fill / brush of the tile type (Brush),
        - the pen / line details of the tile type (Pen) and
        - a list of all the positions of the tile type (Positions)       
        """

        # set focus to center of screen
        self.center = QtCore.QPointF(self.geometry().width() / 2, self.geometry().height() / 2)

        self.Build_tiles()

    def Build_tiles(self):

        #  default white background surrounded by a black 1 width line
        brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        pen = QtGui.QPen(QtGui.QColor(0,0,0), 1, QtCore.Qt.SolidLine)
        
        # Create tiles for all the rows and columns
        row = 0
        while row <= self.rows:

            column = 0
            while column <= self.columns:

                """
                maybe add following to seperate method, so this method can be shape agnostic
                """

                tile = self.Add_shape_to_scene(row, column, pen, brush)
                # Column = X, Row = Y coordinate.
                self.map_coordinates_by_tile[tile] = [row, column] 
                self.map_tile_by_coordinates[f"{row}-{column}"] = tile

                column += 1
                # break
            row += 1
            # break

    def Get_tile_grid_location(self, tile):
        for graphics_item in self.map_coordinates_by_tile:
            if graphics_item == tile:
                coordinates = self.map_coordinates_by_tile[tile]
                return coordinates

    def Add_shape_to_scene(self, row, column, pen, brush):

        """
        Method to easily determine the angle and position of a hexagon tile
        within a gameboard
        """
        scaler = 10

        # tile size
        radius = (self.size / 2) * scaler
        # set the angle of the hexagon
        angle = 90
    
        # space between tiles in columns and rows to make a snug fit
        column_default = self.size * scaler
        column_offset = self.size * (scaler - 1)

        row_default = self.size * scaler
        row_distance = row * row_default 
        row_distance = row * self.size * (scaler - 1)

        # set screen adjustments: get relative position of tile against center of screen
        screen_offset_x = self.center.x() - ((self.columns / 2) * column_default) + self.shiftfocus.x()
        screen_offset_y = self.center.y() - ((self.rows / 2) * row_default) + self.shiftfocus.y()
              
        x = column_offset * column + screen_offset_x + (row-1) * radius
        y = row_distance + screen_offset_y

        hexagon_shape = QHexagonShape(x, y, radius, angle)

        # Create the background tile
        tile = self.scene.addPolygon(hexagon_shape, pen, brush)
        return tile

    def Get_adjacent_tiles(self, target_tile):
        adjacent_tiles = []
        coordinates = self.Get_tile_grid_location(target_tile)
        # adjacent coordinates

        for offset in self.adjacent_offset:
            adjacent_coordinate = [coordinates[0] + offset[0], coordinates[1] + offset[1]]

            try:
                tile = self.map_tile_by_coordinates[f"{adjacent_coordinate[0]}-{adjacent_coordinate[1]}"]
                adjacent_tiles.append(tile)
            except:
                pass
        
        return adjacent_tiles
        
class QHexagonShape(QtGui.QPolygonF):
    """
    polygon with number of sides, a radius, angle of the first point
    hexagon is made with 6 sides
    radius denotes the size of the shape, 
    angle of 
    0 makes a horizontal aligned hexagon (first point points flat), 
    90 makes a vertical aligned hexagon (first point points upwards)

    The hexagon needs the width and height of the current widget or window 
    in order to place itself. 
    the position x and y denote the position relative to the current width and height
    """

    def __init__(self, x, y, radius, angle):
        QtGui.QPolygonF.__init__(self)
        
        self.x = x
        self.y = y
        self.sides = 6
        self.radius = radius
        self.angle = angle

        # angle per step
        w = 360/self.sides

        # add the points of polygon per side
        for i in range(self.sides):
            t = w*i + self.angle

            # horizontal alignment
            x = self.x + self.radius*math.cos(math.radians(t))
            # vertical alignment
            y = self.y + self.radius*math.sin(math.radians(t))

            # add side to polygon
            self.append(QtCore.QPointF(x, y)) 