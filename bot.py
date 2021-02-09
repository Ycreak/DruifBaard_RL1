import random
import numpy as np

class Bot:
    # def __init__(self):
        # print('bliep bloop')

    def Do_move(self, board, bot_type):
        
        if bot_type == 'random':
            return self.Random_bot(board)
        
    def Random_bot(self, board):

        indeces = np.argwhere(board == 0) 
        row, col = random.choice(indeces)
        # print('bot move', row, col)

        return row, col