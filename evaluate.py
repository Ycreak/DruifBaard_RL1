import numpy as np

class Evaluate:
    # def __init__(self):
    #     print('hello')
    def __init__(self):

        self.adjacent_offset = [
            [-1,0], # topleft
            [-1,1], # topright
            [0,1],  # right
            [1,0],  # bottomright
            [1,-1],  # bottomleft
            [0,-1], # left
        ]

    def Check_winning(self, board, player='human'):
        # TODO: do we want to specify which player, so we know what sides to check? (saves time)
        
        # TODO: we can perform a check: at least (2 * $dimension) stones need to be played for a line to exist
        num_rows, num_cols = board.shape

        # print(board)
        # check if line exist top to bottom
        indeces = np.argwhere(board == 1)
        print(board)
        print('ind', indeces) 
        # print('board', board[board == 1])

        # Find all tiles that have a 1.
        result = np.where(board == 1)
        listOfCoordinates= list(zip(result[0], result[1]))
        # for cord in listOfCoordinates:
        #     print('cord:', cord)

        if len(indeces) < num_rows:
            return False # One cannot win with so few stones
        else:
            for tile in listOfCoordinates:
                x, y = tile 
                print('tile', tile, board[x,y])
                if y == 0:
                    # candidate, lets go digging
                    # print('candidate', tile)
                    # x2, y2 = tile
                    print('candidate:', tile, board[x,y])
            
                    for offset in self.adjacent_offset:
                        x2 = x + offset[1]
                        y2 = y + offset[0]

                        if x2 >= 0 and x2 < num_cols and y2 >= 0 and y2 < num_rows:
                            print('adjacent:', x2,y2, board[x2, y2])
                            # adjacent_tiles.append(tile)
            
            return True




        
        # return adjacent_tiles

        # Check if line exist left to right            
        
        
        # return False

    def Check_ended(self, board):
        
        if np.all(board):
            # Every field filled
            return True

        else:
            return False 

    # def Evaluate_bot(self, board):
    #     # TODO: check if line exist left to right
    #     return