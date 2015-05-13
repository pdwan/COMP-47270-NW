#!/usr/bin/env python

"""
    Author          Paula Dwan
    Email           paula.dwan@gmail.com
    Student ID      13208660

    Module          COMP47270 (Computational Network Analysis and Modeling)
    Course          MSc ASE
    Due date        11-May-2015
    Lecturer 	    Dr. Neil Hurley

    CASE STUDY 2 :  Community Finding
                    Algorithm = Hierarchical Clustering --> create dendrogram
"""

from scipy.spatial import distance
from scipy.cluster import hierarchy
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import community as cmty
import os.path as osp
import cs2_functions as nxc
import logging

cs_ref = 'CS 2 : Hierarchical Clustering : '

# src_file = "../DataSets/test.txt"
# src_file = "../DataSets/social_facebook_combined.txt"
src_file = "../DataSets/p2p-Gnutella06.txt"
# src_file = "../DataSets/cit-HepTh.txt"
# src_file = "../DataSets/twitter_combined.txt"
# src_file = "../DataSets/gplus_combined.txt"
graph = nx.read_edgelist(path=str(src_file), delimiter='\t', create_using=nx.Graph(), comments='#', nodetype=int,
                         edgetype=int, data=True, encoding='utf-8')

def create_output_data_file():
    """
    create_output_data_file()
    create output data file using timestamp and name of data source file
    :return: df - destination file name
    """
    logging.info(cs_ref, 'create output data file')
    current_date = '%Y%m%d-%H%M%S'
    head, tail = osp.split(src_file)
    first_data = "OUTPUT DATA FILE for " + cs_ref + src_file
    df = 'data/%s_%s' % (datetime.now().strftime(current_date), tail)
    open(df, 'w').write(first_data)
    return df

def calc_best_partition(g):
    """
    calc_best_partition(g)
    calculate best partition using community in-built function.
    :param g:   source graph
    :return:    best_partition
    """
    logging.info(cs_ref, 'best partition')
    bp = cmty.best_partition(g)
    count = 0.
    for com in set(bp.values()):
        count += 1.
        list_nodes = [nodes for nodes in bp.keys() if bp[nodes] == com]
    nodes_info = "\tNodes in best partitioned Community[" + str(com) + "] = " + str(list_nodes)
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n" + nodes_info)
    print(nodes_info)
    return  bp

def calc_community_modularity(bp, g):
    """
    calc_community_modularity(bp,g)
    calculate modularity using community
    :param bp:  best partition
    :param g:   source graph
    :return:    ---
    """
    logging.info(cs_ref, 'modularity')
    modularity_info = "\tModularity : for best partition is : " + str(cmty.modularity(bp, g))
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n" + modularity_info)
    print (modularity_info)

def create_dendrogram(g):
    """
    create_dendrogram(g)
    create dendrogram (tree structure) from graph from lowest to highest level
    :param g:   source graph
    :return:    hier - hierarchy
    """
    logging.info(cs_ref, 'create graph')
    path_length = nx.all_pairs_shortest_path_length(g)
    n = len(g.nodes())
    distances = np.zeros((n, n))
    for u, p in path_length.iteritems():
        for v, d in p.iteritems():
            distances[int(u) - 1][int(v) - 1] = d
    sd = distance.squareform(distances)
    hier = hierarchy.average(sd)
    return hier


def plot_dendrogram(hier):
    """
    plot_dendrogram(hier)
    plot the resulting clusters using the hierarchy function dendrogram
    :param hier:    averaged linked clusters as previously calculated
    :return:        --
    """
    logging.info(cs_ref, 'plot graph dendrogram')
    hierarchy.dendrogram(hier, show_leaf_counts=True, truncate_mode='level', p=7, show_contracted=True)
    # hierarchy.dendrogram(hier)
    plt.title("Hierarchical Clustering - dendrogram " + src_file)
    plt.ylabel("Dissimilarity (Distance)")
    plt.xlabel("Node reference")
    plt.savefig("plots/hierarchical_clustering.png")
    plt.show()


if __name__ == '__main__':
    logging.info(cs_ref, 'start MAIN')
    dest_file = create_output_data_file()
    time_start = nxc.get_start_time()

    print '\nHIERARCHICAL CLUSTERING - dendrogram ...\n'
    hierarchy_dendrogram = create_dendrogram(graph)
    plot_dendrogram(hierarchy_dendrogram)

    print '\nHIERARCHICAL CLUSTERING - performance ...\n'
    partition = calc_best_partition(graph)
    calc_community_modularity(partition, graph)

    time_taken = nxc.show_time_taken(time_start)
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n"+time_taken)
    print(time_taken)

    logging.info(cs_ref, 'end MAIN')
    raw_input("Press Enter to Continue ...")