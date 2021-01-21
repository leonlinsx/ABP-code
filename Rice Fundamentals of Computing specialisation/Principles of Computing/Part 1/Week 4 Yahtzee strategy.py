"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
http://www.codeskulptor.org/#user47_1qZHxsY3PG_2.py
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    return max([hand.count(die) * die for die in hand])


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold (a tuple)
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    all_seq = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    total = 0.0  # init as float 
    for seq in all_seq:
        total += score(held_dice + seq)
#    print "ev: " + str(total / len(all_seq))
    return total / len(all_seq)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    
    https://www.coursera.org/learn/principles-of-computing-1/discussions/weeks/4/threads/PaU9Age6EeepAAp3RBDGpA/replies/9Tzt4mLQEeePJhJIucBoNg/comments/3M6HyGN3EeeU3Q5chjCViA
    """
    
    res_set = set([()])

    for die in hand:
        for hold in list(res_set):  # don't update and iterate the same set
            temp_list = list(hold)
            temp_list.append(die)
            res_set.add(tuple(temp_list))  # add rather than set update
                
    return res_set



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    max_val = 0
    max_hold = ()
    for hold in gen_all_holds(hand):
        exp_val = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if exp_val > max_val:  # go through all holds until find the max
            max_val = float(exp_val)
            max_hold = hold
            
    return (max_val, max_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



