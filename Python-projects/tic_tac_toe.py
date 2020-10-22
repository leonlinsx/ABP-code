# jetbrains academy project
# plays tic tac toe with human or AI
# AI has 3 levels, easy, medium, hard
import random
import sys

class TicTacToe:
    
    # initialise board dictionary; _ represents blank
    # note the coordinates are different from instructions; easier for me to understand
    theBoard = {1: '_' , 2: '_' , 3: '_' ,
                4: '_' , 5: '_' , 6: '_' ,
                7: '_' , 8: '_' , 9: '_' }
    
    # have a dictionary converting the instruction coordinates to my board dictionary
    # changed the x y representation from original problem
    coord_to_idx = {(1, 1): 1, (1, 2): 2, (1, 3): 3,
                    (2, 1): 4, (2, 2): 5, (2, 3): 6,
                    (3, 1): 7, (3, 2): 8, (3, 3): 9}
    
    def __init__(self):
        pass
    
    def main(self):
        
        print("Instructions:")
        print("Input command takes three arguments: start, player1, player2")
        print("player1 and player2 can be 'user', 'easy', 'medium', or 'hard' ")
        print("Input command exit to exit")
        print("Coordinates are x y, with 1 1 on top left and 3 3 bottom right\n")

        playing, player1, player2 = self.menu()
        
        while playing:
            # loop through user/com moves, checking state after each move
            # raises a flag to return to menu and check if still playing
            if player1 == "user":
                self.move_user(TicTacToe.theBoard)
            elif player1 == "easy":
                self.move_com_easy(TicTacToe.theBoard)
            elif player1 == "medium":
                self.move_com_med(TicTacToe.theBoard)
            elif player1 == "hard":
                self.move_com_hard(TicTacToe.theBoard)
            state, flag = self.board_state(TicTacToe.theBoard)
            if flag:
                print(state, '\n')
                TicTacToe.theBoard.update({1: '_' , 2: '_' , 3: '_' ,
                                            4: '_' , 5: '_' , 6: '_' ,
                                            7: '_' , 8: '_' , 9: '_' }) 
                playing, player1, player2 = self.menu()
                continue    
            
            if player2 == "user":
                self.move_user(TicTacToe.theBoard)
            elif player2 == "easy":
                self.move_com_easy(TicTacToe.theBoard)
            elif player2 == "medium":
                self.move_com_med(TicTacToe.theBoard)
            elif player2 == "hard":
                self.move_com_hard(TicTacToe.theBoard)
            state, flag = self.board_state(TicTacToe.theBoard)
            if flag:
                print(state, '\n')
                TicTacToe.theBoard.update({1: '_' , 2: '_' , 3: '_' ,
                                            4: '_' , 5: '_' , 6: '_' ,
                                            7: '_' , 8: '_' , 9: '_' }) 
                playing, player1, player2 = self.menu()
                continue
                     
        sys.exit()   
        
        # # v2.0 if want to have game w/ only use and computer
        # self.board_print(TicTacToe.theBoard)
        # # loop while game unfinished
        # while True:
        #     self.move_user(TicTacToe.theBoard)
        #     state, flag = self.board_state(TicTacToe.theBoard)
        #     if flag:
        #         print(state)
        #         break
        #    
        #     self.move_com_easy(TicTacToe.theBoard)
        #     state, flag = self.board_state(TicTacToe.theBoard)
        #     if flag:
        #         print(state)
        #         break

        # # v1.0 if want to initialise board from different state
        # # update theBoard global with the values from enter_cells, which returns a dictionary
        # temp_dict = self.enter_cells_custom("Enter cells:")
        # TicTacToe.theBoard.update(temp_dict)

    def menu(self):
        # uses a loop to take commands until only valid commands entered
        # returns boolean flag of game running/not, the player choice for first player and second player
        # players can be any combo of human or AI e.g. all human, all AI
        while True:
            cmd_list = input("Input command: ").lower().split()
            if len(cmd_list) == 1:
                if cmd_list[0] == "exit":
                    playing, player1, player2 = False, None, None
                    break
                else:
                    print("Bad parameters!")
                    continue
            elif len(cmd_list) != 3 and cmd_list[0] != "start":
                print("Bad parameters!")
                continue
            elif cmd_list[1] not in ["user", "easy", "medium", "hard"]:
                print("Bad parameters!")
                continue
            elif cmd_list[2] not in ["user", "easy", "medium", "hard"]:
                print("Bad parameters!")
                continue
            else:
                playing, player1, player2 = True, cmd_list[1], cmd_list[2]
                break
        return playing, player1, player2                
        
    def enter_cells_custom(self, line):
        # if want to initialise board from different state
        # get key value pairs of i, char in input(line); create and return a dictionary from that
        # dictionary is one-indexed so have to adjust
        return dict([(i + 1, char) for i, char in enumerate(input(line))])
    
    def enter_coord(self, line, board):
        # takes a coordinate input, validates it, and returns a converted index to use for board update
        while True:
            # take the input and convert to int. error catch if can't convert (not a num) and recur
            try:
                x, y = [int(i) for i in input(line).split()]
                pass
            except:
                print("You should enter numbers!")
                continue
            # error catch if not in range and recur
            if x not in range(1, 4) or y not in range(1, 4):
                print("Coordinates should be from 1 to 3!")
                continue
            # error catch if not in blank space and recur
            idx = TicTacToe.coord_to_idx[(x, y)]
            if board[idx] == "_":
                return idx
                break    
            else:
                print("This cell is occupied! Choose another one!")
                continue
    
    def symbol_choice(self, board):
        # convert dict values to list for python3
        symbol_list = list(board.values())
        # greater than, since start with X
        if symbol_list.count("X") > symbol_list.count("O"):
            return "O"
        else:
            return "X"
        
    def symbol_opp(self, symbol):
        # returns the opposite symbol
        if symbol == "X":
            return "O"
        else:
            return "X"

    def board_print(self, board):
        print("---------")
        print('| ' + board[1] + ' ' + board[2] + ' ' + board[3] + ' |')
        print('| ' + board[4] + ' ' + board[5] + ' ' + board[6] + ' |')
        print('| ' + board[7] + ' ' + board[8] + ' ' + board[9] + ' |')
        print("---------")
        return True
        
    def board_wins(self, board, symbol):
        # check board win con for any symbol
        # 3 horizontal checks for wins
        if board[1] == board[2] == board[3] == symbol:
            return True
        elif board[4] == board[5] == board[6] == symbol:
            return True
        elif board[7] == board[8] == board[9] == symbol:
            return True
        
        # 3 vertical checks for wins
        elif board[1] == board[4] == board[7] == symbol:
            return True
        elif board[2] == board[5] == board[8] == symbol:
            return True
        elif board[3] == board[6] == board[9] == symbol:
            return True
        
        # 2 diagonal checks for wins
        elif board[1] == board[5] == board[9] == symbol:
            return True
        elif board[3] == board[5] == board[7] == symbol:
            return True
        
        else:
            return False
    
    def board_state(self, board):
        # returns the state and boolean whether game is over
        # have to split from wins check since want to check for both symbols
        if self.board_wins(board, "X"):
            return "X wins", True
        elif self.board_wins(board, "O"):
            return "O wins", True
            
        # unfinished or draw states    
        elif list(board.values()).count("_") > 0:
            return "Game not finished", False
            
        elif list(board.values()).count("_") == 0:
            return "Draw", True
    
    def board_empty(self, board):
        # returns list of empty moves remaining
        return [key for key, value in board.items() if value == "_"]
     
    def check_win(self, board, symbol, moves):
        # checks if a move from a list of moves would win the game
        # if so, returns True and the move; if not returns False and None
        # empty list to track if move wins or not 
        move_wins = []
        for move in moves:
            # create a copy of board to test the move; have to use copy and not = for reference
            board_copy = board.copy()
            board_copy.update({move: symbol})
            move_wins.append(self.board_wins(board_copy, symbol))
        # have an array of moves, array of whether it would win
        # multiply both, zipped, to get list of move (if any) and blanks
        winning_move = [move * win for move, win in zip(moves, move_wins)]
        # remove empty blanks
        winning_move = [x for x in winning_move if x]
        if winning_move:
            return True, winning_move[0]
        else:
            return False, None
    
    def move_user(self, board):
        # take coordinate input, update, and print the board
        index = self.enter_coord("Enter the coordinates: ", board)
        symbol = self.symbol_choice(board)
        # convert to temp dictionary to update
        board.update({index: symbol})
        self.board_print(board)
        return True
        
    def move_com_easy(self, board):
        # easy setting, random choice for computer moves  
        print('Making move level "easy"')
        # get all legal moves 
        empty_box = self.board_empty(board)
        index = random.choice(empty_box)
        symbol = self.symbol_choice(board)
        # convert to temp dictionary to update
        board.update({index: symbol})
        self.board_print(board)
        return True
        
    def move_com_med(self, board):
        # med setting, if it can win in one move (if it has two in a row), it places a third to get three in a row and win
        # If the opponent can win in one move, it plays the third itself to block the opponent to win
        # Otherwise, it makes a random move
        print('Making move level "medium"')
        # get all legal moves 
        empty_box = self.board_empty(board)
        # get the current player symbol and the opponent symbol to check for wins and blocks
        symbol = self.symbol_choice(board)
        opp_symbol = self.symbol_opp(symbol)
        # check if current player can win or block; opponent's winning move is your blocking move  
        win, move_win = self.check_win(board, symbol, empty_box)
        block, move_block = self.check_win(board, opp_symbol, empty_box)
        if win:
            board.update({move_win: symbol})
            self.board_print(board)
        elif block:
            board.update({move_block: symbol})
            self.board_print(board)
        else:
            index = random.choice(empty_box)
            board.update({index: symbol})
            self.board_print(board)
        return True
        
    def max_move(self, board, symbol, moves, alpha, beta):
        # find the value maximising move for a player (symbol) given a board state and list of available moves
        # return the value of the move, and the move
        # possible values are -1 for loss, 0 for tie, 1 for win
        # https://puzzling.stackexchange.com/questions/30/what-is-the-optimal-first-move-in-tic-tac-toe
        # https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
        # https://www.youtube.com/watch?v=6ELUvkSkCts
        
        # initialise the max_val -2 so can overwrite; initialise max_move
        max_val = -2
        max_move = None
        # check if board is in ending state
        state, flag = self.board_state(board)
        if flag:
            if (state == "X wins" and symbol == "X") or (state == "O wins" and symbol == "O"):
                return (1, None)
            elif (state == "X wins" and symbol == "O") or (state == "O wins" and symbol == "X"):
                return (-1, None)
            else:
                return (0, None)
        # if game hasn't ended, run through all moves for player (symbol)
        # then play the next move for opponent (opposite symbol),
        # which is recursive and looks at all opponent moves
        for move in moves:
            board_copy = board.copy()
            board_copy.update({move: symbol})
            opp_symbol = self.symbol_opp(symbol)
            empty_box = self.board_empty(board_copy)
            # returns the value (for you) an opponent's moves would return, for all their moves
            # higher is better for you, means you won (or drew)
            # will choose that winning move (and value)
            val, _ = self.min_move(board_copy, opp_symbol, empty_box, alpha, beta)
            if val > max_val:
                max_val, max_move = val, move

            # alpha beta prune
            # if the val is higher than MIN so far from prior moves,
            # none of the other moves in moves loop will matter
            # since this val will be ignored when passed into min_move
            if max_val >= beta:
                return max_val, max_move
            # update the value of best choice so far for MAX to pass into min_move as alpha
            if max_val > alpha:
                alpha = max_val
        return max_val, max_move
    
    def min_move(self, board, symbol, moves, alpha, beta):
        # find the value minimising move; return the value of the move, and the move 
        # initialise the min_val 2 so can overwrite; initialise min_move
        min_val = 2
        min_move = None
        state, flag = self.board_state(board)
        # possible values are -1 for win, 0 for tie, 1 for loss; opposite of max_move
        # think of it this way: we want to minimise this outcome. If the symbol wins, that's bad (for the opposite symbol)
        if flag:
            if (state == "X wins" and symbol == "X") or (state == "O wins" and symbol == "O"):
                return (-1, None)
            elif (state == "X wins" and symbol == "O") or (state == "O wins" and symbol == "X"):
                return (1, None)
            else:
                return (0, None)
        # run through all options for this symbol and play next move for opp_symbol
        for move in moves:
            board_copy = board.copy()
            board_copy.update({move: symbol})
            opp_symbol = self.symbol_opp(symbol)
            empty_box = self.board_empty(board_copy)
            val, _ = self.max_move(board_copy, opp_symbol, empty_box, alpha, beta)
            if val < min_val:
                min_val, min_move = val, move 

            # alpha beta prune
            # if the val is lower than MAX so far from prior moves,
            # none of the other moves in moves loop will matter
            # since when you pass this result into max_move
            # it'll be ignored
            if min_val <= alpha:
                return min_val, move
            # update the value of best choice so far for MIN
            if min_val < beta:
                beta = min_val
        return min_val, min_move    
    
    def move_com_hard(self, board):
        print('Making move level "hard"')
        # get all legal moves 
        empty_box = [key for key, value in board.items() if value == "_"]
        symbol = self.symbol_choice(board)
        # alpha has to be lower than lowest, beta higher than highest
        _, move = self.max_move(board, symbol, empty_box, -2, 2)
        board.update({move: symbol})
        self.board_print(board)
        return True
        
tictactoe = TicTacToe()
tictactoe.main()  
        