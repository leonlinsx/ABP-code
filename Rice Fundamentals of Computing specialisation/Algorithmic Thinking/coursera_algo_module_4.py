from collections import deque
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

print(compute_resilience(GRAPH0, [0, 1]))

