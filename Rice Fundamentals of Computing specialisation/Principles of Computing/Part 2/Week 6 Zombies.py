"""
Student portion of Zombie Apocalypse mini-project
Simulates Zombies chasing, Humans fleeing, and stationary obstacles
http://www.codeskulptor.org/#user47_8KxVJO5VXk_17.py
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        # can use the Grid class methods
        # but since the test intentionally uses the same method name
        # need to call it this way instead of self.clear()
        poc_grid.Grid.clear(self) 
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        num = 0
        while num < self.num_zombies():
            yield self._zombie_list[num]
            num += 1

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        num = 0
        while num < self.num_humans():
            yield self._human_list[num]
            num += 1
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        grid_height = self.get_grid_height()
        grid_width = self.get_grid_width()
        # Create a new grid visited of the same size as the original grid
        # initialize its cells to be empty.
        visited = poc_grid.Grid(grid_height, grid_width)
        visited.clear()
        # Create a 2D list distance_field of the same size as the original grid
        # initialize entries to be the product of the height times the width of the grid. 
        # (This value is larger than any possible distance.)
        distance_field = [[grid_width * grid_height] * grid_width for _row in range(grid_height)]
        # Create a queue boundary that is a copy of either the zombie list or the human list. 
        # For cells in the queue, initialize visited to be FULL and distance_field to be zero.
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for entity in self.zombies():
                boundary.enqueue(entity)
        else:
            for entity in self.humans():
                boundary.enqueue(entity)
#        print "boundary", boundary
        for entity in boundary:
            row = entity[0]
            col = entity[1]
            visited.set_full(row, col)
            distance_field[row][col] = 0
#            print "dist_field_row", distance_field[row]
        # implement breadth first search
        # For each neighbor_cell in the inner loop, check whether the cell has not been visited and is passable. 
        # If so, update the visited grid and the boundary queue as specified. 
        # In this case, also update the neighbor's distance to be the distance to current_cell plus one 
        # distance_field[current_cell[0]][current_cell[1]] + 1).
        while len(boundary) > 0: 
            curr_cell = boundary.dequeue()
#            print "curr_cell", curr_cell
#            print "start loop", boundary
            neighbours = self.four_neighbors(curr_cell[0], curr_cell[1])
            for neighbour in neighbours:
                row = neighbour[0]
                col = neighbour[1]
                # using one grid for visited, one grid for obstacles
                if visited.is_empty(row, col) and self.is_empty(row, col):
                    visited.set_full(row, col)
                    boundary.enqueue(neighbour)
                    # as long as there is one entity, the dist will be calculated from that inital dist of 0
                    # based on the entity in boundary loop above
                    distance_field[row][col] = distance_field[curr_cell[0]][curr_cell[1]] + 1
#                    print "dist_field_row_post", distance_field[row]
#            print "end loop", boundary         
    
        return distance_field
        
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        num = 0
        for human in self.humans():
            # only take moves that are not obstacles
            neighbours = [move for move in self.eight_neighbors(human[0], human[1]) if self.is_empty(move[0], move[1])]
            neighbours.append(human)  # in case max dist is staying still
            max_dist = max((zombie_distance_field[neighbour[0]][neighbour[1]] for neighbour in neighbours))
#            print "max_dist", max_dist
#            print "field", zombie_distance_field
            max_moves = [move for move in neighbours if zombie_distance_field[move[0]][move[1]] == max_dist]
            picked_move = random.choice(max_moves)  # pick randomly if >1 max move
#            print "max_moves", max_moves
            self._human_list[num] = picked_move
            num += 1
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        num = 0 
        for zombie in self.zombies():
            neighbours = [move for move in self.four_neighbors(zombie[0], zombie[1]) if self.is_empty(move[0], move[1])]
            neighbours.append(zombie)
            min_dist = min((human_distance_field[neighbour[0]][neighbour[1]] for neighbour in neighbours))
            min_moves = [move for move in neighbours if human_distance_field[move[0]][move[1]] == min_dist]
            picked_move = random.choice(min_moves)
            self._zombie_list[num] = picked_move
            num += 1

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))

