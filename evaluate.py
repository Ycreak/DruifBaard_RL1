import numpy as np

class Evaluate:
    # def __init__(self):
    #     print('hello')

    def Check_winning(self, board, player='human'):
        # TODO: check if line exist top to bottom
        return False

    def Check_ended(self, board):
        
        if np.all(board):
            # Every field filled
            return True

        else:
            return False 

    # def Evaluate_bot(self, board):
    #     # TODO: check if line exist left to right
    #     return