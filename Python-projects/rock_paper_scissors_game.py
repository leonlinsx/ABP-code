import random
import sys

points_dict = {'win': 100,
                'draw': 50}

# start the game
name = input('Enter your name: ')
print(f'Hello, {name}')

# lookup user rating 
rating_file = open('rating.txt')
rating_dict = {}
for line in rating_file:
    key, val = line.split(maxsplit = 1)
    rating_dict[key] = int(val.rstrip())
rating = 0
if name in rating_dict.keys():
    rating = rating_dict[name]

# take user options 
options = input()
# jetbrains project v1.0
# rock paper scissors with user defined options

print("Okay, let's start")
if not options:
    options_list = ['rock', 'paper', 'scissors']
else:
    options_list = options.split(',')
matchup_dict = {}
for i in range(len(options_list)):
    temp_list = options_list[i + 1:len(options_list)] + options_list[:i]
    matchup_dict[options_list[i]] = temp_list[:len(temp_list) // 2]

# play the game 
while True:                
    user_choice = input()
    
    # user game commands
    if user_choice == '!exit':
        print('Bye!')
        break 
    elif user_choice == '!rating':
        print(f'Your rating: {rating}')
        continue    
    # input validation
    elif user_choice not in options_list:
        print('Invalid input')
        continue
    
    com_choice = random.choice(options_list)
    
    # print result
    if com_choice in matchup_dict[user_choice]:
        print(f"Sorry, but computer chose {com_choice}")
    elif com_choice == user_choice:
        print(f"There is a draw ({com_choice})")
        rating += points_dict['draw']
    else:
        print(f"Well done. Computer chose {com_choice} and failed")
        rating += points_dict['win']

rating_file.close()
