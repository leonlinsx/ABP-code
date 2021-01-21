# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
# http://www.codeskulptor.org/#user47_FhBnxQnFXG_5.py
# guesses a number within a range from user input

import simplegui
import random
import math

secret_number = 0
max_num = 100
game_type_100 = True

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, max_num, guesses
    
    
    if game_type_100:
        max_num = 100
        guesses = 7
    else:
        max_num = 1000
        guesses = 10
    
    secret_number = random.randrange(0, max_num)
    
    print "New game. Range is from 0 to", max_num
    print "Number of remaining guesses is", guesses, "\n" 

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global max_num, guesses, game_type_100
    max_num = 100
    guesses = int(math.ceil(math.log((max_num - 0 + 1), 2)))  # 2 ** n >= high - low + 1
    game_type_100 = True
    
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global max_num, guesses, game_type_100
    max_num = 1000
    guesses = int(math.ceil(math.log((max_num - 0 + 1), 2)))  # 2 ** n >= high - low + 1
    game_type_100 = False
    
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    g = int(guess)
    print "Guess was", g
    
    global guesses, secret_number
    guesses -= 1
    print "Number of remaining guesses is", guesses
    
    if guesses == 0 and secret_number != g:
        print "You ran out of guesses. The number was", secret_number, "\n"
        new_game()
    elif secret_number == g:
        print "Correct!\n"
        new_game()
    elif secret_number > g:
        print "Higher!\n"
    elif secret_number < g:
        print "Lower!\n"

    
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game 
f.start()
new_game()

# always remember to check your completed program against the grading rubric
