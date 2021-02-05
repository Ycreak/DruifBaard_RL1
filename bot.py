import random

class Bot:
    def __init__(self):
        print('bliep bloop')

    def DoMove(self, rows, columns):
        bot_row = random.randint(1,rows)
        bot_column = random.randint(1,columns) 

        location = str(bot_row) + '-' + str(bot_column)

        # TODO: check if move is legal

        return location
