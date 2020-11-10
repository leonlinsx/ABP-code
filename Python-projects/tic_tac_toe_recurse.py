# recurse tic tac toe project
# plays tic tac toe between two humans

# Before your interview, write a program that lets two humans play a game of Tic Tac Toe in a terminal. 
# The program should let the players take turns to input their moves. 
# The program should report the outcome of the game.

import sys
import random

class TicTacToe:

    def __init__(self):
        self.board = self.board_init()
        self.symbol = self.check_symbol(self.board)

        self.instructions()
        self.board_print(self.board_instruction())
        print("")

    # main function to start playing the game
    def main(self):
        player1, player2 = self.menu()

        while True:
            if player1 == "user":
                self.move_user()
            elif player1 == "easy":
                self.move_easy()
            elif player1 == "hard":
                self.move_hard()
            state, self.ended = self.check_state(self.board)
            if self.ended:
                break


            if player2 == "user":
                self.move_user()
            elif player2 == "easy":
                self.move_easy()
            elif player2 == "hard":
                self.move_hard()
            state, self.ended = self.check_state(self.board)
            if self.ended:
                break

        print(state, '\n')

        # check if want to repeat game
        while True:
            repeat = input("Play again (y/n) ? ").lower()
            if repeat not in ("y", "n"):
                print("Unknown command")
                continue
            elif repeat == "y":
                self.board = self.board_init()
                self.main()
            else:
                sys.exit()

    # instructions to print at start of game
    def instructions(self):
        print("Instructions:")
        print("Input command takes three arguments: start/exit, player1, player2")
        print("If exit is the first word, game will exit, regardless of words after")
        print("player1 and player2 can be 'user' or 'easy' or 'hard' (to be added)\n")
        print("Input coordinates takes an int as argument for the coordinate")
        print("Coordinates for the board are 1 on the top left and 9 on  bottom right\n")

    # takes input command and returns player types (user or com)
    def menu(self):

        player_types = ["user", "easy", "hard"]

        while True:
            cmd_list = input("Input command: ").lower().split()
            if cmd_list[0] == "exit":
                sys.exit()

            elif cmd_list[0] != "start":
                print("First command has to be start or exit")
                continue
            elif cmd_list[1] not in player_types or cmd_list[2] not in player_types:
                print("player1 and player2 have to be either: ")
                print(player_types)
                continue
            else:
                player1, player2 = cmd_list[1], cmd_list[2]
                break

        return player1, player2

    # returns empty board dict, using " " to represent empty cells
    def board_init(self):
        board = {1: " ", 2: " ", 3: " ",
                 4: " ", 5: " ", 6: " ",
                 7: " ", 8: " ", 9: " "}
        return board

    # returns board dict with coord number, to print for instructions
    def board_instruction(self):
        board = {1: "1", 2: "2", 3: "3",
                 4: "4", 5: "5", 6: "6",
                 7: "7", 8: "8", 9: "9"}
        return board

    # takes a board dict and prints a formatted board
    def board_print(self, board):
        print("-------")
        print("|" + board[1] + "|" + board[2] + "|" + board[3] + "|")
        print("|" + board[4] + "|" + board[5] + "|" + board[6] + "|")
        print("|" + board[7] + "|" + board[8] + "|" + board[9] + "|")
        print("-------")

    # takes a board dict and symbol
    # returns boolean if game is won for that symbol
    # prefer checking with a symbol since don't need to find the winning symbol after
    def board_wins(self, board, symbol):
        # 3 horizontal
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

    # takes a board dict and returns list of empty cells
    def board_empty(self, board):
        return [key for key, value in board.items() if value == " "]

    # returns the symbol whose turn it is for a board
    # assumes "X" goes first
    def check_symbol(self, board):
        symbol_list = list(board.values())
        if symbol_list.count("X") > symbol_list.count("O"):
            return "O"
        else:
            return "X"

    # checks the state of the game - win/draw/unfinished
    # returns the state and also a boolean on whether finished
    def check_state(self, board):
        if self.board_wins(board, "X"):
            return "X wins", True
        elif self.board_wins(board, "O"):
            return "O wins", True

        elif list(board.values()).count(" ") == 0:
            return "Draw", True

        else:
            return "Game not finished", False

    # takes coordinate input, validates input, updates board, prints board
    def move_user(self):
        # input validation if not int string
        while True:
            coord = input("Input coordinates: ")
            try:
                coord = int(coord)
            except:
                print("You should enter an integer!")
                continue
            # or if not in range of board
            if coord not in range(1, 10):
                print("Coordinates should be from 1 to 9!")
                continue
            # or if is an occupied cell
            elif coord not in self.board_empty(self.board):
                print("That cell is occupied, pick another!")
                continue
            else:
                break

        # get the right turn
        self.symbol = self.check_symbol(self.board)

        # note the board was stored using ints as keys, not str
        self.board.update({coord: self.symbol})
        self.board_print(self.board)

    # computer chooses a random move
    def move_easy(self):
        
        # get the right turn
        self.symbol = self.check_symbol(self.board)

        coord = random.choice(self.board_empty(self.board))

        print("Computer is making move 'easy'")
        self.board.update({coord: self.symbol})
        self.board_print(self.board)

    # computer chooses a winning or blocking move if able
    def move_hard(self):

        # get the right turn
        self.symbol = self.check_symbol(self.board)
        # get list of avail cells
        choice_list = self.board_empty(self.board)

        coord = None

        # checks if computer can win
        for choice in choice_list:
            board_copy = self.board.copy()
            board_copy.update({choice: self.symbol})
            if self.board_wins(board_copy, self.symbol):
                coord = choice
                break

        # checks if computer can block w/ opposite symbol
        for choice in choice_list:
            board_copy = self.board.copy()
            if self.symbol == "X":
                temp_symbol = "O"
            else:
                temp_symbol = "X"
            board_copy.update({choice: temp_symbol})
            if self.board_wins(board_copy, temp_symbol):
                coord = choice
                break

        if not coord:
            coord = random.choice(choice_list)

        print("Computer is making move 'hard'")
        self.board.update({coord: self.symbol})
        self.board_print(self.board)


tictactoe = TicTacToe()
tictactoe.main()
