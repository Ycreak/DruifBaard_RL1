# Reinforcement Learning
# Leiden University 2021
# Assignment 1
# Philippe Bors S1773585
# Job van der Zwaag S1893378
# Luuk Nolden S1370898

'''
RUN AS FOLLOWS:
   $ python3 main.py

   To run the experiments, the round-robin-tournament package is required:
   https://pypi.org/project/round-robin-tournament/

''' 

from game import Game

if __name__ == '__main__':
    """
    board_dimension (int): sets the size of the gameboard. As it is represented by an numpy array, a
    5x5 board can be created by board_dimension 4.
    perform_experiments (bool): decides whether the experiments as seen in the paper should be run
    tourney_rounds (int): decides how many round robins need to be played    
    """
    board_dimension = 6
    perform_experiments = True
    tourney_rounds = 4
    # Call the game class, which handles the rest of the game.
    game = Game(board_dimension, perform_experiments, tourney_rounds, human_playing=False)