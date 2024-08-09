"""
Provide code and solution for Application 4
"""

DESKTOP = True

from difflib import SequenceMatcher
import math
import random
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import string

if DESKTOP:
    import matplotlib.pyplot as plt
    import coursera_algo_project_4 as student
# else:
#     import simpleplot
#     import userXX_XXXXXXX as student
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib.request.urlopen(filename)
    ykeys = scoring_file.readline().decode('utf-8')
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)

    # keys will be byte strings. 
    # need to decode the byte strings to regular strings before constructing the dictionary.
    scoring_dict = {key.decode('utf-8'): value for key, value in scoring_dict.items()}

    return scoring_dict

def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib.request.urlopen(filename)
    protein_seq = protein_file.read().decode('utf-8')
    protein_seq = protein_seq.rstrip()
    return protein_seq

def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib.request.urlopen(filename)
    
    # read in files as string
    words = word_file.read().decode('utf-8')
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print("Loaded a dictionary with", len(word_list), "words")
    return word_list

def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Simulates local alignment trials between two sequences.

    Parameters:
        seq_x (str): First input sequence.
        seq_y (str): Second input sequence.
        scoring_matrix (dict): Matrix used for scoring the alignment.
        num_trials (int): Number of random trials to perform.

    Returns:
        dict: An un-normalized distribution of alignment scores.

    Process:
        - Shuffle seq_y to generate a random permutation rand_y.
        - Compute the local alignment score between seq_x and rand_y.
        - Increment the score in the scoring_distribution dictionary.
        - Repeat for num_trials iterations.
    """
    scoring_distribution = {}

    for _ in range(num_trials):
        rand_y = ''.join(random.sample(seq_y, len(seq_y)))
        local_alignment_matrix = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        (score, align_x, align_y) = student.compute_local_alignment(seq_x, rand_y, scoring_matrix, local_alignment_matrix)
        scoring_distribution[score] = scoring_distribution.get(score, 0) + 1

    return scoring_distribution

def plot_norm_distribution(distribution):
    """
    normalises and plots a distro
    """
    total = sum(distribution.values())
    normalised_distro = {score: count / total for score, count in distribution.items()}

    plt.bar(normalised_distro.keys(), normalised_distro.values())

    # Add labels and title
    plt.xlabel('Score')
    plt.ylabel('Fraction of Total Trials')
    plt.title('Normalised Distribution of Local Alignment Scores')

    # Display the plot
    plt.show()

    return normalised_distro

def calculate_statistics(distribution):
    """
    Calculates the mean, standard deviation, and z-scores for a given distribution.

    Parameters:
    distribution (dict): A dictionary where keys are scores and values are their counts.

    Returns:
    tuple: mean, standard deviation, and a dictionary of z-scores.
    """
    # Flatten the distribution into a list of scores
    all_scores = [score for score, count in distribution.items() for _ in range(count)]
    
    # Calculate mean
    mean = np.mean(all_scores)
    
    # Calculate standard deviation
    std_dev = np.std(all_scores)
    
    return mean, std_dev

def check_spelling(checked_word, dist, word_list):
    """
    iterates through word_list and 
    returns the set of all words that are 
    within edit distance dist of the string checked_word.
    """
    within_set = set([])

    # get scoring matrix of all alphabet letters with custom values
    # If two corresponding non-dash characters agree, the scoring matrix scores that match as 2
    # Two matching characters also increase the size of len(x) + len(y) by exactly two, 
    # leading to no increase in the edit distance.
    alphabet = string.ascii_lowercase
    scoring_matrix = student.build_scoring_matrix(alphabet, 2, 1, 0)

    for word in word_list:
        alignment_matrix = student.compute_alignment_matrix(checked_word, word, scoring_matrix, True)
        score, align_x, align_y = student.compute_global_alignment(checked_word, word, scoring_matrix, alignment_matrix)
        # len(x) + len(y) - score(x, y) from global alignment
        edit_dist = len(checked_word) + len(word) - score
        if edit_dist <= dist:
            within_set.add(word)

    return within_set

human_eyeless_seq = read_protein(HUMAN_EYELESS_URL)
fly_eyeless_seq = read_protein(FRUITFLY_EYELESS_URL)
pax_seq = read_protein(CONSENSUS_PAX_URL)
pam50_scoring_matrix = read_scoring_matrix(PAM50_URL)
word_list = read_words(WORD_LIST_URL)

# question 1 
local_human_fly_alignment_matrix = student.compute_alignment_matrix(human_eyeless_seq, fly_eyeless_seq, pam50_scoring_matrix, global_flag=False)
(local_human_fly_score, local_align_human, local_align_fly) = student.compute_local_alignment(human_eyeless_seq, fly_eyeless_seq, pam50_scoring_matrix, local_human_fly_alignment_matrix)
print(f"score is {local_human_fly_score} \n human alignment is {local_align_human} \n fly alignment is {local_align_fly}")

# question 2
local_align_human_adj = local_align_human.replace("-", "")
local_align_fly_adj = local_align_fly.replace("-", "")
global_human_adj_pax_alignment_matrix = student.compute_alignment_matrix(local_align_human_adj, pax_seq, pam50_scoring_matrix, global_flag=True)
global_fly_adj_pax_alignment_matrix = student.compute_alignment_matrix(local_align_fly_adj, pax_seq, pam50_scoring_matrix, global_flag=True)
(global_human_adj_pax_score, global_align_human_adj, global_align_pax) = student.compute_global_alignment(local_align_human_adj, pax_seq, pam50_scoring_matrix, global_human_adj_pax_alignment_matrix)
(global_fly_adj_pax_score, global_align_fly_adj, global_align_pax) = student.compute_global_alignment(local_align_fly_adj, pax_seq, pam50_scoring_matrix, global_fly_adj_pax_alignment_matrix)

print(f"human-pax ratio is {SequenceMatcher(None, global_align_human_adj, global_align_pax).ratio()}")
print(f"fly-pax ratio is {SequenceMatcher(None, global_align_fly_adj, global_align_pax).ratio()}")

# question 4
null_distribution = generate_null_distribution(human_eyeless_seq, fly_eyeless_seq, pam50_scoring_matrix, 1000)
# plot_norm_distribution(null_distribution)

# question 5 
mean, std_dev = calculate_statistics(null_distribution)

print("Mean:", mean)
print("Standard Deviation:", std_dev)
print(f"Local human fly zscore is {(local_human_fly_score - mean)/std_dev}")

# question 8
print(check_spelling("humble", 1, word_list))
print(check_spelling("firefly", 2, word_list))