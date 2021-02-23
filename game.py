import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import time

from trueskill import Rating, quality_1vs1, rate_1vs1

from bot import Bot as bot
# from bot import Check_winning
from gameboard import Gameboard

class Game():

    def __init__(self, board_dimension, perform_experiments, tourney_rounds):
        
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
        self.bot7 = bot('ab4D_TT_ID0.5', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=0.5)
        self.bot8 = bot('ab4D_TT_ID2', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=1)
        self.bot9 = bot('ab4D_TT_ID4', 'alphabeta', self.board_dimension, search_depth=4, use_dijkstra=True, use_tt=True, id_time_limit=4)
        self.bot10 = bot('mcts1k', 'mcts', self.board_dimension, iterations=1000)
        self.bot11 = bot('mcts5k', 'mcts', self.board_dimension, iterations=5000)
        self.bot12 = bot('mcts10k', 'mcts', self.board_dimension, iterations=10000)

        # Set experiment lists
        self.alphabeta_experiment = [
            self.bot2, self.bot3, self.bot4
        ]

        self.alphabeta_plus_experiment = [
            self.bot4, self.bot6, self.bot7, self.bot8, self.bot9
        ]

        self.alphabeta_plus_search_depth_experiment = [
            self.bot1
        ]

        self.mcts_experiment = [
            self.bot5, self.bot10, self.bot11, self.bot12
        ]

        self.bot_list = [
            # self.bot1,
            # self.bot2,
            # self.bot3,
            self.bot4,
            # self.bot5,
            self.bot6,
            self.bot7,
            self.bot8,
            self.bot9
            ]

        # Create a gameboard
        self.gameboard = Gameboard(board_dimension)
        self.board = self.gameboard.board      
        
        # Choose to perform experiments
        if self.perform_experiments:
            self.Perform_experiments(self.board, self.mcts_experiment)
            print('End of experiments, shutting down.')
            exit(1)

        # Or just a few matches between two bots
        for _ in range(20):
            res = self.Play_single_bot_match(self.bot_list[2], self.bot_list[4], self.board)
            print("Player " + str(res) + " won")

    def Play_TrueSkill_match(self, board, rounds, bot1, bot2):
        """Plays a tourney with the given bots for the given round. Prints results to screen.

        Args:
            rounds (int): number of rounds to be played
            bot1 (string): type for bot 1
            bot2 (string): type for bot 2

        Returns:
            dataframe: of TrueSkill scores            
        """        
        # Stats
       
        r_bot1 = Rating(bot1.rating)
        r_bot2 = Rating(bot2.rating)

        outcome = self.Play_single_bot_match(bot1, bot2, board) #TODO: should not be self.board ideally
        # print('outcome', outcome)
        if outcome == 0:
            r_bot1, r_bot2 = rate_1vs1(r_bot1, r_bot2, True) # it is a draw

        elif outcome == 1:
            r_bot1, r_bot2 = rate_1vs1(r_bot1, r_bot2)

        elif outcome == 2:
            r_bot2, r_bot1 = rate_1vs1(r_bot2, r_bot1) #TODO: is this good?

        bot1.rating = r_bot1
        bot2.rating = r_bot2

        return bot1, bot2

    def Play_single_bot_match(self, bot1, bot2, board):
        """Plays a botmatch between the two provided bots. Returns the outcome of the game. 0 means draw,
        1 means bot1 won, 2 means bot 2 won.

        Args:
            bot1 (string): bot type
            bot2 (string): bot type
            board (np array): [description]

        Returns:
            int: describing who won
        """        

        # Play the game on a nice empty board. TODO: this is now deprecated.
        board = np.zeros(shape=(self.board_dimension + 1, self.board_dimension + 1), dtype=int)

        while(True):
            # If the board is not yet full, we can do a move
            if not self.gameboard.Check_board_full(board):
                board, elapsed_time = self.Handle_bot_move(board, bot1, 'player1')
                bot1.elapsed_time += elapsed_time
                # Do move for first player               
                if self.bot1.Check_winning(board) == 1: #FIXME: this is bad
                    print(bot1.name, 'has won!')
                    outcome = 1
                    break
            else:
                print('Board is full!')
                outcome = 0
                break


            # If player 1 did not win, check if the board is full
            if not self.gameboard.Check_board_full(board):
                # Do move for first player
                board, elapsed_time = self.Handle_bot_move(board, bot2, 'player2')
                bot2.elapsed_time += elapsed_time

                if self.bot1.Check_winning(board) == 2: #FIXME: this is bad
                    print(bot2.name, 'has won!')
                    outcome = 2
                    break
            else:
                print('Board is full!')
                outcome = 0
                break

        self.gameboard.Print_gameboard(board)

        # print('time for bots:', round(bot1.elapsed_time,2), round(bot2.elapsed_time,2))

        return outcome

    def Handle_bot_move(self, board, given_bot, player):
        """Handles everything regarding the moving of a bot: calls bot class, adds tile information
        and paints the tile on the screen. Also updates the board and returns it with the new move.

        Args:
            board (np array): [description]
            bot (string): describes what bot needs to move
            colour (list): holds colour information in RGB
            player (string): [description]

        Returns:
            board: updated board

        TODO: Revise this class.
        """           

        start = time.time()
        row, col = self.bot1.Do_move(board, given_bot) #FIXME: this is bad   
        end = time.time()

        elapsed_time = round(end - start, 2)


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

        # ax.set_ylim(ymin=0) # TODO: deprecated?
        
        plt.xlim([0, self.tourney_rounds])
        plt.ylim([0, trueskill_max])

        # To make X axis nice integers
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.show()
        plt.savefig('plots/{0}.png'.format(filename))

    def Create_bar_plot(self, df, filename):
        ax = df.T.plot(title='Round Robin on {0}x{0}'.format(self.board_dimension+1), kind='bar')
        
        ax.set_xlabel("Bots")
        ax.set_ylabel("Number of elapsed seconds")

        plt.draw()
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        
        ax.get_legend().remove()
        
        plt.show()
        plt.savefig('plots/{0}.png'.format(filename))



    def Perform_experiments(self, board, bot_list):
        """This class performs the experiments as required in the Assignment
        """        

        column_names = []
        rating_dict = {}
        time_dict = {}

        for bot in bot_list:
            column_names.append(bot.name)
            rating_dict[bot.name] = bot.rating # Create a dictionary

        df = pd.DataFrame(columns = column_names)
        # Add initial rating
        df = df.append(rating_dict, ignore_index=True)

        # TODO: Should be using args*
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

        for bot in bot_list:
            print('Bot {0} needed {1} seconds.'.format(bot.name, bot.elapsed_time))
            time_dict[bot.name] = bot.elapsed_time # Create a dictionary

        df2 = pd.DataFrame(columns = column_names)

        df2 = df2.append(time_dict, ignore_index=True)

        print(df2)

        self.Create_bar_plot(df2, 'elapsed_time')


    def Play_round_robin(self, bot_list, board):
        """Creates and plays a round robin tournament with the bots given

        Args:
            b1 ([type]): [description]
            b2 ([type]): [description]
            b3 ([type]): [description]
            b4 ([type]): [description]

        Returns:
            bots: classes and their updated ELO scores
        """        
        from round_robin_tournament import Tournament
  
        # players = [b1, b2, b3, b4]

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



