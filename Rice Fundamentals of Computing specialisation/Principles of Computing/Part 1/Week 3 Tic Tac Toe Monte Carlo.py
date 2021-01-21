"""
Monte Carlo Tic-Tac-Toe Player
http://www.codeskulptor.org/#user47_5yAvPqgqIt_9.py
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 3         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    play a game starting with the given player by making random moves, 
    alternating between players. 
    does not return anything; should modify the board input
    """
    while not board.check_win():
        # pick one random empty square among the list of tuples
        empty_square = random.choice(board.get_empty_squares())
        board.move(empty_square[0], empty_square[1], player)
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player):
    """
    takes a grid of scores (a list of lists) of board dimensions, 
    a board from a completed game, and which player the machine player is. 
    
    score the completed board and update the scores grid. 
    does not return anything,
    """
    state = board.check_win()
    board_dim = board.get_dim()
#    print("before", scores)
    if state == 4:  # Draw
        pass
    
    elif state == player:  # current player is winner
        for row in range(board_dim):
            for col in range(board_dim):
                if board.square(row, col) == 1:
                    scores[row][col] += 0
                elif board.square(row, col) == player:
                    scores[row][col] += SCORE_CURRENT  # current squares that win the game are good
                elif board.square(row, col) != player:
                    scores[row][col] -= SCORE_OTHER  # opponent squares are bad
    
    elif state != player:  # current player is loser
        for row in range(board_dim):
            for col in range(board_dim):
                if board.square(row, col) == 1:
                    scores[row][col] += 0
                elif board.square(row, col) == player:  
                    scores[row][col] -= SCORE_CURRENT  # current squares that lost the game are bad
                elif board.square(row, col) != player:
                    scores[row][col] += SCORE_OTHER
    
#    print(board)
#    print("after", scores)
    
def get_best_move(board, scores):
    """
    find all of the empty squares with the maximum score 
    and randomly return one of them as a (row, col) tuple
    """
    # associate a tuple:score dict entry for each empty square
    empty_squares = board.get_empty_squares()
    empty_scores = {}
    for square in empty_squares:
        empty_scores[square] = scores[square[0]][square[1]]
    
    max_score = max(empty_scores.values())
    moves = [square for square, score in empty_scores.items() if score == max_score]
    
    if moves:
        return random.choice(moves)
    else:
        print("Error: No more moves")

def mc_move(board, player, trials):
    """
    use the Monte Carlo simulation to return a move for the machine player 
    in the form of a (row, col) tuple
    """
    mc_dim = board.get_dim()
    mc_scores = [[0 for _col in range(mc_dim)] for _row in range(mc_dim)]

    for _trial in range(trials):
        mc_sim = board.clone()  # board has to be recreated each trial
        mc_trial(mc_sim, player)
#        print("board")
#        print(mc_sim)
        mc_update_scores(mc_scores, mc_sim, player)
        
    return get_best_move(board, mc_scores)
    

# check the value of ttb constants
#print("ttb constants")
#print(provided.EMPTY)
#print(provided.PLAYERX)
#print(provided.PLAYERO)
#print(provided.DRAW)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
