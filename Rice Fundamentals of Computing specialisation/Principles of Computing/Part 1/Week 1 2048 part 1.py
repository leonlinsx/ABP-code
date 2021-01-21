"""
Merge function for 2048 game.
http://www.codeskulptor.org/#user47_PfoXzWfTYK_1.py
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """

    res = squish(line)
    
    idx = 0
    while idx < len(res) - 1:
        if res[idx] == res[idx + 1]:
            res[idx] *= 2
            res[idx + 1] = 0
        idx += 1
    
    res = squish(res)
    
    return res

def squish(line):
    """
    Function that moves all numbers to 'front' index 0 of line
    """
    idx = 0
    res = [0] * len(line)
    for num in line:
        if num != 0:
            res[idx] = num
            idx += 1
           
    return res
