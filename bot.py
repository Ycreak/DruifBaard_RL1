import random
import copy
import numpy as np
from random import randrange

class Bot:
    # def __init__(self):
        # print('bliep bloop')

    def Do_move(self, board, bot_type, search_depth, use_Dijkstra):
        self.board_dimension = board.shape[0] - 1 #TODO: should be in init
        # print(self.board_dimension)
                
        if bot_type == 'random':
            return self.Random_bot(board, search_depth)
        elif bot_type == 'alphabeta':
            return self.Alpha_Beta_bot(board, search_depth, use_Dijkstra)
        elif bot_type == 'mcts':
            return self.Mcts_bot(board)
        else:
            raise Exception('The bot type {0} is not recognised. \nPlease choose random, alphabeta or mcts.'.format(bot_type)) 

    def Random_bot(self, board, search_depth):
        """Simple bot that checks for an empty space on the board. Returns this in row column format.
        Whether the board is full is checked before the bot is called.

        Args:
            board (np array): [description]
            search_depth (int): [description]

        Returns:
            ints: of position to play
        """        
        indeces = np.argwhere(board == 0) 
        row, col = random.choice(indeces)

        return row, col

    def Alpha_Beta_bot(self, board, search_depth, use_Dijkstra):    

        empty_tiles = np.argwhere(board == 0)
        if int((empty_tiles.size/2)) % 2 == 1:
            player = True
        else:
            player = False
        
        copyboard = copy.deepcopy(board)
        alpha = float('-inf')
        beta = float('inf')
        value, option = self.minimax(copyboard, search_depth, alpha, beta, player, use_Dijkstra)

        row, col = option
        return row, col

    def minimax(self, board, depth, alpha, beta, max_player, use_Dijkstra):
        
        if np.all(board):
            child = [-700, -700]
            return 0, child

        winner = self.check_winning(board)
        if winner == 1:
            child = [-800, -800]
            return 10, child

        if winner == 2:
            child = [-900, -900]
            return -10, child

        if depth == 0:
            value = self.evaluate(board, use_Dijkstra)
            child = [-100, -100]
            return value, child
        
        if(max_player):
            max_value = float('-inf')
            max_child = [-200, -200]
            options = np.argwhere(board == 0)
            for option in options:
                copyboard = copy.deepcopy(board)
                row, col = option
                copyboard[row, col] = 1
                value, child = self.minimax(copyboard, depth-1, alpha, beta, False, use_Dijkstra)
                if value > max_value:
                    max_value = value
                    max_child = option
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return max_value, max_child
        
        else: 
            min_value = float('inf')
            min_child = [-300, -300]
            options = np.argwhere(board == 0)
            for option in options:
                copyboard = copy.deepcopy(board)
                row, col = option
                copyboard[row, col] = 2
                value, child = self.minimax(copyboard, depth-1, alpha, beta, True, use_Dijkstra)
                if value < min_value:
                    min_value = value
                    min_child = option
                beta = min(beta, value)
                if beta <= alpha:
                    break
            row, col = min_child
            return min_value, min_child

    def evaluate(self, board, use_Dijkstra):
        if use_Dijkstra:
            player1 = self.dijkstra(board, 1) 
            player2 = self.dijkstra(board, 2)

            return player2 - player1
        else:
            return randrange(-10, 10)

    def dijkstra(self, board, player):

        width = self.board_dimension+1
        #Begin point [-5, -5]
        #End point   [-10, -10]

        shortest_path = {}
        shortest_path[-5, -5] = 0
        taken = []
        visited = []
        unvisited = [[-5, -5]]
        adjacent = {}
        adjacent[-5, -5] = []
        adjacent[-10, -10] = []

        for tile in np.argwhere(board == 0):
            row, col = tile
            shortest_path[row, col] = float('inf')
            unvisited.append([row, col])
            adjacent[row, col] = []
            if(player == 1):
                if(row == 0):
                    adjacent[-5, -5].append([row, col])
                    adjacent[row, col].append([-5, -5])
                if(row == width-1):
                    adjacent[-10, -10].append([row, col])
                    adjacent[row, col].append([-10, -10])
            else:
                if(col == 0):
                    adjacent[-5, -5].append([row, col])
                    adjacent[row, col].append([-5, -5])
                if(col == width-1):
                    adjacent[-10, -10].append([row, col])
                    adjacent[row, col].append([-10, -10])
        
        for tile in np.argwhere(board == player):
            row, col = tile
            shortest_path[row, col] = float('inf')
            unvisited.append([row, col])
            adjacent[row, col] = []
            taken.append([row, col])
            if player == 1:
                if(row == 0):
                    adjacent[-5, -5].append([row, col])
                    adjacent[row, col].append([-5, -5])
                if(row == width-1):
                    adjacent[-10, -10].append([row, col])
                    adjacent[row, col].append([-10, -10])
            else:
                if(col == 0):
                    adjacent[-5, -5].append([row, col])
                    adjacent[row, col].append([-5, -5])
                if(col == width-1):
                    adjacent[-10, -10].append([row, col])
                    adjacent[row, col].append([-10, -10])
        
        shortest_path[-10, -10] = float('inf')
        unvisited.append([-10, -10])

        adjacent = self.get_adjacent_tiles(adjacent, unvisited)

        while unvisited:
            min_value = float('inf')
            min_item = [-400, -400]
            for item in unvisited:
                row, col = item
                value = shortest_path[row, col]
                if value < min_value:
                    min_value = value
                    min_item = item
            
            if min_item == [-400, -400]:
                break

            min_row, min_col = min_item
            path_to_min_item = shortest_path[min_row, min_col]
            adjacent_to_min = adjacent[min_row, min_col]
            for adjacent_item in adjacent_to_min:
                adjacent_row, adjacent_col = adjacent_item
                new_path = path_to_min_item + 1
                if adjacent_item in taken:
                    new_path = new_path - 1
                if new_path < shortest_path[adjacent_row, adjacent_col]:
                    shortest_path[adjacent_row, adjacent_col] = new_path
            
            unvisited.remove(min_item)
            visited.append(min_item)

        return shortest_path[-10, -10]
    
    def get_adjacent_tiles(self, adjacent, list_of_items):

        adjacent_offset = [
            [0, -1], # topleft
            [1, -1], # topright
            [1, 0],  # right
            [0, 1],  # bottomright
            [-1, 1],  # bottomleft
            [-1, 0], # left     
        ]

        for item in adjacent:
            row, col = item
            coordinate = [row, col]

            for offset in adjacent_offset:
                adjacent_coordinate = [coordinate[0] + offset[0], coordinate[1] + offset[1]]
                if adjacent_coordinate in list_of_items:
                    adjacent[item].append(adjacent_coordinate)
        
        return adjacent

    def check_winning(self, board):
        taken1 = []
        taken2 = []
        for tile in np.argwhere(board == 1):
            row, col = tile
            taken1.append([row, col])
        for tile in np.argwhere(board == 2):
            row, col = tile
            taken2.append([row, col])
        
        player1 = self.winning_state(taken1, 1)
        player2 = self.winning_state(taken2, 2)

        if player1:
            return 1
        
        if player2:
            return 2
        
        return 0
    
    def winning_state(self, taken, player_number):
        width = self.board_dimension+1

        adjacent_offset = [
            [0, -1], # topleft
            [1, -1], # topright
            [1, 0],  # right
            [0, 1],  # bottomright
            [-1, 1],  # bottomleft
            [-1, 0], # left     
        ]

        unvisited = []
        visited = []
        contains_begin = False
        contains_end = False

        for item in taken:
            row, col = item
            if player_number == 2:
                if col == 0:
                    unvisited.append(item)
                    contains_begin = True
                if col == width -1:
                    contains_end = True
            else:
                if row == 0:
                    unvisited.append(item)
                    contains_begin = True
                if row == width -1:
                    contains_end = True

        if not contains_begin or not contains_end:
            return False

        while unvisited:
            item = unvisited.pop()
            visited.append(item)
            for offset in adjacent_offset:
                adjacent_coordinate = [item[0] + offset[0], item[1] + offset[1]]
                if adjacent_coordinate not in visited:
                    if adjacent_coordinate in taken:
                        row, col = adjacent_coordinate
                        unvisited.append(adjacent_coordinate)
                        if player_number == 2:
                            if col == width -1:
                                return True
                        else:
                            if row == width -1:
                                return True
        
        return False

    def Mcts_bot(self, board):

        return   