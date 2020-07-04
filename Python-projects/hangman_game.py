# jetbrains project
# hangman game with defined word list

import random
import nltk

# get lowercase long word list from nltk corpus
# nltk.download()
# https://stackoverflow.com/a/28339791
from nltk.corpus import brown
wordset_lower = list(set(i.lower() for i in brown.words()))

def play_game():
    # random word from list
    word_list = wordset_lower
    ans = random.choice(word_list)

    # list of answer, interim ans, and guesses so far
    ans_list = list(ans)
    temp_list = list('-' * len(ans))
    guess_list = [] 
    tries = 8
    
    while start_game == 'play':
        print('\n')
        print(''.join(temp_list))
        print('Lives left:', tries)
        guess = input('Input a letter: ')
        # validate input
        if len(guess) != 1:
            print('You should input a single letter')     
            continue
        elif not guess.islower():
            print('It is not an ASCII lowercase letter')
            continue
        elif guess in guess_list:
            print('You already typed this letter')
            continue        
        # check guess against answer
        if guess in ans_list:
            for i in range(0, len(ans_list)):
                if ans_list[i] == guess:
                    temp_list[i] = guess
            guess_list.append(guess)
        else:
            tries -= 1
            guess_list.append(guess)
            print('No such letter in the word')
        # final outcome
        if '-' not in temp_list:
            print('You guessed the word!')
            print('You survived!')
            print('\n')
            break
        if tries == 0:
            print('You are hanged!')
            print('The word was:', ans)
            print('\n')
            break
            
while True:
    print("H A N G M A N")
    start_game = input('Type "play" to play the game, "exit" to quit:')
    # play or exit game
    if start_game not in ('play', 'exit'):
        continue
    if start_game == 'exit':
        break
    else:
        play_game()  