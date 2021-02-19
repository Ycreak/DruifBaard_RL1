import random
import copy
import numpy as np
from random import randrange
import time

class Bot:
    # def __init__(self):
        # print('bliep bloop')

    def Do_move(self, board, bot): 

        self.board_dimension = board.shape[0] - 1 #TODO: should be in init
        # print(self.board_dimension)

        if bot.algorithm == 'random':
            return self.Random_bot(board)
        elif bot.algorithm == 'alphabeta':
            return self.Alpha_Beta_bot(board, bot.search_depth, bot.use_dijkstra, bot.use_tt, bot.id_time_limit)
        elif bot.algorithm == 'mcts':
            return self.Mcts_bot(board)
        else:
            raise Exception('The bot type {0} is not recognised. \nPlease choose random, alphabeta or mcts.'.format(bot.algorithm)) 

    def Random_bot(self, board):
        """Simple bot that checks for an empty space on the board. 
            Returns this in row column format.
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

    def Alpha_Beta_bot(self, board, search_depth, use_dijkstra, use_tt, id_time_limit):
        """Bot that returns an empty space on the board chosen by a Minimax algorithm using alpha-beta pruning

        Args:
            board (np array): the current playboard
            search_depth (int): the number of rounds forward the Minimax algorithm should look
            use_dijkstra (bool): True if we use the Dijkstra evaluation method, 
                False if we use the random evaluation method
            use_tt (bool): True if we use transposition tables to Store_result and load previous results from, 
                False if we do not

        Returns:
            ints: of position to play
        """            

        #Get all the empty spaces
        empty_spaces = np.argwhere(board == 0)

        #If the number of empty spaces is odd we are player 1, the maximizing player
        if int((empty_spaces.size/2)) % 2 == 1:
            maximizing_player = True
        else:
            maximizing_player = False
        
        copy_board = copy.deepcopy(board)

        #Init for alpha and beta for the alpha-beta pruning
        alpha = float('-inf')
        beta = float('inf')

        #When the time limit is 0, we dont want to use iterative deepening
        use_id = (id_time_limit != 0)

        if use_id:
            #Computing the end time for the search
            begin_time = time.time()
            end_time = begin_time + id_time_limit
            
            #The initial search depth
            depth_id = 1

            value = -130
            space = [-130, -130]

            self.Initialise_tt()

            #Keep searching till time time is up
            while self.StillGotTime(end_time):
                if use_tt:
                    value, space = self.Minimax_tt(copy_board, depth_id, alpha, beta, maximizing_player, use_dijkstra, -1)
                else:
                    value, space = self.Minimax(copy_board, depth_id, alpha, beta, maximizing_player, use_dijkstra)
                
                #Next loop we use a higer search depth
                depth_id = depth_id + 1
            
        else:
            if use_tt:
                self.Initialise_tt()
                value, space = self.Minimax_tt(copy_board, search_depth, alpha, beta, maximizing_player, use_dijkstra, -1)
            else:
                value, space = self.Minimax(copy_board, search_depth, alpha, beta, maximizing_player, use_dijkstra)
            
        row, col = space
        return row, col    
        
    def Minimax(self, board, depth, alpha, beta, max_player, use_dijkstra):
        """Minimax algorithm. 
            The algorithm returns the value of the current playstate and the best space in this state.

        Args:
            board (np array): the current playboard
            depth (int): the number of rounds forward the min max algorithm should look
            alpha (int): the current minimum value of the maximizing player in the alpha-beta pruning
            beta (int):  the current maximum value of the minimizing player in the alpha-beta pruning
            max_player (bool): True if it is the turn of player 1, the maximizing player in the evaluation, 
                False if it is the turn of player 2.
            use_dijkstra (bool): True if we use the Dijkstra evaluation method.
                False if we use the random evaluation method

        Returns:
            int, [int, int]: The first int returned is the value of the evaluation. 
                The second and third int is the position to play
        """        

        #If the gameboard is full
        if np.all(board):
            space = [-700, -700]
            return 0, space

        # If player 1 has won the game
        winner = self.Check_winning(board)
        if winner == 1:
            space = [-800, -800]
            return 10, space

        # If player 2 has won the game
        if winner == 2:
            space = [-900, -900]
            return -10, space

        # If the algorithm has reached the search depth
        if depth == 0:
            value = self.Evaluate_game_state(board, use_dijkstra)
            space = [-100, -100]
            return value, space
        
        # If it is the turn of the maximizing player
        if max_player:
            max_value = float('-inf')
            max_space = [-200, -200]
            spaces = np.argwhere(board == 0)

            for space in spaces:

                #Make a copy of the game board and take the space in that board
                copy_board = copy.deepcopy(board)
                row, col = space
                copy_board[row, col] = 1

                value, best_space = self.Minimax(copy_board, depth - 1, alpha, beta, False, use_dijkstra)
                
                if value > max_value:
                    max_value = value
                    max_space = space
                
                #Alpha-beta pruning
                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            return max_value, max_space
        
        # If it is the turn of the minimizing player
        else: 
            min_value = float('inf')
            min_space = [-300, -300]
            spaces = np.argwhere(board == 0)

            for space in spaces:

                #Make a copy of the game board and take the space in that board
                copy_board = copy.deepcopy(board)
                row, col = space
                copy_board[row, col] = 2

                value, best_space = self.Minimax(copy_board, depth - 1, alpha, beta, True, use_dijkstra)

                if value < min_value:
                    min_value = value
                    min_space = space

                #Alpha-beta pruning
                beta = min(beta, value)
                if beta <= alpha:
                    break

            return min_value, min_space

    def Minimax_tt(self, board, depth, alpha, beta, max_player, use_dijkstra, hashed_board):
        """Minimax algorithm (transposition tables version). 
            The algorithm returns the value of the current playstate and the best space in this state.

        Args:
            board (np array): the current playboard
            depth (int): the number of rounds forward the min max algorithm should look
            alpha (int): the current minimum value of the maximizing player in the alpha-beta pruning
            beta (int):  the current maximum value of the minimizing player in the alpha-beta pruning
            max_player (bool): True if it is the turn of player 1, the maximizing player in the evaluation, 
                False if it is the turn of player 2.
            use_dijkstra (bool): True if we use the Dijkstra evaluation method.
                False if we use the random evaluation method
            hashed_board (int): A hashed version of the playboard to easily store in the transposition tables
                -1 if the board has not been made yet

        Returns:
            int, [int, int]: The first int returned is the value of the evaluation. 
                The second and third int is the position to play
        """      

        #If the hashed_board has not been made, make the board
        if hashed_board == -1:
            hashed_board = self.Hash_board(board)
        
        #If we've seen this game state before, load the result from the transposition table 
        succes, value, space = self.Load_result(hashed_board, depth)
        if succes:
            return value, space

        #If the gameboard is full
        if np.all(board):
            value = 0
            space = [-700, -700]
            self.Store_result(hashed_board, depth, value, space)
            return value, space

        # If player 1 has won the game
        winner = self.Check_winning(board)
        if winner == 1:
            value = 10
            space = [-800, -800]
            self.Store_result(hashed_board, depth, value, space)
            return value, space

        # If player 2 has won the game
        if winner == 2:
            value = -10
            space = [-900, -900]
            self.Store_result(hashed_board, depth, value, space)
            return value, space

        # If the algorithm has reached the search depth
        if depth == 0:
            value = self.Evaluate_game_state(board, use_dijkstra)
            space = [-100, -100]
            self.Store_result(hashed_board, depth, value, space)
            return value, space
        
        # If it is the turn of the maximizing player
        if max_player:
            max_value = float('-inf')
            max_space = [-200, -200]
            spaces = np.argwhere(board == 0)
            
            for space in spaces:
                #Make a copy of the game board and take the space in that board
                copy_board = copy.deepcopy(board)
                row, col = space
                copy_board[row, col] = 1
                
                hashed_board_copy = hashed_board
                hashed_board_copy ^= self.hash_table[row][col][1]

                value, best_space = self.Minimax_tt(copy_board, depth - 1, alpha, beta, False, use_dijkstra, hashed_board_copy)
                
                if value > max_value:
                    max_value = value
                    max_space = space
                
                #Alpha-beta pruning
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            
            self.Store_result(hashed_board, depth, max_value, max_space)
            return max_value, max_space
        
        # If it is the turn of the minimizing player
        else: 
            min_value = float('inf')
            min_space = [-300, -300]
            spaces = np.argwhere(board == 0)

            for space in spaces:

                #Make a copy of the game board and take the space in that board
                copy_board = copy.deepcopy(board)
                row, col = space
                copy_board[row, col] = 2

                hashed_board_copy = hashed_board
                hashed_board_copy ^= self.hash_table[row][col][2]

                value, best_space = self.Minimax_tt(copy_board, depth - 1, alpha, beta, True, use_dijkstra, hashed_board_copy)

                if value < min_value:
                    min_value = value
                    min_space = space

                #Alpha-beta pruning
                beta = min(beta, value)
                if beta <= alpha:
                    break
            
            self.Store_result(hashed_board, depth, min_value, min_space)
            return min_value, min_space

    def Evaluate_game_state(self, board, use_dijkstra):
        """The evalutation function returns a value for the current state of the game. 
            A higher score is positive for player 1, a lower score is positive for player 2.

        Args:
            board (np array): the current playboard
            use_dijkstra (bool): True if we use the Dijkstra evaluation method.
                False if we use the random evaluation method

        Returns:
            int: the score appointed to this current game state
        """        

        #If we use the Dijkstra evaluation method
        if use_dijkstra:
            score_player1 = self.Dijkstra(board, 1) 
            score_player2 = self.Dijkstra(board, 2)

            #The score equals the cost of the shortest path to winning of player 2 subtracted by
            #   the cost of the shortest path to winning of player 1
            return score_player2 - score_player1
        
        #If we use the random evaluation method
        else:
            #Return a random value between -10 and 10
            return randrange(-10, 10)

    def Dijkstra(self, board, player_number):
        """The Dijkstra function computes the shortest path through the gameboard using only the empty spaces and the spaces
            that are allready taken by this player. Empty spaces all cost 1, while the allready taken spaces cost 0.

        Args:
            board (np array): the current playboard
            player (int): the player for which the function will compute the path and its cost

        Returns:
            int: the cost of the shortest path
        """        

        board_dimension = self.board_dimension + 1

        #[-5, -5] is the begin node, [-10, -10] is the end node
        #The begin node is connected to all spaces on the top row (for player 1) or the first column (for player 2) 
        #The end node is connected to all spaces on the bottom row (for player 1) or the last column (for player 2) 
        #So the algorithm seeks the shortest path from [-5, -5] to [-10, -10]


        #The dictionary of shortest paths. {[x, y]: shortest path from [-5, -5] to [x, y]}
        shortest_path = {}
        shortest_path[-5, -5] = 0

        #The list of taken spaces in the game.
        taken_spaces = []

        #The list of visited spaces in the algorithm
        visited = []

        #The list of unvisited spaces in the algorithm
        unvisited = [[-5, -5]]

        #The dictionary of adjacent spaces. {[x, y]: [[a, b]]} means [x, y] is adjacent to [a, b]
        adjacent_spaces = {}
        adjacent_spaces[-5, -5] = []
        adjacent_spaces[-10, -10] = []

        for space in np.argwhere(board == 0):
            row, col = space
            
            #Add all the empty spaces to the shortest path dictionary. 
            #   We don't know a path to the spaces, so the shortest path is infinity.
            shortest_path[row, col] = float('inf')

            #Add all the empty spaces to the list of unvisited spaces.
            unvisited.append([row, col])

            #Add all the empty spaces to the dictionary of adjacent spaces
            adjacent_spaces[row, col] = []

            if player_number == 1:
                if row == 0:
                    
                    #Atatch [-5, -5] to all the empty spaces on the top row
                    adjacent_spaces[-5, -5].append([row, col])
                    adjacent_spaces[row, col].append([-5, -5])

                if row == board_dimension - 1:

                    #Atatch [-10, -10] to all the empty spaces on the bottom row
                    adjacent_spaces[-10, -10].append([row, col])
                    adjacent_spaces[row, col].append([-10, -10])

            else:
                if col == 0:

                    #Atatch [-5, -5] to all the empty spaces in the first column
                    adjacent_spaces[-5, -5].append([row, col])
                    adjacent_spaces[row, col].append([-5, -5])

                if col == board_dimension - 1:

                    #Atatch [-10, -10] to all the empty spaces in the last column
                    adjacent_spaces[-10, -10].append([row, col])
                    adjacent_spaces[row, col].append([-10, -10])
        
        for space in np.argwhere(board == player_number):
            row, col = space

            #Add all the spaces taken by the player to the shortest path dictionary. 
            #   We don't know a path to the spaces, so the shortest path is infinity.
            shortest_path[row, col] = float('inf')

            #Add all the spaces taken by the player to the list of unvisited spaces.
            unvisited.append([row, col])

            #Add all the spaces taken by the player to the dictionary of adjacent spaces
            adjacent_spaces[row, col] = []

            #Add all the spaces taken by the player to the list of taken spaces in the game
            taken_spaces.append([row, col])

            if player_number == 1:
                if row == 0:

                    #Atatch [-5, -5] to the taken spaces on the top row
                    adjacent_spaces[-5, -5].append([row, col])
                    adjacent_spaces[row, col].append([-5, -5])

                if row == board_dimension - 1:

                    #Atatch [-10, -10] to the taken spaces on the bottom row
                    adjacent_spaces[-10, -10].append([row, col])
                    adjacent_spaces[row, col].append([-10, -10])

            else:
                if col == 0:

                    #Atatch [-5, -5] to the taken spaces in the first column
                    adjacent_spaces[-5, -5].append([row, col])
                    adjacent_spaces[row, col].append([-5, -5])

                if col == board_dimension - 1:

                    #Atatch [-10, -10] to the taken spaces in the last column
                    adjacent_spaces[-10, -10].append([row, col])
                    adjacent_spaces[row, col].append([-10, -10])
        
        #Add [-10, -10] to the shortest path dictionary. 
            #   We don't know a path to the spaces, so the shortest path is infinity.
        shortest_path[-10, -10] = float('inf')

        #Add [-10, -10] to the list of unvisited spaces
        unvisited.append([-10, -10])

        #Fill the dictionary of adjacent spaces
        adjacent_spaces = self.Fill_adjacent_spaces(adjacent_spaces, unvisited)

        while unvisited:

            #Get the space with the shortest path out of the unvisited spaces
            min_value = float('inf')
            min_space = [-400, -400]
            for space in unvisited:
                row, col = space
                value = shortest_path[row, col]
                if value < min_value:
                    min_value = value
                    min_space = space
            
            if min_space == [-400, -400]:
                break
            
            min_row, min_col = min_space
            path_to_min_space = shortest_path[min_row, min_col]
            adjacent_to_min = adjacent_spaces[min_row, min_col]
            
            #Make a new path to all adjacent spaces
            for adjacent_space in adjacent_to_min:
                adjacent_row, adjacent_col = adjacent_space
                
                #Compute the cost of the new path
                new_path = path_to_min_space + 1

                #If the space is allready taken, the spaces costs 0 to add
                if adjacent_space in taken_spaces:
                    new_path = new_path - 1

                #If the new path costs less than the current shortest path, update the shortest path
                if new_path < shortest_path[adjacent_row, adjacent_col]:
                    shortest_path[adjacent_row, adjacent_col] = new_path
            
            #Update the list of unvisisted and visited spaces
            unvisited.remove(min_space)
            visited.append(min_space)

        #When all spaces are visited we can return the cost of the shortest path from [-5, -5] to [-10, -10]
        return shortest_path[-10, -10]
    
    def Fill_adjacent_spaces(self, adjacent_spaces, list_of_spaces):
        """Will return a dictionary of all the adjacent spaces that are taken by the player or still empty

        Args:
            adjacent (dictionary of tuples of ints): the dictionary with all the spaces but without the adjacent information 
            list_of_items (list of tuples of ints): coordinates that are taken by the player or still empty 

        Returns:
            [dictionary of tuples of ints]: dictionary of all the adjacent spaces that are taken by the player or still empty
        """        

        #All the possible connections of a space
        adjacent_offset = [
            [0, -1], # topleft
            [1, -1], # topright
            [1, 0],  # right
            [0, 1],  # bottomright
            [-1, 1], # bottomleft
            [-1, 0], # left     
        ]

        #Go over all the relevant spaces
        for space in adjacent_spaces:
            row, col = space
            coordinate = [row, col]

            #Go over all the possible conncetions
            for offset in adjacent_offset:

                #Create the new coordinate
                adjacent_coordinate = [coordinate[0] + offset[0], coordinate[1] + offset[1]]

                #Check if the new coordinate exists and is relevant
                if adjacent_coordinate in list_of_spaces:

                    #Add the new coordinate to the list of adjacent spaces
                    adjacent_spaces[space].append(adjacent_coordinate)
        
        return adjacent_spaces

    def Initialise_tt(self):
        """Function to initialise the transposition table
        TODO: This function should be run on init of the bot, not every time a move is requested
        """

        board_dimension = self.board_dimension + 1

        self.transposition_table = {}
        self.hash_table = [[[random.randint(1, 2**(board_dimension * board_dimension) - 1) for x in range(3)] for y in range(board_dimension)] for z in range(board_dimension)] 
        return

    def Load_result(self, hashed_board, depth):
        """Check if a game state has been seen before and return it if so

        Args:
            hashed_board (int): hashed version of the game board
            depth (int): the number of rounds forward the algorithm would have looked 

        Returns:
            [bool, int, [int, int]]: The bool: True on a succesfull load, False when the state has not been seen before
                The first int is the value found, the last two ints are the space found
        """        

        if (hashed_board, depth) in self.transposition_table:
            value, row, col = self.transposition_table[hashed_board, depth]
            return True, value, [row, col]

        return False, -690, [-690, -690]

    def Store_result(self, hashed_board, depth, value, space):
        """Store a calculated value and best space for a seen gamestate

        Args:
            hashed_board (int): Hashed version of the gameboard
            depth (int): the number of rounds forward the algorithm would have looked 
            value (int): the calculated value of the game state
            space ([int, int]): the calculated best move of the game state
        """        
      
        row, col = space
        self.transposition_table[(hashed_board, depth)] = [value, row, col]
        return

    def Hash_board(self, board):
        """Hash a gameboard to a int

        Args:
            board (np array): the current playboard

        Returns:
            [int]: Hashed version of the gameboard
        """        

        board_dimension = self.board_dimension + 1

        hashed_board = 0
        for row in range(board_dimension):
            for col in range(board_dimension):

                if board[row][col] != 0:
                    space = board[row][col]

                    #XOR the new space over the hashed_board
                    hashed_board ^= self.hash_table[row][col][space]

        return hashed_board

    def StillGotTime(self, end_time):
        """Check if there is still time left for searching

        Args:
            end_time (float): time for which the algorithm should stop searching

        Returns:
            bool: True if there is still time left,
                False if there is no time left
        """        
        current_time = time.time()

        return current_time < end_time

    def Check_winning(self, board):
        """Returns if one of the players has won the game 

        Args:
            board (np array): the current playboard

        Returns:
            [int]: 0 if the game has not been won, 1 if player 1 has won and 2 if player 2 has won
        """        

        taken_spaces_player1 = []
        taken_spaces_player2 = []

        for space in np.argwhere(board == 1):
            row, col = space
            taken_spaces_player1.append([row, col])

        for space in np.argwhere(board == 2):
            row, col = space
            taken_spaces_player2.append([row, col])
        
        player1_winning = self.Check_winning_for_player(taken_spaces_player1, 1)
        player2_winning = self.Check_winning_for_player(taken_spaces_player2, 2)

        if player1_winning:
            return 1
        
        if player2_winning:
            return 2
        
        return 0
    
    def Check_winning_for_player(self, taken_spaces, player_number):
        """Returns if a player has won the game

        Args:
            taken_spaces (list of tuples of ints): list of the coordinates of taken spaces by the player 
            player_number (int): player number for which we want to check

        Returns:
            bool: True of the current game has been won by the player,
                False if the current game has not bee won by the player
        """    

        board_dimension = self.board_dimension + 1

        #All the possible connections of a space
        adjacent_offset = [
            [0, -1], # topleft
            [1, -1], # topright
            [1, 0],  # right
            [0, 1],  # bottomright
            [-1, 1], # bottomleft
            [-1, 0], # left     
        ]

        #The list of unvisited spaces in the algorithm
        unvisited = []

        #The list of visited spaces in the algorithm
        visited = []

        #To keep track if a winning state is even possible
        contains_begin = False
        contains_end = False

        for space in taken_spaces:
            row, col = space

            if player_number == 2:
                if col == 0:

                    #Add all the taken spaces in the fist column to the list of unvisited items
                    unvisited.append(space)

                    contains_begin = True

                if col == board_dimension - 1:
                    contains_end = True

            else:
                if row == 0:

                    #Add all the taken spaces in the top row to the list of unvisited items
                    unvisited.append(space)

                    contains_begin = True

                if row == board_dimension - 1:
                    contains_end = True

        #If there is no taken space in the first and last row or column a winning state is impossible
        if not contains_begin or not contains_end:
            return False

        while unvisited:

            #Go over all spaces in the unvisited list
            space = unvisited.pop()
            visited.append(space)

            #Go over all adjacent spaces
            for offset in adjacent_offset:
                adjacent_coordinate = [space[0] + offset[0], space[1] + offset[1]]

                #It's no use looking at spaces we allready looked at
                if adjacent_coordinate not in visited:

                    #If the space is also taken, we can add it to the unvisited list
                    if adjacent_coordinate in taken_spaces:
                        row, col = adjacent_coordinate
                        unvisited.append(adjacent_coordinate)

                        #If we have reached the other side of the board, the game is won
                        if player_number == 2:
                            if col == board_dimension - 1:
                                return True
                        else:
                            if row == board_dimension - 1:
                                return True
        
        #If we never reached the other side of the board the game is not won by this player
        return False

    def Mcts_bot(self, board):

        return   