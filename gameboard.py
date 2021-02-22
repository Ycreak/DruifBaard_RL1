# Library Imports
# import sys, math
# import collections
import numpy as np

class Gameboard():
 
    def __init__(self, board_dimension):

        self.board_dimension = board_dimension

        # Board parameters.
        self.rows = self.board_dimension
        self.columns = self.board_dimension

        self.board = self.Create_numpy_board(self.rows, self.columns)

    def Print_gameboard(self, board):

        board_dimension = board.shape[0] - 1

        row_string = ''
        space_string = ''

        for i in range(board_dimension + 1):
            
            current_row = board[i]

            for j in current_row:
                row_string = row_string + ' ' + str(j)

            space_string = space_string + ' '
            

            print(space_string + row_string)
            row_string = ''

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

