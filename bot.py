import random
import copy
import numpy as np
from random import randrange

class Bot:
    # def __init__(self):
        # print('bliep bloop')

    def Do_move(self, board, bot_type, search_depth):
        
        if bot_type == 'random':
            return self.Random_bot(board, search_depth)
        elif bot_type == 'alphabeta':
            return self.Alpha_Beta_bot(board, search_depth)
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

    def Alpha_Beta_bot(self, board, search_depth):
        
        copyboard = copy.deepcopy(board)
        value, option = self.minimax(copyboard, search_depth, True)
        print(option)
        print(value)
        return option

    def minimax(self, board, depth, max_player):

        if depth == 0 or np.all(board): #or wining state
            value = self.evaluate(board)
            child = [-1,-1]
            return value, child
        
        if(max_player):
            max_value = float('-inf')
            max_child = [-1,-1]
            options = np.argwhere(board == 0) 
            for option in options:
                copyboard = copy.deepcopy(board)
                copyboard[option] = 1
                value, child = self.minimax(copyboard, depth-1, False)
                if value > max_value:
                    max_value = value
                    max_child = option
            return max_value, max_child

        else: 
            min_value = float('inf')
            min_child = [-1,-1]
            options = np.argwhere(board == 0) 
            for option in options:
                copyboard = copy.deepcopy(board)
                copyboard[option] = 2
                value, child = self.minimax(copyboard, depth-1, True)
                if value < min_value:
                    min_value = value
                    min_child = option
            return min_value, min_child

    def evaluate(self, board):

        return randrange(-10,10)

    def Mcts_bot(self, board):

        return   