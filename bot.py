import random

class Bot:
    def __init__(self):
        print('bliep bloop')

    def DoMove(self, board):
        x = random.randint(0,5) 
        y = random.randint(0,5)

        # Checks if move is legal
        while board[x, y] != 0:

            y = random.randint(0,5)
            x = random.randint(0,5) 

        print('bot move', x, y)

        return x, y
