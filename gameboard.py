# Based on https://pypi.org/project/pyqt-gameboard/

# Library Imports
import sys, math
import collections
import random 
from PyQt5 import QtCore, QtGui, QtWidgets

# Class Imports
from bot import Bot as bot

class QGameboard(QtWidgets.QGraphicsView):
    """This class handles the entire gameboard and exports it as a QT5 widget.

    Args:
        QtWidgets (QtWidget): Screen stuff handle thingy.
    """    
    def __init__(self, rows, columns, size = 4, overlays = [], horizontal = True, relative = True):
        QtWidgets.QGraphicsView.__init__(self)
        # Board parameters. Provided by the class caller (main.py).
        self.rows = rows
        self.columns = columns
        self.size = size
        self.overlays = overlays
        self.horizontal = horizontal
        self.relative = relative
        # Default parameters
        self.deltaF = 1.0 # Used in WheelEvent
        self.center = None # Used to put hexagons relatively on the screen
        self.shiftfocus = QtCore.QPointF(0, 0) # Same
        # Tuples that map coordinates to tiles
        self.map_coordinates_by_tile = {}
        self.map_tile_by_coordinates = {}
        # Board and widget building
        self.scene = QtWidgets.QGraphicsScene()
        self.build_board_scene()
        self.setScene(self.scene)
        # Tile data
        self.selected_tile = None
        self.adjacent_tiles = None
        self.target_tile = None

    def DoBotMove(self):
        # TODO: Provide the bot with a snapshot of the current board.
        
        location = bot().DoMove(self.rows, self.columns)      
        
        selected_tile = self.map_tile_by_coordinates[location]

        self.Paint_tile(selected_tile, 'bot')

    def mousePressEvent(self, event):
        """This functions listens for mouse activity. Calls functions accordingly

        Args:
            event ([type]): mouse event
        """        
        # store current selected tile
        current_selected_tile = self.selected_tile

        # get position (of pixel clicked)
        position = self.mapToScene(event.pos())
        # print(f"tile selected at position {position}")

        # associated tile graphic_item
        new_selected_tile = self.scene.itemAt(position, QtGui.QTransform())

        # TODO: If already selected, ask to try again

        self.Selection_new(new_selected_tile)
        self.selection_adjacent_tiles()

        # Now the bot may move
        self.DoBotMove()

    def Selection_new(self, new_selected_tile):
        """[summary]

        Args:
            new_selected_tile ([type]): [description]
        """            
        # Paint the newly selected tile
        self.Paint_tile(new_selected_tile)
        
        # Make new tile the selected tile
        self.selected_tile = new_selected_tile
        
        # Grid Location of the selected tile
        print('Selected tile', self.get_tile_grid_location(self.selected_tile))

        # And its adjecent tiles
        for tile in self.get_adjacent_tiles(self.selected_tile):
          print('Adjecent tile', self.get_tile_grid_location(tile))         

    def selection_adjacent_tiles(self):

        # get adjacent tiles
        adjacent_tiles = self.get_adjacent_tiles(self.selected_tile)

        # paint adjacent tiles
        # adjacent_brush = QtGui.QBrush(QtGui.QColor(0,0,255,255))
        # self.paint_graphic_items(adjacent_tiles, brush = adjacent_brush)

        return adjacent_tiles

    def Paint_tile(self, tile, player='human'):
        if player == 'bot':
            brush = QtGui.QBrush(QtGui.QColor(255,0,0,255))
        else:
            brush = QtGui.QBrush(QtGui.QColor(255,255,0,255))
 
        self.paint_graphic_items([tile], brush = brush)


    def wheelEvent(self, event):

        # get delta of mousewheel scroll, default is 120 pixels, we devide by 1200 to return 0.10 to get the zoom factor
        delta = event.angleDelta()
        self.deltaF = 1 + float(delta.y() / 1200)
        self.scale(self.deltaF, self.deltaF)

    def build_board_scene(self):
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

        self.build_tiles()
        self.build_overlays()

    def build_tiles(self):

        #  default white background surrounded by a black 1 width line
        brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        pen = QtGui.QPen(QtGui.QColor(0,0,0), 1, QtCore.Qt.SolidLine)
        
        # Create tiles for all the rows and columns
        row = 1
        while row <= self.rows:

            column = 1
            while column <= self.columns:

                """
                maybe add following to seperate method, so this method can be shape agnostic
                """

                tile = self.add_shape_to_scene(row, column, pen, brush)

                self.map_coordinates_by_tile[tile] = [row, column]
                self.map_tile_by_coordinates[f"{row}-{column}"] = tile

                column += 1
                # break
            row += 1
            # break

    def build_overlays(self):

        # Create overlays
        for overlay in self.overlays:
            
            # Get brush
            if overlay["Brush"] != "":
                brush = overlay["Brush"]
            else:
                brush = None

            # Get pen
            if overlay["Pen"] != "":
                pen = overlay["Pen"]
            else:
                pen = None

            # create tile list to paint for this overlay
            overlay_tiles = []
            
            for overlay_coordinates in overlay["Positions"]:

                # get position info from the tile list
                overlay_coordinates_string = f"{overlay_coordinates[0]}-{overlay_coordinates[1]}"

                # get the respective tile
                tile = self.map_tile_by_coordinates[overlay_coordinates_string]
                
                # move the tile on top of the background tiles
                tile.setZValue(1)
                
                # add to the overlay tiles
                overlay_tiles.append(tile)

            # paint all the respective tiles
            self.paint_graphic_items(overlay_tiles, pen, brush)

    def get_tile_grid_location(self, tile):
        for graphics_item in self.map_coordinates_by_tile:
            if graphics_item == tile:
                coordinates = self.map_coordinates_by_tile[tile]
                return coordinates

    def paint_graphic_items(self, graphic_items, pen = None, brush = None):

        if graphic_items != None:
            for graphic_item in graphic_items:
                self.paint_graphic_item(graphic_item, pen, brush)

    def paint_graphic_item(self, graphic_item, pen = None, brush = None):
        if pen != None:
            graphic_item.setPen(pen)
        
        if brush != None:
            graphic_item.setBrush(brush)
        
        graphic_item.update()     
       
class QHexagonboard(QGameboard):
    def __init__(self, rows, columns, size = 4, overlays = [], horizontal = True, relative = True):
        super().__init__(rows, columns, size, overlays, horizontal, relative)

    def add_shape_to_scene(self, row, column, pen, brush):

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

    def get_adjacent_tiles(self, target_tile):
        adjacent_tiles = []
        coordinates = self.get_tile_grid_location(target_tile)
        # adjacent coordinates

        # For our offset specific! (90 degree angle)
        adjacent_offset = [
            [-1,0], # topleft
            [-1,1], # topright
            [0,1],  # right
            [1,0],  # bottomright
            [1,-1],  # bottomleft
            [0,-1], # left
        ]

        for offset in adjacent_offset:
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
