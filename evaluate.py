import numpy as np
from itertools import chain

class Evaluate:

    def __init__(self, board, offset):

        self.adjacent_offset = offset

        self.num_rows, self.num_cols = board.shape

        self.found_winning = False

        self.debugging = False

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
        """Makes candidate set to start searching. For player1, we search from the top, for player2, 
        we search from the left.

        Args:
            indeces (list): of tiles for given player
            board (np array): [description]
            player_token (int): encoding of given player

        Returns:
            list: of candidate nodes for the respective player
        """        
        node_list = []
        
        for tile in indeces:
            row, col = tile
        
            if player_token == 1:
                if row == 0:
                    # Add these nodes to our node list
                    if self.debugging: 
                        print('candidate:', tile, board[row,col])
                    node_list.append([row,col])

            elif player_token == 2:
                if col == 0:
                    # Add these nodes to our node list
                    if self.debugging: 
                        print('candidate:', tile, board[row,col])
                    node_list.append([row,col])                

        return node_list

    def Check_winning(self, board, player):
        if player == 'player2':
            taken2 = []
            for tile in np.argwhere(board == 2):
                row, col = tile
                taken2.append([row, col])
            return self.winning_state(taken2, 2)
        else:
            taken1 = []
            for tile in np.argwhere(board == 1):
                row, col = tile
                taken1.append([row, col])
            return self.winning_state(taken1, 1)
    
    def winning_state(self, taken, player_number):
        width = self.num_cols

        adjacent_offset = [
            [0, -1], # topleft
            [1, -1], # topright
            [1, 0],  # right
            [0, 1],  # bottomright
            [-1, 1],  # bottomleft
            [-1, 0], # left     
        ]

        unvisited = []
        visited = []
        contains_begin = False
        contains_end = False

        for item in taken:
            row, col = item
            if player_number == 2:
                if col == 0:
                    unvisited.append(item)
                    contains_begin = True
                if col == width -1:
                    contains_end = True
            else:
                if row == 0:
                    unvisited.append(item)
                    contains_begin = True
                if row == width -1:
                    contains_end = True

        if not contains_begin or not contains_end:
            return False

        while unvisited:
            item = unvisited.pop()
            visited.append(item)
            for offset in adjacent_offset:
                adjacent_coordinate = [item[0] + offset[0], item[1] + offset[1]]
                if adjacent_coordinate not in visited:
                    if adjacent_coordinate in taken:
                        row, col = adjacent_coordinate
                        unvisited.append(adjacent_coordinate)
                        if player_number == 2:
                            if col == width -1:
                                return True
                        else:
                            if row == width -1:
                                return True
        
        return False

    # def Check_winning2(self, board, player):

    #     if self.debugging: 
    #         print('Checking win condition for:', player)
        
    #     node_list = []
    #     visited_list = []

    #     # Player1 moves top to bottom, Player2 moves left to right
    #     if player == 'player2':
    #         player_token = 2
    #     elif player == 'player1':
    #         player_token = 1
    #     else:
    #         if self.debugging: 
    #             print('player except:',player)

    #     # Find all our squares
    #     indeces = self.Make_coordinate_list(player_token, board)

    #     # Find all candidates according to the player token: player1 top-down, player2 left-right
    #     node_list = self.Make_candidate_set(indeces, board, player_token)
       
    #     # Now we have found all adjacent candidate tiles. Recursively search through these
    #     self.Dig_down(node_list, board, player_token, visited_list)
        
    #     if self.found_winning:
    #         return True
    #     else:
    #         return False



    # def Dig_down(self, node_list, board, player, visited_list=[]):
    #     # THIS FUNCTION NEEDS TO BE REDONE COMPLETELY.
        
    #     if self.debugging: 
    #         print('-------------')
    #         print('i got the following list to explore:', node_list)
    #         print('i already explored:', visited_list)

    #     adjacent_list = []
    #     # visited_list = []
    #     # Exit clause: check if one of the tiles is at the bottom
    #     for tile in node_list:

    #         if self.debugging: 
    #             print('data', player, tile[0], self.num_rows - 1)

    #         if player == 1 and tile[0] == self.num_rows - 1:
    #             # We reached the end, winning position
    #             self.found_winning = True
    #             # exit(0)
    #         elif player == 2 and tile[1] == self.num_cols - 1:
    #             self.found_winning = True

    #     # Delete from the node_list those nodes we already visited
    #     node_list_copy = []
        
    #     for item in node_list:
    #         if item not in visited_list:
    #             node_list_copy.append(item)
            
    #     node_list = node_list_copy

    #     if self.debugging: 
    #         print('now i need to explore', node_list)

    #     # Loop through this list and do recursion        
    #     for tile in node_list:

    #         if self.debugging: 
    #             print('i am now visiting,',tile)

    #         adjacent_list = self.Find_adjacent_candidate_tiles(board, tile[0], tile[1], player)

    #         if self.debugging: 
    #             print('adjacent is', adjacent_list)
    #         # Make sure that we have not yet visited these!
    #         if tile not in visited_list:
    #             visited_list.append(tile)

    #         if self.debugging: 
    #             print('i already visited', visited_list)
                       
    #         # Dig down
    #         self.Dig_down(adjacent_list, board, player, visited_list)



    def Check_board_full(self, board):
        """Simple function to check whether the board is full

        Args:
            board (np array): [description]

        Returns:
            bool: whether board is filled with all but zeroes
        """        
        if np.all(board):
            # There are no zeroes on the board
            return True
        else:
            return False
