# Mini-project #6 - Blackjack
# http://www.codeskulptor.org/#user47_Me6BQqplbo_3.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
action = "Hit or stand?"

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object to have an empty list of Card objects
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        card_str = " ".join([str(card) for card in self.cards])
        return "Hand contains " + card_str
        
    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_val = sum([VALUES[card.get_rank()] for card in self.cards])
        
        if "A" not in [card.get_rank() for card in self.cards]:
            return hand_val
        else:
            if hand_val + 10 <= 21:
                return hand_val + 10
            else:
                return hand_val
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards

        for idx, card in enumerate(self.cards):
            # pad 50 pixels on left; card is 72 pixels wide
            card.draw(canvas, (50 + pos[0] + idx * 72, pos[1]))
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object as list of cards. 
        # You can generate this list using a pair of nested for loops
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        card_str = " ".join([str(card) for card in self.cards])
        return "Deck contains " + card_str



#define event handlers for buttons
def deal():
    global outcome, in_play, action, score
    global DECK, PLAY_HAND, DEAL_HAND
    
    # if the "Deal" button is clicked during the middle of a round, 
    # the program reports that the player lost the round 
    # and updates the score appropriately.
    if in_play:
        outcome = "Player loses"
        score -= 1
        action = "New deal?"
        in_play = False
    
    else:
        # shuffle the deck (stored as a global variable), 
        # create new player and dealer hands (stored as global variables), 
        # and add two cards to each hand
        DECK = Deck()
        PLAY_HAND = Hand()
        DEAL_HAND = Hand()

        DECK.shuffle()
        PLAY_HAND.add_card(DECK.deal_card())
        PLAY_HAND.add_card(DECK.deal_card())
        DEAL_HAND.add_card(DECK.deal_card())
        DEAL_HAND.add_card(DECK.deal_card())

#        print("Player's hand:")
#        print(str(PLAY_HAND))
#        print("Dealer's hand:")
#        print(str(DEAL_HAND))

        in_play = True
        outcome = ""
        action = "Hit or stand?"

def hit():
    global in_play, DECK, PLAY_HAND, score, outcome, action
    # if the hand is in play, hit the player
    if in_play:
        PLAY_HAND.add_card(DECK.deal_card())
        # if busted, assign a message to outcome, update in_play and score
        if PLAY_HAND.get_value() > 21:
            in_play = False
            outcome = "You have busted"
            score -= 1
            action = "New deal?"
            
    else:
        outcome = "Not in play"
        action = "New deal?"
        
def stand():
    global in_play, DECK, DEAL_HAND, score, outcome, action
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while DEAL_HAND.get_value() < 17:
            DEAL_HAND.add_card(DECK.deal_card())
        # assign a message to outcome, update in_play and score
        if DEAL_HAND.get_value() > 21:
            in_play = False
#            print(DEAL_HAND)
#            print(PLAY_HAND)
            outcome = "Dealer busted"
            score += 1
            action = "New deal?"
        else:
            if DEAL_HAND.get_value() >= PLAY_HAND.get_value():
                in_play = False
#                print(DEAL_HAND)
#                print(PLAY_HAND)
                outcome = "Dealer won"
                score -= 1
                action = "New deal?"
            else:
                in_play = False
#                print(DEAL_HAND)
#                print(PLAY_HAND)
                outcome = "You won"
                score += 1
                action = "New deal?"
    else:
        if PLAY_HAND.get_value() > 21:
            outcome = "You have busted"
            action = "New deal?"
        else:
            outcome = "Not in play"
            action = "New deal?"
    
# draw handler    
def draw(canvas):
    # draw game title and score
    canvas.draw_text("Blackjack", (50, 100), 50, "Blue")
    canvas.draw_text("Score: " + str(score), (400, 100), 30, "Black")
    
    # draw dealer hand
    canvas.draw_text("Dealer", (50, 200), 30, "Black")
    canvas.draw_text(outcome, (200, 200), 30, "Black")
    DEAL_HAND.draw(canvas, [0, 220])
    # card size is 72, 96
    if in_play:
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        # canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest)
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, (50 + 36, 220 + 48), CARD_BACK_SIZE)
    
    # draw player hand
    canvas.draw_text("Player", (50, 400), 30, "Black")
    canvas.draw_text(action, (200, 400), 30, "Black")
    PLAY_HAND.draw(canvas, [0, 420])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric