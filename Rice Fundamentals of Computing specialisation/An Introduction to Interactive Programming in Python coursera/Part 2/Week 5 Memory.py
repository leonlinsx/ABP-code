# implementation of card game - Memory
# http://www.codeskulptor.org/#user47_3wMfpnOjUc_2.py

import simplegui
import random


# helper function to initialize globals
def new_game():
    # randomly shuffled list of 0-7 x2, 16 False exposed
    global card_list, exposed, state, turns, label
    
    card_list = list(range(8)) + list(range(8))
    random.shuffle(card_list)
    exposed = [False] * 16
    state = 0 
    turns = 0
    label.set_text('Turns = ' + str(turns))
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    # since 16 cards fill the space, mod 50 is the index of card clicked
    global exposed, state, card1, card2, card_list, turns, label
    
    idx = pos[0] // 50
    
    if exposed[idx] != True:
    
        if state == 0:  # game start
            exposed[idx] = True
            card1 = idx
            state = 1
        elif state == 1:  # 1 card exposed
            exposed[idx] = True
            card2 = idx
            state = 2
        else:  # 2 card exposed, end the turn
            # flip both current cards if not matching
            if card_list[card1] != card_list[card2]:
                exposed[card1] = False
                exposed[card2] = False
                
            exposed[idx] = True
            card1 = idx
            state = 1
            
            turns += 1
            label.set_text('Turns = ' + str(turns))
    
    else:
        pass  # ignore mouse click if already exposed
        
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card_index in range(len(card_list)):
        card_pos = 50 * card_index
        if exposed[card_index]:  # if card exposed draw number
            canvas.draw_text(str(card_list[card_index]), (card_pos + 8, 75), 70, "White")
        else:
            point_list = [(card_pos, 0), (card_pos + 50, 0), (card_pos + 50, 100), (card_pos, 100)]
            canvas.draw_polygon(point_list, 1, "Black", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric