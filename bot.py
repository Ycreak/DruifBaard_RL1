import random
import numpy as np

class Bot:
    # def __init__(self):
        # print('bliep bloop')

    def Do_move(self, board, bot_type, search_depth):
        
        if bot_type == 'random':
            return self.Random_bot(board, search_depth)
        elif bot_type == 'dijkstra':
            return self.Dijkstra_bot(board, search_depth)
        elif bot_type == 'mcts':
            return self.Mcts_bot(board)
        else:
            print('whut?')
            exit(1)

    def Random_bot(self, board, search_depth):

        indeces = np.argwhere(board == 0) 
        row, col = random.choice(indeces)
        # print('bot move', row, col)

        return row, col

    def Dijkstra_bot(self, board, search_depth):
        # test
        return

    def Mcts_bot(self, board):

        return   