def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    args:
    Takes as input a set of characters alphabet and three scores 
    diag_score, off_diag_score, and dash_score. 
    
    returns:
    The function returns a dictionary of dictionaries 
    whose entries are indexed by pairs of characters in alphabet plus '-'

    Given two characters row_char and col_char, 
    we can access the matrix entry corresponding to this pair of characters via 
    scoring_matrix[row_char][col_char]

    The score for any entry indexed by one or more dashes is dash_score. 
    The score for the remaining diagonal entries is diag_score. 
    The score for the remaining off-diagonal entries is off_diag_score
    
    include an entry for two dashes (which will never be used).
    """
    char_list = list(alphabet)
    char_list.append("-")
    
    scoring_matrix = {}
    for row_char in char_list:
        scoring_matrix[row_char] = {}
        for col_char in char_list:
            if row_char == "-" or col_char == "-":            
                scoring_matrix[row_char][col_char] = dash_score
            elif row_char == col_char:
                scoring_matrix[row_char][col_char] = diag_score
            else:
                scoring_matrix[row_char][col_char] = off_diag_score
    
    return scoring_matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    args:
    Takes as input two sequences seq_x and seq_y 
    whose elements share a common alphabet with scoring_matrix

    computes and returns the alignment matrix for seq_x and seq_y

    If global_flag is True, 
    each entry of the alignment matrix is computed using the method described in Question 8 of the Homework. 
    (global alignment)

    If global_flag is False,
    each entry is computed using the method described in Question 12 of the Homework.
    (local pairwise alignment)

    Entries in the alignment matrix will be indexed by their row and column with these integer indices starting at zero. 
    We will model these matrices as lists of lists in Python and can access a particular entry via an expression of the form 
    alignment_matrix[row][col].
    """
    alignment_matrix = [[0]]
    num_rows = len(seq_x) + 1
    num_cols = len(seq_y) + 1

    # fill in first row and first col where matching with increasing number of '-'
    for row_idx in range(1, num_rows):
        score = alignment_matrix[row_idx - 1][0] + scoring_matrix[seq_x[row_idx - 1]]['-']
        alignment_matrix.insert(row_idx, [max(score, 0) if not global_flag else score])
    for col_idx in range(1, num_cols):
        score = alignment_matrix[0][col_idx - 1] + scoring_matrix['-'][seq_y[col_idx - 1]]
        alignment_matrix[0].insert(col_idx, max(score, 0) if not global_flag else score)

    # dynamic programming fill in rest of matrix based on earlier calced values
    for row_idx in range(1, num_rows):
        for col_idx in range(1, num_cols):
            score_pick_both_seq = alignment_matrix[row_idx - 1][col_idx - 1] + scoring_matrix[seq_x[row_idx - 1]][seq_y[col_idx - 1]]
            score_pick_seq_x = alignment_matrix[row_idx - 1][col_idx] + scoring_matrix[seq_x[row_idx - 1]]['-']
            score_pick_seq_y = alignment_matrix[row_idx][col_idx - 1] + scoring_matrix['-'][seq_y[col_idx - 1]]
            score = max(score_pick_both_seq, score_pick_seq_x, score_pick_seq_y)
            alignment_matrix[row_idx].insert(col_idx, max(score, 0) if not global_flag else score)

    return alignment_matrix
       
def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    args:
    Takes as input two sequences, seq_x and seq_y, 
    whose elements share a common alphabet with the scoring matrix scoring_matrix. 
    
    This function computes a global alignment of seq_x and seq_y 
    using the global alignment matrix alignment_matrix. 
    
    returns:
    The function returns a tuple of the form (score, align_x, align_y) 
    where score is the score of the global alignment, align_x, and align_y. 
    
    Note that align_x and align_y should have the same length 
    and may include the padding character '-'.
    """
    row_idx, col_idx = len(seq_x), len(seq_y)
    align_x, align_y = "", ""

    # calc scores before row_idx and col_idx are used in while loops
    if row_idx > 0 and col_idx > 0:
        score = alignment_matrix[row_idx][col_idx]
    else:
        score = 0
    
    # traceback walking back in the matrix from entry S[|X|, |Y|] to entry S[0, 0] 
    # along the path that has score S[|X|, |Y|], 
    # and while doing so, creating the alignment itself.
    while row_idx != 0 and col_idx != 0:
        if alignment_matrix[row_idx][col_idx] == (alignment_matrix[row_idx - 1][col_idx - 1] + scoring_matrix[seq_x[row_idx - 1]][seq_y[col_idx - 1]]):
            align_x = seq_x[row_idx - 1] + align_x
            align_y = seq_y[col_idx - 1] + align_y
            row_idx -= 1
            col_idx -= 1
        else:
            # If the current cell value equals the value from the cell above plus the score for a gap in seq_y, 
            # a gap ('-') is added to align_y, and the character from seq_x is added to align_x, and row_idx is decremented.
            if alignment_matrix[row_idx][col_idx] == (alignment_matrix[row_idx - 1][col_idx] + scoring_matrix[seq_x[row_idx - 1]]['-']):
                align_x = seq_x[row_idx - 1] + align_x
                align_y = '-' + align_y
                row_idx -= 1
            else:
                align_x = '-' + align_x
                align_y = seq_y[col_idx - 1] + align_y
                col_idx -= 1
    
    # pad with dash if havent fully transversed rows / cols
    while row_idx != 0:
        align_x = seq_x[row_idx - 1] + align_x
        align_y = '-' + align_y
        row_idx -= 1
    while col_idx != 0:
        align_x = '-' + align_x
        align_y = seq_y[col_idx - 1] + align_y
        col_idx -= 1

    return (score, align_x, align_y)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    args:
    Takes as input two sequences seq_x and seq_y 
    whose elements share a common alphabet with the scoring matrix scoring_matrix. 
    
    This function computes a local alignment of seq_x and seq_y using the local alignment matrix alignment_matrix. 
    
    returns:
    The function returns a tuple of the form (score, align_x, align_y) 
    where score is the score of the optimal local alignment, align_x, and align_y. 
    
    Note that align_x and align_y should have the same length and may include the padding character '-'.
    """
    row_idx, col_idx, score = 0, 0, 0
    align_x, align_y = "", ""
    
    for align_row_idx in range(len(seq_x) + 1):
        for align_col_idx in range(len(seq_y) + 1):
            if score <= alignment_matrix[align_row_idx][align_col_idx]:
                score = alignment_matrix[align_row_idx][align_col_idx]
                row_idx = align_row_idx
                col_idx = align_col_idx

    # traceback walking back in the matrix from entry S[|X|, |Y|] to entry S[0, 0] 
    # along the path that has score S[|X|, |Y|], 
    # and while doing so, creating the alignment itself.
    # stop the traceback when first entry with value 0 is encountered
    while row_idx != 0 and col_idx != 0 and alignment_matrix[row_idx][col_idx] != 0:
        if alignment_matrix[row_idx][col_idx] == (alignment_matrix[row_idx - 1][col_idx - 1] + scoring_matrix[seq_x[row_idx - 1]][seq_y[col_idx - 1]]):
            align_x = seq_x[row_idx - 1] + align_x
            align_y = seq_y[col_idx - 1] + align_y
            row_idx -= 1
            col_idx -= 1
        else:
            # If the current cell value equals the value from the cell above plus the score for a gap in seq_y, 
            # a gap ('-') is added to align_y, and the character from seq_x is added to align_x, and row_idx is decremented.
            if alignment_matrix[row_idx][col_idx] == (alignment_matrix[row_idx - 1][col_idx] + scoring_matrix[seq_x[row_idx - 1]]['-']):
                align_x = seq_x[row_idx - 1] + align_x
                align_y = '-' + align_y
                row_idx -= 1
            else:
                align_x = '-' + align_x
                align_y = seq_y[col_idx - 1] + align_y
                col_idx -= 1
    
    # do not need to pad with dash if havent fully transversed rows / cols, since getting local alignment only

    return (score, align_x, align_y)  


# print(build_scoring_matrix(set(['A', 'C', 'T', 'G']), 6, 2, -4))
# print(compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, True))
# print(compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, False))
# print(compute_global_alignment('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0, -4], [-4, 6]]))
