"""
Mini-max Tic-Tac-Toe Player

Board class is here: https://www.coursera.org/learn/principles-of-computing-2/supplement/qMWrV/tttboard-class
test suite here: http://www.codeskulptor.org/#user48_IVQKbrFzXY_52.py
practice nim game here: http://www.codeskulptor.org/#user48_nim_recursive_template_0.py
"""

import poc_ttt_gui
import poc_ttt_provided as provided
#import user48_IVQKbrFzXY_52 as tester

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

#provided.EMPTY is 1
#provided.PLAYERX 2
#provided.PLAYERO 3
#provided.DRAW 4

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    # if game over, return score and invalid move
    game_over = board.check_win()
    if game_over:
        return SCORES[game_over], (-1, -1)
    
    moves = board.get_empty_squares()
    
    score_move_list = []
    
    for move in moves:
        # need to make a copy and not edit original board
        board_copy = board.clone()  
        board_copy.move(move[0], move[1], player)
        
        # switch player and evaluate new board after the move
        new_player = provided.switch_player(player)
#        print board_copy, move, new_player
        copy_score, _ = mm_move(board_copy, new_player)
        
        # if you multiply the score by SCORES[player] then you can always maximize
        # if playerx wins on playerx turn, copy_score 1 * 1
        # if playero wins on playero turn, copy_score -1 * -1
        if copy_score * SCORES[player] == 1:
            return copy_score, move
        
        score_move_list.append((copy_score, move))    
#    print score_move_list
    
    # get the max score and the associated move
    max_score = max(elem[0] * SCORES[player] for elem in score_move_list)
#    print max_score
    for score, move in score_move_list:
        if score * SCORES[player] == max_score:
            return score, move
        
#	codeskulptor doesn't have max key functionality    
#    return max(score_move_list, key = lambda x: x[0] * SCORES[player])

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#tester.run_suite(mm_move)