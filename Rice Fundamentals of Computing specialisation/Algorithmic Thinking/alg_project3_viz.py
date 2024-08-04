"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import random
import urllib.request
import alg_cluster
import matplotlib.pyplot as plt  

# conditional imports
if DESKTOP:
    import coursera_algo_project_3      # desktop project solution
    import alg_clusters_matplotlib
# else:
    #import userXX_XXXXXXXX as alg_project3_solution   # CodeSkulptor project solution
    # import alg_clusters_simplegui
    # import codeskulptor
    # codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib.request.urlopen(data_url)
    data = data_file.read().decode('utf-8')
    data_lines = data.split('\n')
    print("Loaded", len(data_lines), "data points")
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_3108_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    # cluster_list = sequential_clustering(singleton_list, 15)	
    # print("Displaying", len(cluster_list), "sequential clusters")

    # question 2 
    # cluster_list = coursera_algo_project_3.hierarchical_clustering(singleton_list, 15)
    # print("Displaying", len(cluster_list), "hierarchical clusters")

    # question 3 
    cluster_list = coursera_algo_project_3.kmeans_clustering(singleton_list, 15, 5)	
    print("Displaying", len(cluster_list), "k-means clusters")

            
    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
        #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    # else:
        # alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers

def run_example_2():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_111_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    # cluster_list = sequential_clustering(singleton_list, 15)	
    # print("Displaying", len(cluster_list), "sequential clusters")

    # question 5 
    cluster_list = coursera_algo_project_3.hierarchical_clustering(singleton_list, 9)
    distortion = coursera_algo_project_3.compute_distortion(cluster_list, data_table)
    print("Displaying", len(cluster_list), "hierarchical clusters")
    print(f"Distortion is {distortion}")

    # question 6 
    # cluster_list = coursera_algo_project_3.kmeans_clustering(singleton_list, 9, 5)	
    # distortion = coursera_algo_project_3.compute_distortion(cluster_list, data_table)
    # print("Displaying", len(cluster_list), "k-means clusters")
    # print(f"Distortion is {distortion}")

            
    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
        #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    # else:
        # alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers

def run_example_3(data_table_url):
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(data_table_url)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    # question 10        
    hierarchical_distortions = []
    kmeans_distortions = []

    # calc kmeans first since hierarchical mutates the list and i'm lazy to change code
    for num_cluster in range(20, 5, -1): 
        kmeans_cluster_list = coursera_algo_project_3.kmeans_clustering(singleton_list, num_cluster, 5)	
        kmeans_distortion = coursera_algo_project_3.compute_distortion(kmeans_cluster_list, data_table)
        kmeans_distortions.append(kmeans_distortion)

    # To compute the distortion for all 15 output clusterings produced by hierarchical_clustering
    # you should remember that you can use the hierarchical cluster of size 20 
    # to compute the hierarchical clustering of size 19 and so on
    cluster_list = coursera_algo_project_3.hierarchical_clustering(singleton_list, 20)

    for num_cluster in range(20, 5, -1): 
        cluster_list = coursera_algo_project_3.hierarchical_clustering(cluster_list, num_cluster)
        distortion = coursera_algo_project_3.compute_distortion(cluster_list, data_table)
        hierarchical_distortions.append(distortion)

    # print(hierarchical_distortions)
    # print(kmeans_distortions)

    # plot distortion vs number of clusters comparison
    plt.figure(figsize=(10, 6))
    plt.plot(range(20, 5, -1), hierarchical_distortions, label='hierarchical', marker='o')
    plt.plot(range(20, 5, -1), kmeans_distortions, label='kmeans', marker='s')
    plt.xlabel('Number of clusters (n)')
    plt.ylabel('Distortion')
    plt.title('Distortion of closest pair algos\n(Desktop Python)')
    plt.legend()
    plt.grid(True)
    plt.show()

# question 3 and 4
# run_example()

# question 5 and 6
# run_example_2()

# question 10
run_example_3(DATA_111_URL)
run_example_3(DATA_290_URL)
run_example_3(DATA_896_URL)




    





  
        






        




