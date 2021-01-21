"""
Student code for Word Wrangler game
Recursion practice, without using set, sorted, or sort.
No functions should mutate inputs; return new lists

Also must use more efficient algos for remove_duplicates and intersect
If not tester will time out
http://www.codeskulptor.org/#user47_3REaYEnr2f_6.py
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import math

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1) == 0:
        return list1
    else:
        idx = 0
        new_list = [list1[0]]
        for elem in list1:
            if elem != new_list[idx]:
                new_list.append(elem)
                idx += 1
        return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    len_1 = len(list1)
    len_2 = len(list2)
    new_list = []
    idx_1 = 0
    idx_2 = 0
    
    # only need to compare while both lists still have elems
    while idx_1 < len_1 and idx_2 < len_2:
        if list1[idx_1] < list2[idx_2]:
            idx_1 += 1
        elif list1[idx_1] > list2[idx_2]:
            idx_2 += 1
        else:
            new_list.append(list1[idx_1])
            idx_1 += 1
            idx_2 += 1
            
    return new_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    len_1 = len(list1)
    len_2 = len(list2)
    new_list = []  
    idx_1 = 0
    idx_2 = 0
    
    # while still comparing both lists at the same time
    while idx_1 < len_1 and idx_2 < len_2:
        if list1[idx_1] <= list2[idx_2]:
            new_list.append(list1[idx_1])
            idx_1 += 1
        else:
            new_list.append(list2[idx_2])
            idx_2 += 1
    
    # this means list2 broke the loop, 
    # so rest of list1 is larger, and in order
    while idx_1 < len_1:
        new_list.append(list1[idx_1])
        idx_1 += 1
    
    # this on the other hand means list1 broke the loop
    while idx_2 < len_2:
        new_list.append(list2[idx_2])
        idx_2 += 1
    
    return new_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
        # split the list in two
        mid_idx = int(math.floor(len(list1) / 2))
        left_list = list1[:mid_idx]
        right_list = list1[mid_idx:]
        
        return merge(merge_sort(left_list), merge_sort(right_list))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]  # this has to be a list for recursion to work
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        # inserting the initial character, first, 
        # in all possible positions within the string.
        new_strings = []
        for string in rest_strings:
            for idx in range(len(string) + 1):
                new_string = string[:idx] + first + string[idx:]
                new_strings.append(new_string)
        
        return rest_strings + new_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(WORDFILE)
    netfile = urllib2.urlopen(url)
    return [line[:-1] for line in netfile.readlines()]

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

#print gen_all_strings("aab")
    