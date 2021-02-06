import random
import numpy as np

class Bot:
    def __init__(self):
        print('bliep bloop')

    def Check_board_full(self, board):
        if np.count_nonzero(board==0) == 0:
            # There are no zeroes on the board
            return True
        else:
            return False

    def Do_move(self, board, bot_type):
        if bot_type == 'random':
            return self.Random_bot(board)

    def Random_bot(self, board):
        
        if self.Check_board_full(board):
            col = -1
            row = -1

        else: 
            # Find available spots and pick one     
            indeces = np.argwhere(board == 0) 
            row, col = random.choice(indeces)
            print('bot move', row, col)

        return row, col