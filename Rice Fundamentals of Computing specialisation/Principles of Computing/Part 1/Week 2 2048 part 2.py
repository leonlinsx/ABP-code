"""
Clone of 2048 game.
http://www.codeskulptor.org/#user47_SLw7xPWtfd_10.py
"""

import poc_2048_gui
import random
#import user47_YOogrwX7s1_2 as tester

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
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
    Helper function that moves all numbers to 'front' index 0 of line
    """
    idx = 0
    res = [0] * len(line)
    for num in line:
        if num != 0:
            res[idx] = num
            idx += 1
           
    return res

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.grid = None
        self.reset()
        
        # pre-computing a list of the indices for the initial tiles in that direction
        # to use for move method
        self.idx_dict = {}
        self.idx_dict[UP] = [(0, col) for col in range(self.width)]
        self.idx_dict[DOWN] = [(self.height - 1, col) for col in range(self.width)]
        self.idx_dict[LEFT] = [(row, 0) for row in range(self.height)]
        self.idx_dict[RIGHT] = [(row, self.width - 1) for row in range(self.height)]
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # empty grid with row x col dimension
        self.grid = [ [0 for _col in range(self.width)] for _row in range(self.height)]

        # create 2 tiles to start game
        self.new_tile()
        self.new_tile()    
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self.grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        initial_tiles = self.idx_dict[direction]
        offs = OFFSETS[direction]
        # calc the amount of steps vertical or horizontal
        steps = 0
        if direction == 1 or direction == 2:
            steps = self.height
        else:
            steps = self.width
      
        changed = False
        
        # tile is a tuple of row, col nums, in a list of tiles
        for tile in initial_tiles:
            idx_list = []
            for step in range(steps):
                row_num = tile[0] + step * offs[0]
                col_num = tile[1] + step * offs[1]
                idx_list.append((row_num, col_num))
            
            temp_list = [self.get_tile(idx[0], idx[1]) for idx in idx_list]
            
            merged_list = merge(temp_list)
            
            for step in range(steps):
                row_num = tile[0] + step * offs[0]
                col_num = tile[1] + step * offs[1]
                self.set_tile(row_num, col_num, merged_list[step])
                
            if merged_list != temp_list:
                changed = True
                
        if changed:
            self.new_tile()
                

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_squares = []
        for row_num, row in enumerate(self.grid):
            for col_num, num in enumerate(row):
                if num == 0:
                    empty_squares.append((row_num, col_num))
                
        selected_square = random.choice(empty_squares)
        
        if random.random() <= 0.1:
            self.set_tile(selected_square[0], selected_square[1], 4)
        else:
            self.set_tile(selected_square[0], selected_square[1], 2)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]

# test suite
# tester.run_suite(merge)

#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
