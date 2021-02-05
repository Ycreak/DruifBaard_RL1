import random

class Bot:
    def __init__(self):
        print('bliep bloop')

    def Legal_move(self, board, x, y):
        if board[x, y] == 0:
            return True
        else: 
            return False

    def Do_move(self, board):
        
        return self.Random_bot(board)
        


    def Random_bot(self, board):
        x = random.randint(0,5) 
        y = random.randint(0,5)

        # Checks if move is legal
        while not self.Legal_move(board, x, y):
            x = random.randint(0,5) 
            y = random.randint(0,5)

        print('bot move', x, y)

        return x, y