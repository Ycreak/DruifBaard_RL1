from trueskill import Rating, quality_1vs1, rate_1vs1
from bot import Bot
from evaluate import Evaluate

from gameboard import QGameboard

class Game(QGameboard):
    def __init__(self):
        super().__init__() # Inheritance (professionals have standards)



        self.gameboard = QGameboard()

        print(self.gameboard)

        # Game Parameters
        self.board_dimension = 6
        # Whether two bots play or human vs ai
        self.bot_match = True
        # Algorithms for the bots
        self.bot1 = 'random'
        self.bot2 = 'random'
        # Whether we have a tourney
        self.tourney = True
        self.tourney_rounds = 5

        # # Print parameters on screen
        # self.yellow = [255,255,0]
        # self.red = [255,0,0]

        # self.eval = Evaluate(self.board, self.adjacent_offset)
        # self.bot = Bot()

        # We can pitch two bots against eachother.
        if self.bot_match:
            # Now check if we are playing a tourney
            if self.tourney:
                self.Play_bot_tourney(self.tourney_rounds, self.bot1, self.bot2, self.board)
            else: # TODO: just put tourney rounds to 1 to get the same result
                # Play a simple both match for testing
                outcome = self.Play_bot_match(self.bot1, self.bot2, self.board)
                if outcome == 0:
                    print('Draw')
                elif outcome == 1:
                    print('Bot1 won')
                elif outcome == 2:
                    print('Bot2 won')               
        # Else do nothing and just wait for mouse events (handled by mousePressEvent)

    def Play_bot_tourney(self, rounds, bot1, bot2, board):
        # Stats
        draws = 0
        bot1_wins = 0
        bot2_wins = 0

        # Starting TrueSkill rating
        r_bot1 = Rating(25)
        r_bot2 = Rating(25)

        # Lets play a few rounds
        for _ in range(rounds):
            outcome = self.Play_bot_match(self.bot1, self.bot2, self.board)

            if outcome == 0:
                draws += 1
                r_bot1, r_bot2 = rate_1vs1(r_bot1, r_bot2, True) # it is a draw

            elif outcome == 1:
                bot1_wins += 1
                r_bot1, r_bot2 = rate_1vs1(r_bot1, r_bot2)

            elif outcome == 2:
                bot2_wins += 1
                r_bot1, r_bot2 = rate_1vs1(r_bot2, r_bot1)

        print('\nNumber of rounds played:', rounds)
        print('Bot1 wins:', bot1_wins, '\nBot2 wins:', bot2_wins, '\nDraws:', draws)
        print('\nRating bot 1:', r_bot1)
        print('Rating bot 2:', r_bot2)

    def Play_bot_match(self, bot1, bot2, board):
        """Plays a botmatch between the two provided bots. Returns the outcome of the game. 0 means draw,
        1 means bot1 won, 2 means bot 2 won.

        Args:
            bot1 (string): bot type
            bot2 (string): bot type
            board (np array): [description]

        Returns:
            int: describing who won
        """        
        while(True):
            # If the board is not yet full, we can do a move
            if not self.eval.Check_board_full(self.gameboard.board):
                # Do move for first player
                self.board = self.Do_bot_move(self.board, bot1, self.yellow, 'player1')
                if self.eval.Check_winning(self.board, 'player1'):
                    # print('Player 1 has won!')
                    outcome = 1
                    break
            else:
                # print('Board is full!')
                outcome = 0
                break
            # If player 1 did not win, check if the board is full
            if not self.eval.Check_board_full(self.board):
                # Do move for first player
                self.board = self.Do_bot_move(self.board, bot2, self.red, 'player2')
                if self.eval.Check_winning(self.board, 'player2'):
                    # print('Player 2 has won!')
                    outcome = 2
                    break
            else:
                # print('Board is full!')
                outcome = 0
                break

        # print('GAME OVER.')

        return outcome

    def Do_bot_move(self, board, bot_type, colour, player):
        """Handles everything regarding the moving of a bot: calls bot class, adds tile information
        and paints the tile on the screen. Also updates the board and returns it with the new move.

        Args:
            board (np array): [description]
            bot_type (string): describes what bot needs to move
            colour (list): holds colour information in RGB
            player (string): [description]

        Returns:
            board: updated board
        """           

        row, col = self.bot.Do_move(board, bot_type)   
        
        location = f"{row}-{col}"
        selected_tile = self.map_tile_by_coordinates[location]
        # Paint what is done
        self.Paint_tile(selected_tile, colour)
        # Update the numpy matrix
        board = self.Update_numpy_board(board, row, col, player)
        # TODO: less convoluted
        return board