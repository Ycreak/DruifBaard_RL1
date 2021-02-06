import numpy as np

class Evaluate:

    def __init__(self, board, offset):

        self.adjacent_offset = offset

        self.num_rows = board.shape
        self.num_cols = board.shape

        self.visited_tile_list = []

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

    def Check_winning(self, board):
        return False
        
        to_visit_list = []
        
        # TODO: do we want to specify which player, so we know what sides to check? (saves time)
        
        # TODO: we can perform a check: at least (2 * $dimension) stones need to be played for a line to exist

        # check if line exist top to bottom

        indeces = self.Make_coordinate_list(1, board)

        # if len(indeces) < num_rows:
        #     return False # One cannot win with so few stones
        # else:
        for tile in indeces:
            row, col = tile 
            # print('tile', tile, board[row,col])
            if row == 0:
                # For every tile that is ours, we have a candidate, so lets go digging
                print('candidate:', tile, board[row,col])
                
                # Add this candidate to the list of visited tiles
                self.visited_tile_list.append([row,col])

                # Find its adjacent tiles (that we have not visited yet)
                to_visit_list.extend(self.Find_adjacent_candidate_tiles(board, row, col, 1))    

                # Now, for each candidate, recursively dig down using the candidate and a visited list

        print('to visit: ', to_visit_list)
        print('visited:', self.visited_tile_list)
        
        # Now we have found all adjacent candidate tiles. Recursively search through these
        self.Dig_down(to_visit_list)
        
        # exit(0)

        # Now for every adjacent field, check if it contains a 1
        # for new_tile in to_visit_list:
        #     row, col = new_tile
        #     self.Dig_down(row, col, num_rows, board)




        return True



    def Dig_down(self, to_visit_list):
        new_to_visit_list = []

        for tile in to_visit_list:
            if tile[0] == self.num_rows - 1:
                # We reached the end, winning position
                print('WINNING')
                exit(0)
        
        # No winning position detected, find new candidates and do recursion
        for tile in to_visit_list:
            # Add this newly visited tile to visited list
            self.visited_tile_list.append(tile)
            new_to_visit_list.extend(self.Find_adjacent_candidate_tiles(board, tile[0], tile[1], 1))    

            print('visited', self.visited_tile_list)
            print('to visit list', new_to_visit_list)

            # new_to_visit_list = self.Diff(new_to_visit_list, self.visited_tile_list)

            print('new2', new_to_visit_list)


            # exit(0)
            # Subtract the already visited

    def Check_ended(self, board):
        """Checks first if the board is full. Then if a player has won. If none, returns false.

        Args:
            board ([type]): [description]

        Returns:
            bools: True is game is finished, false otherwise.
        """        
        if np.all(board):
            # Every field filled
            return True

        elif self.Check_winning(board):
            return True

        else:
            return False 
