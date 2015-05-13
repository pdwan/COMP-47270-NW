#!/usr/bin/python

"""
    Author          Paula Dwan
    Email           paula.dwan@gmail.com
    Student ID      13208660

    Module          COMP47270 (Computational Network Analysis and Modeling)
    Course          MSc ASE
    Due date        20-April-2015
    Lecturer 	    Dr. Neil Hurley

    CASE STUDY 2 :  Community Finding - laplacian
    using simplified laplacian alogrithim as defined in networkx

"""
from random import random

import networkx as nx
import networkx.convert as cv
import numpy.linalg as lg
import matplotlib.pyplot as plt
import community as cmty
import numpy as np
import cs2_functions as nxc
from scipy.cluster.vq import vq, kmeans, whiten
from datetime import datetime
import os.path as osp
import logging

cs_ref = 'CS 2 : Laplacian & Kmeans : '

src_file = "../DataSets/test.txt"
# src_file = "../DataSets/social_facebook_combined.txt"
# src_file = "../DataSets/cit-HepTh.txt"
# src_file = "../DataSets/p2p-Gnutella06.txt"
# src_file = "../DataSets/cit-HepPh.txt"
# src_file = "../DataSets/twitter_combined.txt"
# src_file = "../DataSets/gplus_combined.txt"
graph = nx.read_edgelist(path=str(src_file), delimiter=' ', create_using=nx.Graph(), comments='#', nodetype=int,
                         edgetype=int, data=True, encoding='utf-8')


def create_output_data_file():
    """
    create_output_data_file()
    create output data file using timestamp and name of data source file
    :return: df - destination file name
    """
    logging.info(cs_ref, 'create Output Data File')
    current_date = '%Y%m%d-%H%M%S'
    head, tail = osp.split(src_file)
    first_data = "OUTPUT DATA FILE for " + src_file
    df = 'data/%s_%s' % (datetime.now().strftime(current_date), tail)
    open(df, 'w').write(first_data)
    return df


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

def calc_laplacian_matrix(g):
    """
    calc_laplacian_matrix(g)
    calculate directed Laplacian matrix of G = (V, E) (directed)
        L = D - A
    where A is the adjacency matrix and D is the diagonal matrix of node degrees..
    :param g:   graph for processing
    :return:    eigen_values
    """
    logging.info(cs_ref, 'laplacian_matrix')
    g2 = cv.convert_to_directed(g)
    laplacian = nx.normalized_laplacian_matrix(g)
    eigen_values= lg.eigvals(laplacian.A)
    eigen_info = "\tLaplacian : \n\tLargest eigen-value :" + str(max(eigen_values)) + "\n\tSmallest eigen-value : " \
                 + str(min(eigen_values))
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n" + eigen_info)
    print(eigen_info)
    return eigen_values

def plot_laplacian_histogram(e):
    logging.info(cs_ref, 'plot matrix as histogram')
    plt.hist(e, bins=100)
    plt.xlim(min(e), max(e) + 0.5)
    plt.title("Laplacian - histogram : " + src_file)
    plt.savefig("plots/laplacian_histogram.png")
    plt.show()


def calc_kmeans(g):
    """
    calc_kmeans(g)
    Use scipy.cluster.vq to calculate kmeans
    :param g:   graph to process
    :return:    ---
    """
    g_matrix= nx.to_numpy_matrix(g)
    g_array = np.asarray(g_matrix).reshape(-1)
    whitened = whiten(g_array)
    clusters = 3
    centroids,_ = kmeans(whitened, clusters)
    idx,_ = vq(g_array, centroids)
    plt.scatter(g_array[:,0], g_array[:,1], c=centroids)
    plt.title("KMeans: " + src_file)
    plt.show()


if __name__ == '__main__':
    logging.info(cs_ref, 'start MAIN')
    dest_file = create_output_data_file()
    time_start = nxc.get_start_time()
    print '\n{0} using {1} - calculations ...\n'.format(cs_ref, src_file)
    eigens = calc_laplacian_matrix(graph)
    # plot_laplacian_histogram(eigens)
    # calc_kmeans(graph)

    print '\n{0} using {1} - performance ...\n'.format(cs_ref, src_file)
    partition = calc_best_partition(graph)
    calc_community_modularity(partition, graph)

    time_taken = nxc.show_time_taken(time_start)
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n"+time_taken)
    print(time_taken)

    logging.info(cs_ref, 'end MAIN')
    raw_input("Press Enter to Continue ...")