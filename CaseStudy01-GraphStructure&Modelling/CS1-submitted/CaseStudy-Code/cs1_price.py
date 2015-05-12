#!/usr/bin/python

"""
    Author          Paula Dwan
    Email           paula.dwan@gmail.com
    Student ID      13208660

    Module          COMP47270 (Computational Network Analysis and Modeling)
    Course          MSc ASE
    Due date        11-May-2015
    Lecturer 	    Dr. Neil Hurley

    CASE STUDY 1 :  Graph Structure & Modelling - Price's Model

"""

import networkx as nx
import matplotlib.pylab as plt
import numpy as np
import random
import logging
from datetime import datetime
import os.path as osp

import cs1_functions as fn

np.seterr(divide='ignore', invalid='ignore')

cs_ref = 'CS 1 : Price\'s Model : '     # used for logging only!

# src_file not used in PRice's Model calculation but only for reference in resulting plots, instead same number of nodes are used
# src_file = "../DataSets/social_facebook_combined.txt" ; n_max = 4039
src_file = "../DataSets/cit-HepPh.txt" ; n_max = 27770
# src_file = "../DataSets/cit-HepTh.txt" ; n_max = 34546
# src_file = "../DataSets/twitter_combined.txt" ; n_max = 81306
# src_file = "../DataSets/gplus_combined.txt" ; n_max = 107614
# graph = nx.read_edgelist(path=str(src_file), delimiter=' ', create_using=nx.DiGraph(), comments='#', nodetype=int, data=True, encoding='utf-8')

print ("source file is " + src_file)

def create_output_data_file():
    """
    create_output_data_file()
    create output data file using timestamp and name of data source file
    :return:
    """
    logging.info(cs_ref, 'create Output Data File')
    current_date = '%Y%m%d-%H%M%S'
    head, tail = osp.split(src_file)
    first_data = "OUTPUT DATA FILE for " + src_file
    df = 'data/%s_%s' % (datetime.now().strftime(current_date), tail)
    open(df, 'w').write(first_data)
    return df

def calc_prices_model(n, avg_biblio_size=20, alpha=3):
    """
    calc_prices_model(n, avg_biblio_size=20, alpha=3)
    calculate the edges for each node and add both nodes and edges to graph g
    :param n:
    :param avg_biblio_size: 20
    :param alpha:           3
    :return: graph - simulated directed graph
    """
    logging.info(cs_ref, 'calculate Price\'s Model')
    func_intro = "\nPrice\'s Model ... "
    print func_intro
    with open(dest_file, "a") as dat_file:
        dat_file.write(func_intro)

    if alpha <= 2:
        raise ValueError ('Power Law parameter alpha must be greater than 2')
        return 1

    in_degrees=np.zeros(n_max, dtype=int)
    out_degrees=np.zeros(n_max, dtype=int)
    edges = np.zeros(n_max*10, dtype=int)
    M = 0
    sum_in_degrees = 0
    g = nx.DiGraph()

    a = avg_biblio_size*(alpha - 2)
    phi = avg_biblio_size *1.0 / (avg_biblio_size + a)

    for n in range(1, n_max):                   # for each node in range 1 to n_max
        for j in range(n):                      # calculate in-degrees and out-degrees for each and add to edges.
            x = random.uniform(0, 1)
            if (sum_in_degrees > 0.0):
                compare = phi * in_degrees[j] * 1.0/sum_in_degrees + (1 - phi)/n
            else:
                compare = 0.5/n
            if ((sum_in_degrees == 0) or x < compare):
                edges[M] = j
                out_degrees[n] += 1
                in_degrees[j] += 1
                M += 1
                sum_in_degrees += 1
        with open(dest_file, "a") as dat_file:
            dat_file.write("\nNumber of IN-Degrees & OUT-Degrees Values for Node[*]...")
        j=0
        with open(dest_file, "a") as dat_file:
            dat_file.write("\n\tNode[*] \t|in-degrees| \t|out-degrees|\n")
        for j in range(n):
            with open(dest_file, "a") as dat_file:
                dat_file.write('\tNode[{0}] \t\t\t {1} \t\t\t\t{2}\n'.format(j, in_degrees[j], out_degrees[j]))
            print('\tNode[{0}] \t\t\t {1} \t\t\t\t{2}\n'.format(j, in_degrees[j], out_degrees[j]))
            g.add_node(j)
        k=0
        for j in range(n):
            for i in range(out_degrees[j]):
                g.add_edge(k, edges[k])
                k += 1
    return g

def draw_prices_model(g):
    """
    draw_prices_model(g)
    draw the Price's Model with labelled nodes, using the graph g as previously created.
    :param g:   graph as source
    :return:
    """
    logging.info(cs_ref, 'plot Price\'s Model')
    labels={}
    for i in range(g.number_of_nodes()):
        labels[i]=r'${0}$'.format(i)
    pos = nx.spring_layout(g)
    nx.draw_networkx_edges(g, pos, alpha=0.4, edge_color='k', width=1)
    nx.draw_networkx_nodes(g, pos, nodelist=g.nodes(), node_color='r')
    nx.draw_networkx_labels(g, pos, labels, font_size=10)
    plt.figure(1)
    plt.title("Prices Model" + src_file)
    plt.savefig("plots/cs1_prices_model.png")
    plt.show()

def calc_in_degrees_price(g):
    """
    calc_in_degrees_price(g)
    calculate slope for in_degrees for Price's Model
    :param g: graph used as source for in-degrees
    :return: in_slope : slope of nodes -v- in-degree of each
    """
    in_degrees = g.in_degree()
    in_values = sorted(set(in_degrees.values()))
    in_rank = [in_degrees.values().count(x) for x in in_values]
    x = in_values
    x.pop(0)
    y = in_rank
    y.pop(0)
    in_slope, in_intercept = np.polyfit(np.log(x), np.log(y), 1)
    return in_slope

def calc_out_degrees_price(g):
    """
    calc_in_degrees_price(g)
    calculate slope for in_degrees for Price's Model
    :param g: graph used as source for in-degrees
    :return: in_slope : slope of nodes -v- in-degree of each
    """
    out_degrees = g.in_degree()
    out_values = sorted(set(out_degrees.values()))
    out_rank = [out_degrees.values().count(x) for x in out_values]
    x = out_values
    x.pop(0)
    y = out_rank
    y.pop(0)
    out_slope, out_intercept = np.polyfit(np.log(x), np.log(y), 1)
    return out_slope

#   ############################################################################################
#   MAIN
#   ############################################################################################

if __name__ == '__main__':
    dest_file = create_output_data_file()
    graph = calc_prices_model(1, 20, 3)
    draw_prices_model(graph)
    in_degree_slope = calc_in_degrees_price(graph)
    out_degree_slope = calc_out_degrees_price(graph)

    summary_info_in = "\nSUMMARY : \nin_degrees = \n\t" + str(graph.in_degree())
    summary_info_out = "\nout_degrees = \n\t" + str(graph.out_degree())
    summary_slope_in = "\nSlope & Beta : \n\tIN-degree slope = " + str(in_degree_slope) + "\tBeta = " + str(in_degree_slope*-1)
    summary_slope_out = "\n\tOUT-degree slope = " + str(out_degree_slope) + "\tBeta = " + str(out_degree_slope*-1)
    print(summary_slope_in)
    print(summary_slope_out)

    with open(dest_file, "a") as dat_file:
        dat_file.write(summary_info_in)
        dat_file.write(summary_info_out)
        dat_file.write(summary_slope_in)
        dat_file.write(summary_slope_out)

    raw_input("Press Enter to Continue ...\n")        # basically - pause!