"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster
import random
import time 
import matplotlib.pyplot as plt  
# import alg_clusters_matplotlib

######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    
    (dist, idx1, idx2) = (float('inf'), -1, -1)
    for cluster_idx, cluster in enumerate(cluster_list):
        for second_cluster_idx, second_cluster in enumerate(cluster_list):
            if cluster == second_cluster:
                pass
            else:
                new_dist_tuple = pair_distance(cluster_list, cluster_idx, second_cluster_idx)
                if new_dist_tuple[0] < dist:
                    (dist, idx1, idx2) = new_dist_tuple

    return (dist, idx1, idx2)



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    # work on a copy (python 2 test suite) and ensure sorted
    cluster_list = cluster_list[:]
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    
    len_list = len(cluster_list)

    if len_list <= 3:
        (dist, idx1, idx2) = slow_closest_pair(cluster_list)
    else:
        # divide and conquer
        half_len_list = len_list // 2
        cluster_list_first_half = cluster_list[0:half_len_list]
        cluster_list_sec_half = cluster_list[half_len_list:]
        (dist_1, idx1_1, idx2_1) = fast_closest_pair(cluster_list_first_half)
        (dist_2, idx1_2, idx2_2) = fast_closest_pair(cluster_list_sec_half)
        # merge
        if dist_1 < dist_2:
            (dist, idx1, idx2) = (dist_1, idx1_1, idx2_1)
        else:
            (dist, idx1, idx2) = (dist_2, idx1_2 + half_len_list, idx2_2 + half_len_list)
        # check for mid line points
        mid_line = 0.5 * (cluster_list[half_len_list - 1].horiz_center() + cluster_list[half_len_list].horiz_center())
        (dist_3, idx1_3, idx2_3) = closest_pair_strip(cluster_list, mid_line, dist)
        # merge
        if dist_3 < dist:
            (dist, idx1, idx2) = (dist_3, idx1_3, idx2_3)

    return (dist, idx1, idx2)


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    within_strip_indexes = []
    
    cluster_list = cluster_list[:]

    # cluster_list.sort(key = lambda cluster: cluster.vert_center())
    
    for index, cluster in enumerate(cluster_list):
        if abs(cluster.horiz_center() - horiz_center) < half_width:
            within_strip_indexes.append(index)
    
    # sort the new indexes list based on cluster list vert_center ascending order's index
    within_strip_indexes.sort(key=lambda idx: cluster_list[idx].vert_center())

    indexes_len = len(within_strip_indexes)
    (dist, idx1, idx2) = (float('inf'), -1, -1)
    
    for i in range(indexes_len - 1):
        for j in range(i + 1, min((i + 3), indexes_len - 1) + 1):
            (dist_ij, idx_i, idx_j) = pair_distance(cluster_list, within_strip_indexes[i], within_strip_indexes[j])
            if dist_ij < dist:
                (dist, idx1, idx2) = (dist_ij, idx_i, idx_j)

    return (dist, idx1, idx2)
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        (dist, cluster_1_idx, cluster_2_idx) = fast_closest_pair(cluster_list)
        
        # this mutates the cluster in place
        cluster_list[cluster_1_idx].merge_clusters(cluster_list[cluster_2_idx])
        del cluster_list[cluster_2_idx]

    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Initialize old cluster using large population counties 
    For number of iterations 
        Initialize the new clusters to be empty 
        For each county 
            Find the old cluster center that is closest 
            Add the county to the corresponding new cluster 
        Set old clusters equal to new clusters 
    Return the new clusters

    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    len_list = len(cluster_list)
    cluster_list = cluster_list[:]
    cluster_list.sort(key = lambda cluster: cluster.total_population(), reverse=True)
    # position initial clusters at the location of clusters with largest populations
    k_centers = cluster_list[:num_clusters]

    for _ in range(num_iterations):
        # initialise k empty sets for the clustering
        cluster_sets = [alg_cluster.Cluster(set([]), 0, 0, 0, 0) for _ in range(num_clusters)]
        for idx in range(len_list):
            # find the index of the closest cluster in cluster_sets, to the clusters in cluster_list
            min_dist = float('inf')
            cluster_set_idx = 0
            for k_idx, cluster in enumerate(k_centers):
                dist = cluster.distance(cluster_list[idx])
                if dist < min_dist:
                    min_dist = dist 
                    cluster_set_idx = k_idx
            # this mutates the cluster in place
            cluster_sets[cluster_set_idx].merge_clusters(cluster_list[idx])
        # update k_centers outside of the loop
        for idx in range(num_clusters):
            k_centers[idx] = cluster_sets[idx]

    return cluster_sets

def gen_random_clusters(num_clusters):
    """
    creates a list of clusters where each cluster in this list corresponds to 
    one randomly generated point in the square with corners (±1,±1)
    """
    cluster_list = []

    for _ in range(num_clusters):
        (x_coord, y_coord) = (random.random(), random.random())
        cluster_list.append(alg_cluster.Cluster(set([]), x_coord, y_coord, 0, 0))

    return cluster_list

def plot_times(n_values=range(2, 201)):
    slow_times = []
    fast_times = []

    for n in n_values:
        cluster_list = gen_random_clusters(n)

        start_time = time.time()
        slow_closest_pair(cluster_list)
        slow_times.append(time.time() - start_time)

        start_time = time.time()
        fast_closest_pair(cluster_list)
        fast_times.append(time.time() - start_time)

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, fast_times, label='Slow closest pair', marker='o')
    plt.plot(n_values, slow_times, label='Fast closest pair', marker='s')
    plt.xlabel('Number of clusters (n)')
    plt.ylabel('Running Time (seconds)')
    plt.title('Running Time of closest pair algos\n(Desktop Python)')
    plt.legend()
    plt.grid(True)
    plt.show()

def compute_distortion(cluster_list, data_table):
    """
    takes a list of clusters and uses cluster_error to compute its distortion
    data_table is the original table of cancer data used in creating the cluster
    """
    total_error = 0
    for cluster in cluster_list:
        total_error += cluster.cluster_error(data_table)

    return total_error

# question 1
# plot_times()

