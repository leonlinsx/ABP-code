"""
Cookie Clicker Simulator
greedy boss practice here http://www.codeskulptor.org/#user47_O1BWDU6cjF_2.py
http://www.codeskulptor.org/#user47_APEUIWbCSB_41.py
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
#SIM_TIME = 10000000000.0
SIM_TIME = 15
class ClickerState:
    """
    Simple class to keep track of the game state. Must track four things;
    
    The total number of cookies produced throughout the entire game init as 0.0
    The current number of cookies you have init as 0.0
    The current time (in seconds) of the game init as 0.0
    The current CPS init as 1.0
    """
    
    def __init__(self):
        self.total_cookies = 0.0
        self.curr_cookies = 0.0
        self.curr_time = 0.0
        self.curr_CPS = 1.0
        # (time, item, cost of item, total cookies)
        self.history_list = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        msg = "\nTime: " + str(self.curr_time) + "\n"
        msg += "Current Cookies: " + str(self.curr_cookies) + "\n"
        msg += "CPS: " + str(self.curr_CPS) + "\n"
        msg += "Total Cookies: " + str(self.total_cookies) + "\n"
        return msg
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self.curr_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self.curr_CPS
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return float(self.curr_time)
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        
        return list(self.history_list)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self.get_cookies():
            return 0.0
        else:
            time_until = (cookies - self.get_cookies()) / self.get_cps()
            time_until = float(math.ceil(time_until))

            return time_until
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            pass
        else:
            self.curr_time += time
            self.curr_cookies += time * self.get_cps()
            self.total_cookies += time * self.get_cps()
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        
        history_list is (time, item, cost of item, total cookies)
        """
        if cost > self.get_cookies():
            pass
        else:
            self.history_list.append((self.get_time(), item_name, cost, self.total_cookies))
            self.curr_cookies -= cost
            self.curr_CPS += additional_cps
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build_copy = build_info.clone()
    clicker = ClickerState()
    
    # loop through duration
    while clicker.get_time() <= duration:
        strat_chosen = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), 
                                (duration - clicker.get_time()), build_copy)
        if strat_chosen:
            strat_cost = build_copy.get_cost(strat_chosen)
        else:  # None means no more to buy
            break
        
        time_to_wait = clicker.time_until(strat_cost)

        # If you would have to wait past the duration of the simulation to purchase the item, 
        # you should end the simulation
        if clicker.get_time() + time_to_wait > duration:
            break
        else:    
            # wait, buy, and update
            clicker.wait(time_to_wait)
            
            # allow for multiple item purchases in one time step
            # need to remember to update cost as well
            while clicker.get_cookies() >= strat_cost:
                clicker.buy_item(strat_chosen, strat_cost, build_copy.get_cps(strat_chosen))
                build_copy.update_item(strat_chosen)
                strat_cost = build_copy.get_cost(strat_chosen)
        
    if clicker.get_time() <= duration:
        clicker.wait(duration - clicker.get_time())
    
    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    
    return none if not enough time left (same for all strategies)
    """
    budget = cookies + cps * time_left

    can_afford = [item for item in build_info.build_items() if build_info.get_cost(item) <= budget]
#    print "cheap", can_afford
    cheap_cost = float('inf')
    cheap_item = None
    for item in can_afford:
        if build_info.get_cost(item) < cheap_cost:
            cheap_cost = build_info.get_cost(item)
            cheap_item = item
            
    return cheap_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    budget = cookies + cps * time_left
    can_afford = [item for item in build_info.build_items() if build_info.get_cost(item) <= budget]
#    print "exp", can_afford
    exp_cost = 0
    exp_item = None
    for item in can_afford:
        if build_info.get_cost(item) > exp_cost:
            exp_cost = build_info.get_cost(item)
            exp_item = item
            
    return exp_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    budget = cookies + cps * time_left
    can_afford = [item for item in build_info.build_items() if build_info.get_cost(item) <= budget]
#    print "best", can_afford
    best_cost_per_cps = float('inf')
    best_item = None
    for item in can_afford:
        cost_per_cps = build_info.get_cost(item) / build_info.get_cps(item)
        if cost_per_cps < best_cost_per_cps:
            best_cost_per_cps = cost_per_cps
            best_item = item
            
    return best_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

#    history = state.get_history()
#    history = [(item[0], item[3]) for item in history]
#    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()

