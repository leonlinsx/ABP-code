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
    for point_idx, point in enumerate(cluster_list):
        for second_point_idx, second_point in enumerate(cluster_list):
            if point == second_point:
                pass
            else:
                new_dist_tuple = pair_distance(cluster_list, point_idx, second_point_idx)
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
        half_len_list = len_list // 2
        cluster_list_first_half = cluster_list[0:half_len_list]
        cluster_list_sec_half = cluster_list[half_len_list:]
        (dist_1, idx1_1, idx2_1) = fast_closest_pair(cluster_list_first_half)
        (dist_2, idx1_2, idx2_2) = fast_closest_pair(cluster_list_sec_half)

        if dist_1 < dist_2:
            (dist, idx1, idx2) = (dist_1, idx1_1, idx2_1)
        else:
            (dist, idx1, idx2) = (dist_2, idx1_2 + half_len_list, idx2_2 + half_len_list)
        mid_line = 0.5 * (cluster_list[half_len_list - 1].horiz_center() + cluster_list[half_len_list].horiz_center())
        (dist_3, idx1_3, idx2_3) = closest_pair_strip(cluster_list, mid_line, dist)
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
    
    return []


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
            
    return []
