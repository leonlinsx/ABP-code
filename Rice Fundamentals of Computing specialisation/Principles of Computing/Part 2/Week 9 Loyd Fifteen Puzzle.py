"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors

test suite here: http://www.codeskulptor.org/#user48_cjISWqyOrU_192.py
practice tantrix game here: http://www.codeskulptor.org/#user48_uJR4f3aRKF_5.py
"""

import poc_fifteen_gui
#import user48_cjISWqyOrU_192 as fifteen_testsuite

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # 0 tile has to be in target_row, col
        if self.get_number(target_row, target_col) == 0:
            # All tiles in rows i+1 or below are solved
            for row in range(target_row + 1, self.get_height()):
                for col in range(self.get_width()):
                    if self.get_number(row, col) != row * self.get_width() + col:
                        return False
            # All tiles in row i to the right of position (i, j) are solved
            for col in range(target_col + 1, self.get_width()):
                if self.get_number(target_row, col) != target_row * self.get_width() + col:
                    return False
            return True
        else:
            return False

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position for target_row > 1, target_col > 0
        Updates puzzle and returns a move string
        """
        # If lower_row_invariant(i, j) is true prior to execution of solve_interior_tile(i, j), 
        # lower_row_invariant(i, j - 1) should be true after execution
        assert self.lower_row_invariant(target_row, target_col)     
        
        move_str = self.position_tile(target_row, target_col, target_row, target_col)
        self.update_puzzle(move_str)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_str

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # If lower_row_invariant(i, 0) is true before, 
        # lower_row_invariant(i - 1, n - 1) should be true after; n is grid width
        assert self.lower_row_invariant(target_row, 0)
        
        # have to actually update and check where target tile is after update
        self.update_puzzle("ur")
        current_pos = self.current_position(target_row, 0)
        
        # if target tile is now in position
        if current_pos[0] == target_row and current_pos[1] == 0:
            move_str = "r" * (self.get_width() - 2)
        # apply the move string for a 3×2 puzzle as described in problem #9 of the homework 
        # to bring the target tile into position (i, 0)
        else:
            move_str = self.position_tile(target_row, 0, target_row - 1, 1)
            move_str += "ruldrdlurdluurddlur"
            move_str += "r" * (self.get_width() - 2)
        
        self.update_puzzle(move_str)
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
        return "ur" + move_str
    
    def position_tile(self, target_row, target_col, zero_row, zero_col):
        """
        moves target tile to target_row and col, with zero to the left
        """
        
        # Given a target position, find current position tuple of the tile that should be there
        current_pos = self.current_position(target_row, target_col)
        # need the row/col difference from the 0 tile to know how many moves to make
        row_diff = zero_row - current_pos[0]
        col_diff = zero_col - current_pos[1]               
        
        move_str = ""
        # move to same row as target
        move_str += "u" * row_diff
        # if target tile is to left, 
        if col_diff > 0:
            # move 0 tile left until it replaces target tile; 0 tile is left of target
            move_str += "l" * col_diff
            # both of these move the 0 tile and target tile right until target is above position
            # if target tile is in first row, have to use row below for the U shaped cycle move
            if current_pos[0] == 0:
                move_str += "drrul" * (col_diff - 1)
                # get 0 tile above target; affects target's row
                if row_diff > 0:
                    move_str += "dru"
                    row_diff -= 1
            # else can use row above for the inverted U shaped cycle
            else:
                move_str += "urrdl" * (col_diff - 1)
                # get 0 tile above target; does not affect target's row
                move_str += "ur"
        # if target tile is to right
        elif col_diff < 0:
            # move 0 tile right until it replaces target tile; 0 tile is right of target
            move_str += "r" * (-1 * col_diff)
            # both of these move the 0 tile and target tile left until target is above position
            # if target tile is in first row, have to use row below for the U shaped cycle move
            if current_pos[0] == 0:
                move_str += "dllur" * (-1 * col_diff - 1)
                # move 0 tile above target; affects target's row
                if row_diff > 0:
                    move_str += "dlu"
                    row_diff -= 1
            # else can use row above for the inverted U shaped cycle
            else:
                move_str += "ulldr" * (-1 * col_diff - 1)
                # move 0 tile above target; does not affect target's row
                move_str += "ul"
        # if target tile was directly above it's now one below
        else:
            row_diff -= 1
        
        if row_diff > 0:
            # 0 tile is above target tile, which is above target position by row_diff
            # cycle moves both downwards
            move_str += "lddru" * row_diff
            
        # get 0 tile in position
        move_str += "ld"            

        return move_str
        

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # check 0 is in 0, target_col
        if self.get_number(0, target_col) == 0:
            # loop through row 0
            for col in range(target_col + 1, self.get_width()):
                if self.get_number(0, col) != col:
                    return False
            # loop through row 1
            for col in range(target_col, self.get_width()):
                if self.get_number(1, col) != 1 * self.get_width() + col:
                    return False
            # loop through other rows
            for row in range(2, self.get_height()):
                for col in range(self.get_width()):
                    if self.get_number(row, col) != row * self.get_width() + col:
                        return False
            return True
        else:
            return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # check the 0 row, cols to the right
        for col in range(target_col + 1, self.get_width()):
            if self.get_number(0, col) != col:
                return False
        
        # if all those were right, check per normal
        return self.lower_row_invariant(1, target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        
        # have to actually update and check target after the update
        self.update_puzzle("ld")
        current_pos = self.current_position(0, target_col)
        
        # if target tile is in position
        if current_pos[0] == 0 and current_pos[1] == target_col:
            move_str = ""
        else:
            move_str = self.position_tile(0, target_col, 1, target_col - 1)
            move_str += "urdlurrdluldrruld"
        
        self.update_puzzle(move_str)
        assert self.row1_invariant(target_col - 1)
        return "ld" + move_str

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        
        move_str = self.position_tile(1, target_col, 1, target_col)
        # move 0 tile above to prep for solve_row0
        move_str += "ur"
        self.update_puzzle(move_str)        
        
        return move_str

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string.
        """
        # I think this forms a group? Only certain number of combos
        assert self.row1_invariant(1)
        self.update_puzzle("ul")
        
        # the position of the 1 tile tells us which move to use
        one_pos = self.current_position(0, 1)
        if one_pos[0] == 0 and one_pos[1] == 1:
            move_str = ""
        elif one_pos[1] == 1:
            move_str = "rdlu"
        elif one_pos[1] == 0:
            move_str = "drul"
        else:
            return "2x2 not solvable"
        
        self.update_puzzle(move_str)
        return "ul" + move_str

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_str = ""
        
        puzzle_copy = self.clone()
        height = puzzle_copy.get_height()
        width = puzzle_copy.get_width()
        
        # move 0 tile to bottom right
        zero_pos = puzzle_copy.current_position(0, 0)
        row_diff = height - zero_pos[0] 
        col_diff = width - zero_pos[1]
        move_str += "r" * (col_diff - 1)
        move_str += "d" * (row_diff - 1)
        puzzle_copy.update_puzzle(move_str)
        
        # solve rows after the first two rows
        for row in range(height - 1, 1, -1):
            for col in range(width - 1, -1, -1):
                if col == 0:
                    move_str += puzzle_copy.solve_col0_tile(row)
                else:
                    move_str += puzzle_copy.solve_interior_tile(row, col)
        
        # solve all except 2x2
        for col in range(width - 1, 1, -1):	
            for row in range(1, -1, -1):
                if row == 0:
                    move_str += puzzle_copy.solve_row0_tile(col)
                else:
                    move_str += puzzle_copy.solve_row1_tile(col)
        
        move_str += puzzle_copy.solve_2x2()
        
        self.update_puzzle(move_str)
        return move_str

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
#fifteen_testsuite.run_suite(Puzzle)



