#!/usr/bin/python

"""
    Author :     	Paula Dwan
    Email :      	paula.dwan@gmail.com
    Student ID : 	13208660

    Course :    	COMP-47270
    Module :        Computational Network Analysis and Modeling

    Due date        11-May-2015
    Lecturer :	    Dr. Neil Hurley

    CASE STUDY 1 :  Graph Structure & Modelling

    Use NetworkX to compute the following for chosen networks
        (1) degree distribution | degree sequence
        (2) assortativity co-efficient
        (3) clustering co-efficient
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
from math import floor
from datetime import datetime
import os.path as osp
import logging
import numpy as np

np.seterr(divide='ignore', invalid='ignore')

cs_ref = 'CS 1 : computations : '  # used for logging only!
# src_file = "../DataSets/test.txt"
# src_file = "../DataSets/social_facebook_combined.txt"
# src_file = "../DataSets/cit-HepTh.txt"
# src_file = "../DataSets/cit-HepPh.txt"
# src_file = "../DataSets/gplus_combined.txt"
# src_file = "../DataSets/twitter_combined.txt"
graph = nx.gnp_random_graph(100, 0.02)
# graph = nx.read_edgelist(path=str(src_file), delimiter=' ', create_using=nx.DiGraph(), comments='#', nodetype=int, data=True, encoding='utf-8')
# graph = nx.gnp_random_graph(100,0.02)
# print "\nGraph Source file = \t", src_file

def create_output_data_file():
    """
    create_output_data_file()
    create output data file using timestamp and name of data source file
    :return:    file for data results
    """
    logging.info(cs_ref, 'create Output Data File')
    current_date = '%Y%m%d-%H%M%S'
    head, tail = osp.split(src_file)
    first_data = "\nNX-COMPUTATIONS : OUTPUT DATA FILE for " + src_file
    df = 'data/%s_%s' % (datetime.now().strftime(current_date), tail)
    open(df, 'w').write(first_data)
    return df

def calc_degree_sequence(g, dest_file):
    """
    calc_degree_sequence(g)
    Calculate & plot the degree sequence of the graph g & writes data to the created data output file
    :param g:   graph as source
    :return:    --
    """
    func_intro = "\n\nDegree Sequence ... "
    logging.info(cs_ref, func_intro)
    print func_intro
    with open(dest_file, "a") as dat_file:
        dat_file.write(func_intro)

    degree_sequence = sorted(nx.degree(g).values(), reverse=True)
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n\tDegree Sequence = \t" + str(degree_sequence))

    plt.loglog(degree_sequence, 'g-', marker='o')
    plt.title("Degree Rank/Sequence" +src_file)
    plt.ylabel("degree")
    plt.xlabel("rank")
    gcc = sorted(nx.connected_component_subgraphs(g), key=len, reverse=True)[0]
    pos = nx.spring_layout(gcc)
    plt.axes([0.45, 0.45, 0.45, 0.45])
    plt.axis('off')
    nx.draw_networkx_nodes(gcc, pos, node_size=10)
    nx.draw_networkx_nodes(gcc, pos, alpha=0.4)
    plt.figure(1)
    plt.savefig("plots/cs1_degree_histogram.png")
    plt.show()

def calc_assortativity_coefficient(g, dest_file):
    """
    calc_assortativity_coefficient(g)
    Calculate & plot the assortativity coefficient of the graph g using inbuilt NetworkX functions,
    Writes data to the created data output file
    :param g:   graph as source
    :return:    ---
    """
    func_intro = "\n\nAssortativity Co-Efficient ..."
    logging.info(cs_ref, func_intro)
    print func_intro
    with open(dest_file, "a") as dat_file:
        dat_file.write(func_intro)

    dac = nx.degree_assortativity_coefficient(g)  # calculate assortativity coefficient
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n\tDegree Assortativity Co-efficient = \t" + str(dac))

    A = nx.to_scipy_sparse_matrix(g)  # plot assortativity coefficient
    plt.figure(2)
    plt.spy(A)
    plt.title("Assortativity Co-efficient" + src_file)
    plt.savefig("plots/cs1_assortativity_coefficient.png")
    plt.show()


def calc_clustering_coefficient(g, dest_file):
    """
    calc_clustering_coefficient(g)
    Calculate & plot clustering coefficient of the graph g and writes data to the created data output file
    :param g:   graph as source
    :return:    ---
    """
    func_intro = "\n\nClustering Co-Efficient ..."
    logging.info(cs_ref, func_intro)
    print func_intro
    with open(dest_file, "a") as dat_file:
        dat_file.write(func_intro)

    cce = nx.clustering(g)  # calculate clustering co-efficient
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n\tClustering Coefficients for nodes in graph = \t" + str(cce))
    average_cce = nx.average_clustering(g)
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n\tAverage Clustering Coefficient for graph = \t" + str(average_cce))

    for edge in g.edges():  # plot clustering co-efficient
        if floor(edge[0] / 5.) != floor(edge[1] / 5.):
            if random.random() < 0.95:
                g.remove_edge(edge[0], edge[1])
    plt.figure(3)
    fixed_pos = {1: (0, 0), 10: (1, 1), 30: (1, 0), 50: (0, 1)}
    pos = nx.spring_layout(g, fixed=fixed_pos.keys(), pos=fixed_pos)
    nx.draw_networkx(g, pos=pos)
    plt.title("Clustering Co-efficient" + src_file)
    plt.savefig("plots/cs1_clustering_coefficient.png")
    plt.show()

#   ####################################################################################################
#   main
#   ####################################################################################################
if __name__ == '__main__':
    dest_file = create_output_data_file()
    calc_degree_sequence(graph,dest_file)
    calc_assortativity_coefficient(graph,dest_file)
    calc_clustering_coefficient(graph,dest_file) # not defined for directed graphs
    raw_input("\nPress Enter to Continue ...\n")  # basically - pause for user confirmation!