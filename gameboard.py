# Library Imports
import numpy as np

class Gameboard():
    """This class handles the gameboard. It is used by game and initiated via that class. 
    Here functions to print, update and create a stored.
    """    
    def __init__(self, board_dimension):
        # Given in main
        self.board_dimension = board_dimension
        # Board parameters.
        self.rows = self.board_dimension
        self.columns = self.board_dimension
        # Create the board on init
        self.board = self.Create_numpy_board(self.rows, self.columns)

    def Print_gameboard(self, board):
        """Function prints the given board to terminal

        Args:
            board (np array): of the given board
        """        
        
        row_string = ''
        space_string = ''
        top_row = '   '

        for i in range(self.board_dimension + 1):
            top_row = top_row + str(i) + ' '

        print(top_row)

        # Print the board per row
        for i in range(self.board_dimension + 1):
            
            current_row = board[i]
            # Store each element and add a white space in between
            for j in current_row:
                row_string = row_string + ' ' + str(j)
            # Indent each row with a single whitespace to create hex board
            space_string = space_string + ' '
            
            print(i, space_string + row_string)
            row_string = ''

    def Create_numpy_board(self, rows, columns):
        """Creates numpy matrix that represents the board

        Args:
            rows (int): y dimension of board
            columns (int): x dimension of board

        Returns:
            board: numpy array with created board
        """        
        board = np.zeros(shape=(rows + 1, columns + 1), dtype=int)
        
        return board

    def Update_numpy_board(self, board, row, col, player='player1'):
        """Updates the numpy board with the given player token on the given location

        Args:
            board (numpy array): of given board
            row (int): y dimension of board
            col (int): x dimension of board
            player (string, optional): of the current player. Defaults to 'player1'.

        Returns:
            board: updated board with move made
        """        
        if player == 'player2':
            code = 2
        else:
            code = 1
        
        board[row,col] = code

        return board

    def Check_board_full(self, board):
        """Simple function to check whether the board is full

        Args:
            board (np array): of given board

        Returns:
            bool: whether board is filled with all but zeroes
        """        
        if np.all(board):
            # There are no zeroes on the board
            return True
        else:
            return False