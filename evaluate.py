import numpy as np
from itertools import chain

class Evaluate:

    def __init__(self, board, offset):

        self.adjacent_offset = offset

        self.num_rows, self.num_cols = board.shape

        self.found_winning = False

    def Make_coordinate_list(self, value, array):        
        """Creates a list of all coordinates belonging to the given player

        Args:
            value (int): player
            array (np array): [description]

        Returns:
            list: of coordinates belonging to the given player
        """        
        return np.argwhere(array == value)

    def Find_adjacent_candidate_tiles(self, board, row, col, value):
        """Finds all adjacent friendly tiles of the tile given

        Args:
            board (np array): [description]
            row (int): [description]
            col (int): [description]
            value (int): player

        Returns:
            list: of all adjacent candidate tiles
        """        
        tile_list = []
        
        # Find all the neighbours 
        for offset in self.adjacent_offset:
            row2 = row + offset[1]
            col2 = col + offset[0]
            
            # Within the boundaries of the given board
            if row2 >= 0 and row2 < self.num_rows and col2 >= 0 and col2 < self.num_cols:
                
                # Check if the tile belongs to the given player
                if board[row2, col2] == value:
                    tile_list.append([row2,col2])      

        return tile_list

    def Make_candidate_set(self, indeces, board, player_token):
        # Find which one start at the top
        node_list = []
        
        for tile in indeces:
            row, col = tile
        
            if player_token == 1:
                if row == 0:
                    # Add these nodes to our node list
                    print('candidate:', tile, board[row,col])
                    node_list.append([row,col])

            elif player_token == 2:
                if col == 0:
                    # Add these nodes to our node list
                    print('candidate:', tile, board[row,col])
                    node_list.append([row,col])                

        return node_list

    def Check_winning(self, board, player):
        # Lists we need for recursion
        node_list = []
        visited_list = []

        # Player1 moves top to bottom, Player2 moves left to right
        if player == 'player2':
            player_token = 2
        elif player == 'player1':
            player_token = 1

        # Find all our squares
        indeces = self.Make_coordinate_list(player_token, board)

        # Find all candidates according to the player token: player1 top-down, player2 left-right
        node_list = self.Make_candidate_set(indeces, board, player_token)
       
        # Now we have found all adjacent candidate tiles. Recursively search through these
        self.Dig_down(node_list, board, player, visited_list)
        
        if self.found_winning:
            return True
        else:
            return False



    def Dig_down(self, node_list, board, player, visited_list=[]):
        print('-------------')
        print('i got the following list to explore:', node_list)
        print('i already explored:', visited_list)

        adjacent_list = []
        # visited_list = []
        # Exit clause: check if one of the tiles is at the bottom
        for tile in node_list:

            print('data', tile[0], self.num_rows)

            if player == 1 and tile[0] == self.num_rows - 1:
                # We reached the end, winning position
                self.found_winning = True
                # exit(0)
            elif player == 2 and tile[1] == self.num_cols - 1:
                self.found_winning = True

        # Delete from the node_list those nodes we already visited
        node_list_copy = []
        
        for item in node_list:
            if item not in visited_list:
                node_list_copy.append(item)
            
        node_list = node_list_copy

        print('now i need to explore', node_list)

        # Loop through this list and do recursion        
        for tile in node_list:

            print('i am now visiting,',tile)

            adjacent_list = self.Find_adjacent_candidate_tiles(board, tile[0], tile[1], 1)

            print('adjacent is', adjacent_list)
            # Make sure that we have not yet visited these!
            if tile not in visited_list:
                visited_list.append(tile)

            print('i already visited', visited_list)
                       
            # Dig down
            self.Dig_down(adjacent_list, board, visited_list)


    # def Check_ended(self, board, player='player1'): DEPRECATED
    #     """Checks first if the board is full. Then if a player has won. If none, returns false.

    #     Args:
    #         board ([type]): [description]

    #     Returns:
    #         bools: True is game is finished, false otherwise.
    #     """        
    #     if np.all(board):
    #         # Every field filled
    #         return True

    #     elif self.Check_winning(board, player):
    #         return True

    #     else:
    #         return False 

    def Check_board_full(self, board):
        #if np.count_nonzero(board==0) == 0:
        if np.all(board):
            # There are no zeroes on the board
            return True
        else:
            return False

    def Diff(self, li1, li2):
        li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
        return li_dif