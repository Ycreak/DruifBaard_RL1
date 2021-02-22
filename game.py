import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

from trueskill import Rating, quality_1vs1, rate_1vs1

from bot import Bot
from evaluate import Evaluate
from gameboard import Gameboard

class Game():

    def __init__(self, board_dimension, perform_experiments, *bots):
        
        self.board_dimension = board_dimension
        self.perform_experiments = perform_experiments
        
        self.bot_list = []

        for bot in bots:
            self.bot_list.append(bot)
        
        # Create a gameboard
        self.gameboard = Gameboard(board_dimension)
        # Save it to a class variable    
        self.board = self.gameboard.board      
        # Initialise the other classes
        self.eval = Evaluate(self.board)
        self.bot = Bot()
        
        if self.perform_experiments:
            self.Perform_experiments(self.board, self.bot_list)
            print('End of experiments, shutting down.')
            exit(1)

        self.Play_single_bot_match(self.bot_list[0], self.bot_list[1], self.board)

    def Play_TrueSkill_match(self, rounds, bot1, bot2):
        """Plays a tourney with the given bots for the given round. Prints results to screen.

        Args:
            rounds (int): number of rounds to be played
            bot1 (string): type for bot 1
            bot2 (string): type for bot 2

        Returns:
            dataframe: of TrueSkill scores            
        """        
        # Stats
        draws = 0
        bot1_wins = 0
        bot2_wins = 0
       
        r_bot1 = Rating(bot1.rating)
        r_bot2 = Rating(bot2.rating)

        outcome = self.Play_single_bot_match(bot1, bot2, self.board) #TODO: should not be self.board ideally
        # print('outcome', outcome)
        if outcome == 0:
            draws += 1
            r_bot1, r_bot2 = rate_1vs1(r_bot1, r_bot2, True) # it is a draw

        elif outcome == 1:
            bot1_wins += 1
            r_bot1, r_bot2 = rate_1vs1(r_bot1, r_bot2)

        elif outcome == 2:
            bot2_wins += 1
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

        # Play the game on a nice empty board.
        board = np.zeros(shape=(self.board_dimension + 1, self.board_dimension + 1), dtype=int)

        while(True):
            # If the board is not yet full, we can do a move
            if not self.eval.Check_board_full(board):
                board = self.Do_bot_move(board, bot1, 'player1')
                # Do move for first player
                if self.eval.Check_winning(board, 'player1'):
                    print('Player 1 has won!')
                    outcome = 1
                    break
            else:
                print('Board is full!')
                outcome = 0
                break

            # If player 1 did not win, check if the board is full
            if not self.eval.Check_board_full(board):
                # Do move for first player
                board = self.Do_bot_move(board, bot2, 'player2')
                if self.eval.Check_winning(board, 'player2'):
                    print('Player 2 has won!')
                    outcome = 2
                    break
            else:
                print('Board is full!')
                outcome = 0
                break

        self.gameboard.Print_gameboard(board)

        return outcome

    def Do_bot_move(self, board, bot, player):
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

        row, col = self.bot.Do_move(board, bot)   
        
        if row < 0 or row > self.board_dimension or col < 0 or col > self.board_dimension:
            raise Exception('Row or col exceeds board boundaries: \n\trow: {0}\n\tcol: {1}\n\tdimension: {2}'.format(row, col, self.board_dimension)) 

        board = self.gameboard.Update_numpy_board(board, row, col, player)
       
        return board

    def Create_plot(self, df, filename):
        """Simple function that creates a line plot of the given dataframe.

        Args:
            df (pd df): dataframe with TrueSkill scores of the bots
            filename (string): filename to be given
        """
        from matplotlib.ticker import MaxNLocator
        # Y Cap.
        trueskill_max = 40

        # Take the names of the columns and plot these
        ax = df.plot.line(title='Round Robin on {0}x{0}'.format(self.board_dimension+1))
        
        ax.set_xlabel("Number of rounds played")
        ax.set_ylabel("TrueSkill score")

        # ax.set_ylim(ymin=0) # TODO: deprecated?
        
        plt.xlim([0, self.tourney_rounds])
        plt.ylim([0, trueskill_max])

        # To make X axis nice integers
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.savefig('plots/{0}.png'.format(filename))
        plt.show()

    def Perform_experiments(self, board, bot_list):
        """This class performs the experiments as required in the Assignment
        """        
        self.tourney_rounds = 1

        # Create Pandas Dataframe
        column_names = [b1.name, b2.name, b3.name, b4.name]
        df = pd.DataFrame(columns = column_names)
        start_position = {b1.name : b1.rating, b2.name : b2.rating, b3.name : b3.rating,
            b4.name : b4.rating}
        df = df.append(start_position, ignore_index=True)

        # TODO: Should be using args*
        for i in range(self.tourney_rounds):
            print("Round", i)
            # Play a round robin between the players
            b1, b2, b3, b4 = self.Play_round_robin(b1, b2, b3, b4)

            # Add scores to dataframe
            new_line = {b1.name : b1.rating.mu, b2.name : b2.rating.mu, b3.name : b3.rating.mu,
                b4.name : b4.rating.mu}
            df = df.append(new_line, ignore_index=True)

        print(df)
        self.Create_plot(df, 'round_robin')

    def Play_round_robin(self, b1, b2, b3, b4):
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
  
        players = [b1, b2, b3, b4]

        tournament = Tournament(players)

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
            print("{} vs {}".format(first_participant_bot.name, second_participant_bot.name))
            
            first_participant_bot, second_participant_bot = self.Play_TrueSkill_match(self.tourney_rounds, first_participant_bot, second_participant_bot)
            # Make sure this match is marked as played
            tournament.add_win(match, first_participant_bot)
            matches = tournament.get_active_matches()

        return b1, b2, b3, b4



