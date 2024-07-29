from collections import deque
import urllib.request
import time
import math
import random 
import matplotlib.pyplot as plt 
# from plotly import graph_objects as go
# import numpy as np

GRAPH0 = {0: set([1]),
          1: set([0, 2]),
          2: set([1, 3]),
          3: set([2])}

GRAPH1 = {0: set([1, 2, 3, 4]),
          1: set([0, 2, 3, 4]),
          2: set([0, 1, 3, 4]),
          3: set([0, 1, 2, 4]),
          4: set([0, 1, 2, 3])}

GRAPH2 = {1: set([2, 4, 6, 8]),
          2: set([1, 3, 5, 7]),
          3: set([2, 4, 6, 8]),
          4: set([1, 3, 5, 7]),
          5: set([2, 4, 6, 8]),
          6: set([1, 3, 5, 7]),
          7: set([2, 4, 6, 8]),
          8: set([1, 3, 5, 7])}

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph ugraph and the node start_node
    and returns the set consisting of all nodes that are visited by 
    a breadth-first search that starts at start_node.

    args:
    ugraph: dict, keys are nodes and values are sets of nodes for undirected graph
    start_node: int, starting node for the search
    """
    queue = deque()
    visited = set([start_node])
    queue.append(start_node)

    while len(queue) > 0:
        current_node = queue.popleft()
        for neighbour in ugraph[current_node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)     
        
    return visited

def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of sets, 
    where each set consists of all the nodes (and nothing else) in a connected component, 
    and there is exactly one set in the list for each connected component in 
    ugraph and nothing else.

    args:
    ugraph: dict, keys are nodes and values are sets of nodes for undirected graph
    """
    remaining_nodes = list(ugraph.keys())
    connected_components = list()

    while len(remaining_nodes) > 0:
        node = remaining_nodes[0]
        node_connected_components = bfs_visited(ugraph, node)
        connected_components.append(node_connected_components)
        remaining_nodes = [ele for ele in remaining_nodes if ele not in list(node_connected_components)]

    return connected_components

def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph 
    and returns the size (an integer) of the largest connected component in ugraph
    """
    connected_components_list = cc_visited(ugraph)

    max_size = -1
    # get the largest set within the list
    for cc_set in connected_components_list:
        max_size = max(max_size, len(cc_set))

    return max_size

def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes attack_order 
    and iterates through the nodes in attack_order. 
    For each node in the list, the function removes the given node and its edges from the graph 
    and then computes the size of the largest connected component for the resulting graph. 
    
    The function should return a list whose k+1th entry is 
    the size of the largest connected component in the graph 
    after the removal of the first k nodes in attack_order. 
    
    The first entry (indexed by zero) is the size of the largest connected component in the original graph.
    """

    resilience_list = [largest_cc_size(ugraph)]

    for attack_node in attack_order:
        attack_node_neighbours = ugraph[attack_node]
        for neighbour in attack_node_neighbours:
            ugraph[neighbour].remove(attack_node)
        del ugraph[attack_node]

        resilience_size = max(largest_cc_size(ugraph), 0)

        resilience_list.append(resilience_size) 

    return resilience_list

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

def fast_targeted_order(ugraph):
    """
    faster implementation of targeted attack order on an undirected graph
    When it encounter a non-empty set, the nodes in this set must be of maximum degree. 
    The method then repeatedly chooses a node from this set, deletes that node from the graph, 
    and updates degree_sets appropriately.

    args:
    dict of undirected graph with nodes as keys and edges as values
    
    returns:
    ordered list of nodes in decreasing order of their degrees
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    # creates a list degree_sets whose kth element is the set of nodes of degree 𝑘
    degree_set = []
    for node in list(new_graph.keys()):
        degree_set.append(set([]))
    for node in list(new_graph.keys()):
        node_degree = len(new_graph[node])
        degree_set[node_degree].add(node)

    order = []
    # i = 0
    for node_set in reversed(degree_set):
        while len(node_set) > 0:
            random_node = random.choice(list(node_set))
            node_set.remove(random_node)
            neighbours = new_graph[random_node]
            for neighbour in neighbours:
                neighbour_degree = len(new_graph[neighbour])
                degree_set[neighbour_degree].remove(neighbour)
                degree_set[neighbour_degree - 1].add(neighbour)
            
            order.append(random_node)
            delete_node(new_graph, random_node)

    return order

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib.request.urlopen(graph_url)
    graph_text = graph_file.read().decode('utf-8')
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print(f"Loaded graph with {len(graph_lines)} nodes")
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def make_complete_graph(num_nodes):
    """
    makes complete graph with all nodes connected
    """
    complete_graph = {}
    if num_nodes <= 0:
        return complete_graph
    else:
        for node in range(num_nodes):
            node_list = set(range(num_nodes))
            node_list.remove(node)
            complete_graph[node] = node_list
        return complete_graph

def make_ER_graph(num_nodes, probability):
    """
    creates undirected ER graph with edges created with probability p

    args:    
    probability: value from 0 to 1 of how likely the edge will be created
    """
    complete_graph = {node: set() for node in range(num_nodes)}

    if num_nodes <= 0:
        return complete_graph
    else:
        for node in range(num_nodes):
            node_list = set(range(num_nodes))
            node_list.remove(node)

            for neighbour in node_list:
                rand_num = random.random()
                if rand_num <= probability:
                    complete_graph[node].add(neighbour)
                    complete_graph[neighbour].add(node)

        return complete_graph

def make_UPA_graph(connect_to_m_nodes, final_n_nodes):
    """
    Generate an undirected graph using the undirected version of 
    the DPA (Directed Preferential Attachment) algorithm.
    
    This algorithm starts with a complete graph of `connect_to_m_nodes` nodes.
    It then adds new nodes to the graph, one at a time, each connecting to 
    `connect_to_m_nodes` existing nodes selected with probability proportional 
    to their current degrees.

    Parameters:
    connect_to_m_nodes (int): The number of nodes to connect to initially.
                              This is also the number of neighbors each new node will connect to.
    final_n_nodes (int): The total number of nodes in the final graph.

    Returns:
    dict: A dictionary representing the adjacency list of the graph.
          Keys are node indices, and values are sets of nodes that the key node has directed edges to.
    
    """
    m_node_complete_graph = make_complete_graph(connect_to_m_nodes)
    
    upa_trial = UPATrial(connect_to_m_nodes)

    for i in range(connect_to_m_nodes, final_n_nodes):        
        nodes_to_add = upa_trial.run_trial(connect_to_m_nodes)
        m_node_complete_graph[i] = nodes_to_add
        for node in nodes_to_add:
            m_node_complete_graph[node].add(i)

    return m_node_complete_graph

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def count_edges_undirected(ugraph):
    """
    counts edges in an undirected graph, considering each edge once not twice
    """
    count_edge = 0

    for i in ugraph.keys():
        count_edge += len(ugraph[i])

    count_edge /= 2

    return count_edge

def random_order(graph):
    """
    takes a graph and returns a list of the nodes in the graph in some random order.
    """
    node_list = list(graph.keys())
    random.shuffle(node_list)

    return node_list

def plot_resilience(network_resilience, er_resilience, upa_resilience):

    # The number of nodes removed (x-axis)
    nodes_removed = list(range(len(network_resilience)))

    plt.figure(figsize=(10, 6))

    # Plot each resilience curve
    plt.plot(nodes_removed, network_resilience, label='Network Resilience', marker='o')
    plt.plot(nodes_removed, er_resilience, label='ER Resilience', marker='s')
    plt.plot(nodes_removed, upa_resilience, label='UPA Resilience', marker='^')

    # Adding labels and title
    plt.xlabel('Number of Nodes Removed')
    plt.ylabel('Size of Largest Connected Component')
    plt.title('Resilience of Networks Under Attack')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

def plot_times(m=5, n_values=range(10, 1000, 10)):
    targeted_times = []
    fast_targeted_times = []

    for n in n_values:
        graph = make_UPA_graph(m, n)

        start_time = time.time()
        targeted_order(graph)
        targeted_times.append(time.time() - start_time)

        start_time = time.time()
        fast_targeted_order(graph)
        fast_targeted_times.append(time.time() - start_time)

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, targeted_times, label='Targeted Order', marker='o')
    plt.plot(n_values, fast_targeted_times, label='Fast Targeted Order', marker='s')
    plt.xlabel('Number of Nodes (n)')
    plt.ylabel('Running Time (seconds)')
    plt.title('Running Time of Targeted Order Algorithms on UPA Graphs\n(Desktop Python)')
    plt.legend()
    plt.grid(True)
    plt.show()

example_network = load_graph(NETWORK_URL)
network_edges = count_edges_undirected(example_network)
network_nodes = len(example_network.keys())
print(f"loaded network has {network_edges} edges, {network_nodes} nodes, {network_edges / network_nodes} edges per node, {(network_edges / network_nodes) / network_nodes} probability of a given node's edge")

er_graph = make_ER_graph(network_nodes, ((network_edges / network_nodes) / network_nodes))
er_edges = count_edges_undirected(er_graph)
er_nodes = len(er_graph.keys())
print(f"er graph has {er_edges} edges and {er_nodes} nodes")

# print(f"new upa node has {network_edges / network_nodes} edges on average")
# print(f"implies {upa_start_nodes} nodes starting connected graph")
# above wasn't right

upa_graph = make_UPA_graph(2, network_nodes)
upa_edges = count_edges_undirected(upa_graph)
upa_nodes = len(upa_graph.keys())
print(f"upa graph has {upa_edges} edges and {upa_nodes} nodes")

# network_atk_order = random_order(example_network)
# er_atk_order = random_order(er_graph)
# upa_atk_order = random_order(upa_graph)

# network_resilience = compute_resilience(example_network, network_atk_order)
# er_resilience = compute_resilience(er_graph, er_atk_order)
# upa_resilience = compute_resilience(upa_graph, upa_atk_order)

# print('question 1 and 2')
# plot_resilience(network_resilience, er_resilience, upa_resilience)

# print('question 3')
# plot_times()

network_tgt_atk_order = fast_targeted_order(example_network)
er_tgt_atk_order = fast_targeted_order(er_graph)
upa_tgt_atk_order = fast_targeted_order(upa_graph)

network_tgt_resilience = compute_resilience(example_network, network_tgt_atk_order)
er_tgt_resilience = compute_resilience(er_graph, er_tgt_atk_order)
upa_tgt_resilience = compute_resilience(upa_graph, upa_tgt_atk_order)

plot_resilience(network_tgt_resilience, er_tgt_resilience, upa_tgt_resilience)