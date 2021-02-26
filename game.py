# Library imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import datetime
from trueskill import Rating, quality_1vs1, rate_1vs1
# Class imports
from bot import Bot as bot
from gameboard import Gameboard

class Game():
    """This class handles the game: pits bots versus bots and plays tourneys.
    """
    def __init__(self, board_dimension, perform_experiments, tourney_rounds, human_playing):
        # Set global parameters
        self.board_dimension = board_dimension
        self.perform_experiments = perform_experiments
        self.tourney_rounds = tourney_rounds
        # Create our bots
        self.bot1 = bot('rnd', 'random', self.board_dimension)
        self.bot2 = bot('ab3R', 'alphabeta', self.board_dimension, search_depth=3, use_dijkstra=False, use_tt=False, id_time_limit=0)
        self.bot3 = bot('ab3D', 'alphabeta', self.board_dimension, search_depth=3, use_dijkstra=True, use_tt=False, id_time_limit=0)
        self.bot4 = bot('ab4D', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=False, id_time_limit=0)
        self.bot5 = bot('mcts500', 'mcts', self.board_dimension, iterations=500)
        self.bot6 = bot('ab4D_TT', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=0)
        self.bot7 = bot('ab_TT_ID1', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=1)
        self.bot8 = bot('ab_TT_ID2', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=2)
        self.bot9 = bot('ab_TT_ID4', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=4)

        self.botx = bot('mcts500', 'mcts', self.board_dimension, iterations=500)
        self.bot10 = bot('mcts1k', 'mcts', self.board_dimension, iterations=1000)
        self.bot11 = bot('mcts5k', 'mcts', self.board_dimension, iterations=5000)
        self.bot12 = bot('mcts10k', 'mcts', self.board_dimension, iterations=10000)
        self.bot13 = bot('mcts5k_C0.7', 'mcts', self.board_dimension, iterations=5000, c_param=0.7)
        self.bot14 = bot('mcts5k_C1.0', 'mcts', self.board_dimension, iterations=5000, c_param=1)
        self.bot15 = bot('mcts5k_C1.3', 'mcts', self.board_dimension, iterations=5000, c_param=1.3)

        self.bot16 = bot('mctsinf_T1_C0.1', 'mcts', self.board_dimension, iterations=1000000, c_param=0.1, mcts_time_limit=1)
        self.bot17 = bot('mctsinf_T1_C0.5', 'mcts', self.board_dimension, iterations=1000000, c_param=0.5, mcts_time_limit=1)
        self.bot18 = bot('mctsinf_T1_C1.0', 'mcts', self.board_dimension, iterations=1000000, c_param=1, mcts_time_limit=1)
        self.bot19 = bot('mctsinf_T1_C1.5', 'mcts', self.board_dimension, iterations=1000000, c_param=1.5, mcts_time_limit=1)

        # self.bot18 = bot('ab4D_TT_ID2', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=2)
        # self.bot19 = bot('ab4D_TT_ID3', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=3)
        self.botab = bot('ab4D_TT_ID10', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=10)
        self.botmc = bot('mctsinf_T10_C0.5', 'mcts', self.board_dimension, iterations=1000000, c_param=0.5, mcts_time_limit=10)

        self.bot24 = bot('ab4D_TT_ID1', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=1)
        self.bot25 = bot('mctsinf_T1', 'mcts', self.board_dimension, iterations=100000000, c_param=0.1, mcts_time_limit=1)

        self.bot26 = bot('ab4D_TT_ID10', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=10)
        self.bot27 = bot('mctsinf_T10', 'mcts', self.board_dimension, iterations=100000000, c_param=0.1, mcts_time_limit=10)

        # Set experiment lists
        self.ab = [
            self.bot2, self.bot3, self.bot4
        ]
        self.ab_TT = [
            self.bot4, self.bot6
        ]
        self.ab_ID = [
            self.bot7, self.bot8 , self.bot9
        ]
        self.mcts_iter = [
            self.bot5, self.bot10, self.bot11, self.bot12
        ]
        self.mcts_timed = [
            #self.bot20, self.bot21
        ]
        self.mcts_c = [
            self.bot13, self.bot14, self.bot15
        ]
        self.mcts_experiment3 = [
            self.bot16, self.bot17, self.bot18, self.bot19
        ]
        self.test = [self.botx, self.bot10, self.bot11, self.bot12]
        self.bot_list = [
            self.bot1,
            # self.bot2,
            # self.bot3,
            self.bot7,
            # self.bot5,
            # self.bot6,
            # self.bot7,
            self.bot8,
            self.bot14
        ]
        # Create a gameboard
        self.gameboard = Gameboard(board_dimension)
        self.board = self.gameboard.board      
        
        # Allow the human to play against the given bot
        if human_playing:
            res = self.Play_human_match(self.botx, self.board)

        # Choose to perform experiments
        if self.perform_experiments:
            self.Perform_experiments(self.board, self.test)

            print('End of experiments, shutting down.')
            exit(1)

        else:
            # Or just a few matches between two bots
            for _ in range(20):
                res = self.Play_single_bot_match(self.bot1, self.bot2, self.board)
                print("Player " + str(res) + " won")

    def Play_TrueSkill_match(self, board, rounds, bot1, bot2):
        """Plays a tourney with the given bots for the given round. Prints results to screen.

        Args:
            rounds (int): number of rounds to be played
            bot1 (class object): object of bot1
            bot2 (class object): object of bot2

        Returns:
            bot1, bot2 (class objects): bot1 and bot2 objects with updated scores            
        """        
        # Retrieve rating from the bot and put it in TrueSkill object       
        r_bot1 = Rating(bot1.rating)
        r_bot2 = Rating(bot2.rating)
        # Play a single match and record its output
        outcome = self.Play_single_bot_match(bot1, bot2, board)

        if outcome == 0: # it is a draw
            r_bot1, r_bot2 = rate_1vs1(r_bot1, r_bot2, True) 

        elif outcome == 1: # bot1 wins
            r_bot1, r_bot2 = rate_1vs1(r_bot1, r_bot2)

        elif outcome == 2: # bot2 wins
            r_bot2, r_bot1 = rate_1vs1(r_bot2, r_bot1) #TODO: is this good?

        # Update rating
        bot1.rating = r_bot1
        bot2.rating = r_bot2

        return bot1, bot2

    def Play_single_bot_match(self, bot1, bot2, board):
        """Plays a botmatch between the two provided bots. Returns the outcome of the game. 0 means draw,
        1 means bot1 won, 2 means bot 2 won.

        Args:
            bot1 (class object): object of bot1
            bot2 (class object): object of bot2
            board (np array): of the gameboard

        Returns:
            int: describing who won
        """        

        # Empty board before the game
        board = np.zeros(shape=(self.board_dimension + 1, self.board_dimension + 1), dtype=int)

        # Empty lingering transposition tables
        bot1.transposition_table = {}
        bot2.transposition_table = {}

        # Play the game until a game ending condition is met.
        while(True):
            # If the board is not yet full, we can do a move
            if not self.gameboard.Check_board_full(board):
                # This finds a bot move and handles board update
                board, elapsed_time = self.Handle_bot_move(board, bot1, 'player1')
                bot1.elapsed_time += elapsed_time
                if self.bot1.Check_winning(board) == 1:
                    print(bot1.name, 'has won!')
                    outcome = 1
                    break
            else:
                print('Board is full!')
                outcome = 0
                break
            # If player 1 did not win, check if the board is full
            if not self.gameboard.Check_board_full(board):
                # Do move for second player
                board, elapsed_time = self.Handle_bot_move(board, bot2, 'player2')
                bot2.elapsed_time += elapsed_time
                if self.bot1.Check_winning(board) == 2:
                    print(bot2.name, 'has won!')
                    outcome = 2
                    break
            else:
                print('Board is full!')
                outcome = 0
                break

        # Print the gameboard
        self.gameboard.Print_gameboard(board)

        return outcome

    def Play_human_match(self, bot1, board):
        """Plays a match between the provided bot and a human. Returns the outcome of the game. 0 means draw,
        1 means the human won, 2 means bot 2 won.

        Args:
            bot1 (class object): object of bot1
            board (np array): of the gameboard

        Returns:
            int: describing who won
        """        

        # Empty board before the game
        board = np.zeros(shape=(self.board_dimension + 1, self.board_dimension + 1), dtype=int)

        # Play the game until a game ending condition is met.
        while(True):
            # If the board is not yet full, we can do a move
            if not self.gameboard.Check_board_full(board):
                # Print the board for easy visibility
                self.gameboard.Print_gameboard(board)
                # Ask for input
                row = int(input("What Row do you want to play? "))
                col = int(input("What Column do you want to play? "))

                board = self.gameboard.Update_numpy_board(board, row, col, 'player1')

                if self.bot1.Check_winning(board) == 1:
                    print('The human has won!')
                    outcome = 1
                    break
            else:
                print('Board is full!')
                outcome = 0
                break
            # If player 1 did not win, check if the board is full
            if not self.gameboard.Check_board_full(board):
                # Do move for second player
                board, elapsed_time = self.Handle_bot_move(board, bot1, 'player2')
                bot1.elapsed_time += elapsed_time
                if self.bot1.Check_winning(board) == 2:
                    print(bot1.name, 'has won!')
                    outcome = 2
                    break
            else:
                print('Board is full!')
                outcome = 0
                break

        # Print the gameboard
        self.gameboard.Print_gameboard(board)

        return outcome

    def Handle_bot_move(self, board, given_bot, player):
        """Handles everything regarding the moving of a bot: calls bot class to determine move and 
        updates the board and returns it with the new move.

        Args:
            board (np array): of the gameboard
            given_bot (object): bot object, used to determine the move
            player (string): used in board class to colour the field

        Returns:
            board: updated board
            elapsed_time: time needed for the bot to play its move
        """           

        start = time.time()
        # Play the bot move
        row, col = self.bot1.Do_move(board, given_bot)
        end = time.time()

        elapsed_time = round(end - start, 2)
        # Check if the move is legal (also handled in bot class)
        if row < 0 or row > self.board_dimension or col < 0 or col > self.board_dimension:
            raise Exception('Row or col exceeds board boundaries: \n\trow: {0}\n\tcol: {1}\n\tdimension: {2}'.format(row, col, self.board_dimension)) 

        board = self.gameboard.Update_numpy_board(board, row, col, player)
       
        return board, elapsed_time

    def Create_line_plot(self, df, filename):
        """Simple function that creates a line plot of the given dataframe.

        Args:
            df (pd df): dataframe with TrueSkill scores of the bots
            filename (string): filename to be given
        """
        from matplotlib.ticker import MaxNLocator
        # Y Cap.
        trueskill_max = 50

        # Take the names of the columns and plot these
        ax = df.plot.line(title='Round Robin on {0}x{0}'.format(self.board_dimension+1))
        
        ax.set_xlabel("Number of rounds played")
        ax.set_ylabel("TrueSkill score")
        
        plt.xlim([0, self.tourney_rounds])
        plt.ylim([0, trueskill_max])

        # To make X axis nice integers
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        # plt.show()
        plt.savefig('plots/{0}-{1}.png'.format(filename, datetime.datetime.now().strftime("%H:%M:%S")))

    def Create_bar_plot(self, df, filename):
        """Simple function that creates a bar plot of the given dataframe.

        Args:
            df (pd df): dataframe with TrueSkill scores of the bots
            filename (string): filename to be given
        """        
        ax = df.T.plot(title='Round Robin on {0}x{0}'.format(self.board_dimension+1), kind='bar')
        
        ax.set_xlabel("Bots")
        ax.set_ylabel("Number of elapsed seconds")

        plt.draw()
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        
        ax.get_legend().remove()
        
        # plt.show()
        plt.savefig('plots/{0}3.png'.format(filename))


    def Perform_experiments(self, board, bot_list):
        """This class performs the experiments as required in the Assignment
        """        

        column_names = []
        rating_dict = {}
        time_dict = {}

        # Create the pandas dataframe
        for bot in bot_list:
            column_names.append(bot.name)
            rating_dict[bot.name] = bot.rating # Create a dictionary

        df = pd.DataFrame(columns = column_names)
        # Add initial rating
        df = df.append(rating_dict, ignore_index=True)

        for i in range(self.tourney_rounds):
            print("Round", i)
            # Play a round robin between the players
            bot_list = self.Play_round_robin(bot_list, board)
            # Empty dict and add new ratings           
            rating_dict = {}
            for bot in bot_list:
                rating_dict[bot.name] = bot.rating.mu # Create a dictionary            
            # Add scores to dataframe
            df = df.append(rating_dict, ignore_index=True)

        print(df)
        self.Create_line_plot(df, 'round_robin')

        # Now find the elapsed seconds to plot
        for bot in bot_list:
            print('Bot {0} needed {1} seconds.'.format(bot.name, bot.elapsed_time))
            time_dict[bot.name] = bot.elapsed_time # Create a dictionary

        df2 = pd.DataFrame(columns = column_names)
        df2 = df2.append(time_dict, ignore_index=True)

        print(df2)

        # self.Create_bar_plot(df2, 'elapsed_time')

        # Print the number of searched nodes and cutoffs
        for bot in bot_list:
            if bot.searched_nodes > 0:
                print('Bot {0} searched {1} nodes.'.format(bot.name, bot.searched_nodes))
            if bot.cutoffs > 0:
                print('Bot {0} had {1} cutoffs.'.format(bot.name, bot.cutoffs))


    def Play_round_robin(self, bot_list, board):
        """Creates and plays a round robin tourney with the bots given.
        This code is from the pypi library round-robin-tournament
        https://pypi.org/project/round-robin-tournament/

        Args:
            bot_list (list): with bot objects to play the round robin
            board (np array): of the game board

        Returns:
            list: of bots and their updated scores
        """           
        from round_robin_tournament import Tournament
  
        tournament = Tournament(bot_list)

        matches = tournament.get_active_matches()

        # Play a number of round robin tournaments
        while len(matches) > 0:
            # print("{} matches left".format(len(matches)))
            match = matches[0]
            bots = match.get_participants()
            # Get the participants of the current round
            first_participant = bots[0]
            first_participant_bot = first_participant.get_competitor()
            second_participant = bots[1]
            second_participant_bot = second_participant.get_competitor()
            # Print their names
            print('########################################')
            print("{} vs {}".format(first_participant_bot.name, second_participant_bot.name))
            first_participant_bot, second_participant_bot = self.Play_TrueSkill_match(self.tourney_rounds, board, first_participant_bot, second_participant_bot)
            # Make sure this match is marked as played
            tournament.add_win(match, first_participant_bot)
            matches = tournament.get_active_matches()

        return bot_list



