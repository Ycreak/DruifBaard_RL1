import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

from trueskill import Rating, quality_1vs1, rate_1vs1

from bot import Bot
from evaluate import Evaluate

from gameboard import QGameboard

class Game(QGameboard):
    def __init__(self):
        super().__init__() # Inheritance (professionals have standards)

        # Initialise the other classes
        self.eval = Evaluate(self.board, self.adjacent_offset)
        self.bot = Bot()

        # Game Parameters
        self.board_dimension = 4
        # Algorithms for the bots
        self.bot1 = MyBot('mcts1', 'mcts', search_depth=3, use_Dijkstra=True)
        self.bot2 = MyBot('rnd', 'random')

        self.tourney_rounds = 5
        self.perform_experiments = False

        if self.perform_experiments:
            self.Perform_experiments()
            print('End of experiments, shutting down.')
            exit(1)

        self.Play_bot_tourney(self.tourney_rounds, self.bot1, self.bot2)


       
    def Play_bot_tourney(self, rounds, bot1, bot2):
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

        print('Initial ratings:\n', bot1.name, r_bot1.mu, '\n', bot2.name, r_bot2.mu)

        # Pandas Dataframe
        # column_names = [bot1.name, bot2.name]

        # df = pd.DataFrame(columns = column_names)
        # start_position = {bot1.name: bot1.rating, bot2.name: bot2.rating}
        # df = df.append(start_position, ignore_index=True)

        # Lets play a few rounds
        for _ in range(rounds):
            outcome = self.Play_single_bot_match(bot1, bot2, self.board) #TODO: should not be self.board ideally
            print('outcome', outcome)
            if outcome == 0:
                draws += 1
                r_bot1, r_bot2 = rate_1vs1(r_bot1, r_bot2, True) # it is a draw

            elif outcome == 1:
                bot1_wins += 1
                r_bot1, r_bot2 = rate_1vs1(r_bot1, r_bot2)

            elif outcome == 2:
                bot2_wins += 1
                r_bot2, r_bot1 = rate_1vs1(r_bot2, r_bot1)

            print('Rating', bot1.name, r_bot1.mu)
            print('Rating', bot2.name, r_bot2.mu)            

            ## Add scores to datafram
            # new_line = {bot1.name: r_bot1.mu, bot2.name: r_bot2.mu}
            # df = df.append(new_line, ignore_index=True)

        print('\nNumber of rounds played:', rounds)
        print(bot1.name, 'wins:', bot1_wins, '\n', bot2.name, 'wins:', bot2_wins, '\nDraws:', draws)
        print('\nRating', bot1.name, r_bot1.mu)
        print('Rating', bot2.name, r_bot2.mu)

        # print(df)

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
                board = self.Do_bot_move(board, bot1, self.yellow, 'player1')
                # Do move for first player
                if self.eval.Check_winning(board, 'player1'):
                    #print('Player 1 has won!')
                    outcome = 1
                    break
            else:
                # print('Board is full!')
                outcome = 0
                break

            # If player 1 did not win, check if the board is full
            if not self.eval.Check_board_full(board):
                # Do move for first player
                board = self.Do_bot_move(board, bot2, self.red, 'player2')
                if self.eval.Check_winning(board, 'player2'):
                    # print('Player 2 has won!')
                    outcome = 2
                    break
            else:
                # print('Board is full!')
                outcome = 0
                break

        return outcome

    def Do_bot_move(self, board, bot, colour, player):
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

        location = f"{row}-{col}"
        selected_tile = self.map_tile_by_coordinates[location]
        # Paint what is done
        self.Paint_tile(selected_tile, colour)
        # Update the numpy matrix
        board = self.Update_numpy_board(board, row, col, player)
        # TODO: less convoluted
        return board

    def Create_plot(self, df, filename):

        from matplotlib.ticker import MaxNLocator

        trueskill_max = 35

        # Take the names of the columns and plot these
        ax = df.plot.line(title='{0} versus {1} on {2}x{3}'.format(df.columns[0], df.columns[1], self.board_dimension, self.board_dimension))
        
        ax.set_xlabel("Number of rounds played")
        ax.set_ylabel("TrueSkill score")

        ax.set_ylim(ymin=0)
        
        plt.xlim([0, self.tourney_rounds])
        plt.ylim([0, trueskill_max])

        # To make X axis nice integers
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.savefig('plots/{0}.png'.format(filename))
        plt.show()

    def Perform_experiments(self):
        
        self.tourney_rounds = 1

        # Determine ELO
        
        b1 = MyBot('rnd', 'random')
        b2 = MyBot('ab3R', 'alphabeta', search_depth=3, use_Dijkstra=False)
        b3 = MyBot('ab3D', 'alphabeta', search_depth=3, use_Dijkstra=True)
        b4 = MyBot('ab4D', 'alphabeta', search_depth=4, use_Dijkstra=True)

        # b1.rating, b4.rating = self.Play_bot_tourney(self.tourney_rounds, b1, b4)
        # b1.rating, b2.rating = self.Play_bot_tourney(self.tourney_rounds, b1, b2)
        # b1.rating, b3.rating = self.Play_bot_tourney(self.tourney_rounds, b1, b3)

        from round_robin_tournament import Tournament

        players = [b1, b2, b3, b4]

        tournament = Tournament(players)

        matches = tournament.get_active_matches()

        print('Start of Round Robin Tournament')
        while len(matches) > 0:
            print("{} matches left".format(len(matches)))
            match = matches[0]
            bots = match.get_participants()
            first_participant = bots[0]
            first_participant_name = first_participant.get_competitor()
            second_participant = bots[1]
            second_participant_name = second_participant.get_competitor()
            print("{} vs {}".format(first_participant_name.name, second_participant_name.name))
            
            first_participant_name, second_participant_name = self.Play_bot_tourney(self.tourney_rounds, first_participant_name, second_participant_name)

            
            
            tournament.add_win(match, first_participant_name)
            matches = tournament.get_active_matches()

        print('Start of Round Robin Tournament')
        while len(matches) > 0:
            print("{} matches left".format(len(matches)))
            match = matches[0]
            bots = match.get_participants()
            first_participant = bots[0]
            first_participant_name = first_participant.get_competitor()
            second_participant = bots[1]
            second_participant_name = second_participant.get_competitor()
            print("{} vs {}".format(first_participant_name.name, second_participant_name.name))
            
            first_participant_name, second_participant_name = self.Play_bot_tourney(self.tourney_rounds, first_participant_name, second_participant_name)

            
            
            tournament.add_win(match, first_participant_name)
            matches = tournament.get_active_matches()

        print('Start of Round Robin Tournament')
        while len(matches) > 0:
            print("{} matches left".format(len(matches)))
            match = matches[0]
            bots = match.get_participants()
            first_participant = bots[0]
            first_participant_name = first_participant.get_competitor()
            second_participant = bots[1]
            second_participant_name = second_participant.get_competitor()
            print("{} vs {}".format(first_participant_name.name, second_participant_name.name))
            
            first_participant_name, second_participant_name = self.Play_bot_tourney(self.tourney_rounds, first_participant_name, second_participant_name)

            
            
            tournament.add_win(match, first_participant_name)
            matches = tournament.get_active_matches()

        # print(tournament.get_winners())


        print(b1.name, b1.rating)
        print(b2.name, b2.rating)
        print(b3.name, b3.rating)
        print(b4.name, b4.rating)

        exit(1)


class MyBot():
  def __init__(self, name, algorithm, search_depth=-1, use_Dijkstra=False, iterations=700):
    self.name = name
    self.rating = 25
    self.search_depth = search_depth
    self.use_Dijkstra = use_Dijkstra
    self.iterations = iterations
    self.algorithm = algorithm

