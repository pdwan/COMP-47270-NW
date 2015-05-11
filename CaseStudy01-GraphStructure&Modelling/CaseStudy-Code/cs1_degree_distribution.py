#!/usr/bin/python

"""
    Author          Paula Dwan
    Email           paula.dwan@gmail.com
    Student ID      13208660

    Module          COMP47270 (Computational Network Analysis and Modeling)
    Course          MSc ASE
    Due date        11-May-2015
    Lecturer 	    Dr. Neil Hurley

    CASE STUDY 1 :  Graph Structure & Modelling - Degree Distribution

"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import os.path as osp
import logging
import numpy as np

np.seterr(divide='ignore', invalid='ignore')

cs_ref = "CS 1 - degree distribution: "
# src_file = "../DataSets/test.txt"
# src_file = "../DataSets/social_facebook_combined.txt"
# src_file = "../DataSets/twitter_combined.txt"
src_file = "../DataSets/gplus_combined.txt"
graph = nx.read_edgelist(path=str(src_file), delimiter=' ', create_using=nx.DiGraph(), comments='#', nodetype=int, data=True, encoding='utf-8')
print cs_ref + "\nGraph Source file = \t", src_file     # validate source file name

def create_output_data_file(g):
    """
    create_output_data_file(g)
    create output data file using timestamp and name of data source file
    :param g:   graph as source name for output file
    :return:    data file
    """
    logging.info(cs_ref, 'create Output Data File')
    current_date = '%Y%m%d-%H%M%S'
    head, tail = osp.split(src_file)
    first_data = "CS 1 - DEGREE DISTRIBUTION : OUTPUT DATA FILE for " + src_file
    df = 'data/%s_%s' % (datetime.now().strftime(current_date), tail)
    open(df, 'w').write(first_data)
    return df

def calc_degree_distribution(g, dest_file):
    """
    calc_degree_distribution(graph)
    calculate and plot in-degree and out-degree for specified graph
    :param g:   graph as source
    :return:    --
    """
    func_intro = "\n\nDegree distribution ... "
    logging.info(cs_ref, func_intro)
    print func_intro
    with open(dest_file, "a") as dat_file:
        dat_file.write(func_intro)
    in_degrees = g.in_degree()
    in_values = sorted(set(in_degrees.values()))
    in_rank = [in_degrees.values().count(x) for x in in_values]
    xi = in_values
    xi.pop(0)
    yi = in_rank
    yi.pop(0)
    in_slope, in_intercept = np.polyfit(np.log(xi), np.log(yi), 1)

    out_degrees = g.out_degree()
    out_values = sorted(set(out_degrees.values()))
    out_rank = [out_degrees.values().count(x) for x in out_values]
    xo = out_values
    xo.pop(0)
    yo = out_rank
    yo.pop(0)
    out_slope, out_intercept = np.polyfit(np.log(xo), np.log(yo), 1)

    str_nodes = ', '.join(str(e) for e in g.nodes())
    str_in_values = ', '.join(str(e) for e in in_values)
    str_in_rank = ', '.join(str(e) for e in in_rank)
    str_out_values = ', '.join(str(e) for e in out_values)
    str_out_rank = ', '.join(str(e) for e in out_rank)
    with open(dest_file, "a") as dat_file:
        dat_file.write("\n\nNodes = " + str_nodes)
        dat_file.write("\n\nIn-degrees : \n\tin_values = \t" + str_in_values + "\n\tin_rank = \t" + str_in_rank + "\n\tSlope = \t\t" + str(in_slope) + "\n\tBeta = \t\t" + str(in_slope*-1.))
        dat_file.write("\n\nOut-degrees : \n\tout_values = \t" + str_out_values + "\n\tout_rank = \t\t" + str_out_rank+ "\n\tSlope = \t\t\t" + str(out_slope) + "\n\tBeta = \t\t\t" + str(out_slope*-1.))

    plt.figure()
    plt.loglog(out_values, out_rank, 'bo-')
    plt.loglog(in_values, in_rank,'ro-')
    plt.legend(['In-degree', 'Out-degree'])
    plt.title('Power law -' + src_file)
    plt.ylabel('log(degree)')
    plt.xlabel('log(rank)')
    # plt.xlim([0, 2*10**3])
    plt.savefig('plots/cs1_power_law.png')
    plt.close()

#   #############################################################################################
#   MAIN
#   #############################################################################################
if __name__ == '__main__':
    dest_file = create_output_data_file(graph)
    calc_degree_distribution(graph, dest_file)
    raw_input("Press Enter to Continue ...\n")        # basically - pause!