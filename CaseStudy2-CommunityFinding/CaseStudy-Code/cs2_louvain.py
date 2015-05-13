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
                    Algorithm = Louvain --> create dendrograms
"""
from collections import defaultdict

import networkx as nx
import matplotlib.pyplot as plt
import community as cmty
import cs2_functions as nxc
from datetime import datetime
import os.path as osp
import logging

cs_ref = 'CS 2 : Louvain : '

# src_file = "../DataSets/test.txt"
src_file = "../DataSets/social_facebook_combined.txt"
# src_file = "../DataSets/cit-HepTh.txt"
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
    logging.info(cs_ref, 'create graph')
    best_partition = cmty.best_partition(g)
    return best_partition


def calc_community_modularity(bp, g):
    """
    calc_community_modularity(bp,g)
    calculate modularity using community
    :param bp:  best partition
    :param g:   source graph
    :return:    ---
    """
    logging.info(cs_ref, 'modularity from Louvain')
    modularity_info = "\tModularity : for best partition is : " + str(cmty.modularity(bp, g))
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n" + modularity_info)
    print (modularity_info)


def describe_all_communities(g):
    """
    describe_all_communities(g)
    calculate all partitions using community in-built functions
    :param g:   source graph
    :return:    ---
    """
    logging.info(cs_ref, 'calculate all communities in graph')
    com_dict = {}
    com_values = defaultdict(list)

    for i in set(partition.values()):
        members = [nodes for nodes in partition.keys() if partition[nodes] == i]
        members_info = 'Community[' + str(i) + '] : ', members
        with open(dest_file, "a") as dat_file:
            dat_file.write("\n\t" + str(members_info))
        print "\t" + str(members_info)
        for com_ref, members in com_dict:
            com_values["community_{0}".format(i)].append(members)
    # return com_values


def describe_louvain_best_partitioned_community(bp, g):
    """
    describe_louvain_best_partitioned_community(bp, g)
    plot best partitioned community as calculated using community louvain method
    :param bp:
    :param g:
    :return:
    """
    logging.info(cs_ref, 'plot louvain graph for best partition')
    count = 0.
    for com in set(bp.values()):
        count += 1.
        list_nodes = [nodes for nodes in bp.keys() if bp[nodes] == com]
    nodes_info = "\tNodes in best partitioned Community[" + str(com) + "] = " + str(list_nodes)
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n" + nodes_info)
    print(nodes_info)
    # pos = nx.spring_layout(g)
    # nx.draw_networkx_nodes(g, pos, list_nodes, node_size=20, node_color='b')
    # plt.title("Louvain - best partition " + src_file)
    # plt.savefig("plots/louvain_graph.png")
    # plt.show()
    #
if __name__ == '__main__':
    dest_file = create_output_data_file()
    time_start = nxc.get_start_time()

    print '\nLOUVAIN - Best partition ...'
    partition = calc_best_partition(graph)
    describe_louvain_best_partitioned_community(partition, graph)

    print '\nLOUVAIN - modularity ...'
    calc_community_modularity(partition, graph)

    print '\nLOUVAIN - all communities ....'
    describe_all_communities(graph)

    print '\nLOUVAIN - Performance ...'
    time_taken = nxc.show_time_taken(time_start)
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n"+time_taken)
    print(time_taken)

    raw_input("Press Enter to Continue ...")