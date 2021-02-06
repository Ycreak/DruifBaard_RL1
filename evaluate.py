import numpy as np

class Evaluate:
    # def __init__(self):
    #     print('hello')
    def __init__(self):

        self.adjacent_offset = [
            [0,-1], # topleft
            [1,-1], # topright
            [1,0],  # right
            [0,1],  # bottomright
            [-1,1],  # bottomleft
            [-1,0], # left
        ]

        # self.num_rows, self.num_cols = board.shape



        self.visited_tile_list = []

    def Make_coordinate_list(self, value, array):        
        return np.argwhere(array == value)

    def Find_adjacent_candidate_tiles(self, board, row, col, value):
        tile_list = []
        
        num_rows, num_cols = board.shape #FIXME: should be handled in init

        for offset in self.adjacent_offset:
            row2 = row + offset[1]
            col2 = col + offset[0]

            if row2 >= 0 and row2 < num_rows and col2 >= 0 and col2 < num_cols:
                # print('adjacent:', row2,col2, board[row2, col2])
                # Check if it is our tile and whether we visited it already
                if board[row2, col2] == value:
                    if [row2, col2] not in self.visited_tile_list:
                        print('hoi', [row2, col2], self.visited_tile_list)
                        # if new tile, append it to the list of what we need to search
                        tile_list.append([row2,col2])      

        return tile_list  

    def Check_winning(self, board, player='human'):
        to_visit_list = []
        
        # TODO: do we want to specify which player, so we know what sides to check? (saves time)
        
        # TODO: we can perform a check: at least (2 * $dimension) stones need to be played for a line to exist
        num_rows, num_cols = board.shape

        # check if line exist top to bottom

        indeces = self.Make_coordinate_list(1, board)

        # if len(indeces) < num_rows:
        #     return False # One cannot win with so few stones
        # else:
        for tile in indeces:
            row, col = tile 
            print('tile', tile, board[row,col])
            if row == 0:
                # For every tile that is ours, we have a candidate, so lets go digging
                print('candidate:', tile, board[row,col])
                
                # Add this candidate to the list of visited tiles
                self.visited_tile_list.append([row,col])

                # Find its adjacent tiles (that we have not visited yet)
                to_visit_list.extend(self.Find_adjacent_candidate_tiles(board, row, col, 1))    

        print('to visit: ', to_visit_list)
        print('visited:', self.visited_tile_list)
        
        
        # exit(0)

        # Now for every adjacent field, check if it contains a 1
        # for new_tile in to_visit_list:
        #     row, col = new_tile
        #     self.Dig_down(row, col, num_rows, board)




        return True

    def Dig_down(self, row, col, num_rows, board):
        if row != num_rows - 1:

            to_visit_list = self.Find_adjacent_candidate_tiles(board, row, col, 1)

            for new_tile in to_visit_list:
                row, col = new_tile
                self.Dig_down(row, col, num_rows, board)

        else:
            print('we have a line! w00t')


    def Check_ended(self, board):
        
        if np.all(board):
            # Every field filled
            return True

        else:
            return False 

    # def Evaluate_bot(self, board):
    #     # TODO: check if line exist left to right
    #     return