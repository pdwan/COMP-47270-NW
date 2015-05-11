#!/usr/bin/python

"""
    Author          Paula Dwan
    Email           paula.dwan@gmail.com
    Student ID      13208660

    Module          COMP47270 (Computational Network Analysis and Modeling)
    Course          MSc ASE
    Due date        11-May-2015
    Lecturer 	    Dr. Neil Hurley

    CASE STUDY 1 :  Graph Structure & Modelling - Broder et al

"""

from __future__ import division
import random
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import os.path as osp
import logging

cs_ref = 'CS 1 : Broder et al : '
# src_file = "../DataSets/test.txt"
# src_file = "../DataSets/social_facebook_combined.txt"
# src_file = "../DataSets/twitter_combined.txt"
# src_file = "../DataSets/gplus_combined.txt"
src_file = "../DataSets/soc-Slashdot0902.txt"
graph = nx.read_edgelist(path=str(src_file), delimiter=' ', create_using=nx.DiGraph(), comments='#', nodetype=int, data=True, encoding='utf-8')
print "\nGraph Source file = \t", src_file                          # validate source file name

def create_output_data_file(g):
    """
    create_output_data_file(g)
    create output data file using timestamp and name of data source file
    :param g:   garaph as source
    :return:    data file
    """
    logging.info(cs_ref, 'create Output Data File')
    current_date = '%Y%m%d-%H%M%S'
    head, tail = osp.split(src_file)
    first_data = "\nNX-COMPUTATIONS : OUTPUT DATA FILE for " + src_file
    df = 'data/%s_%s' % (datetime.now().strftime(current_date), tail)
    open(df, 'w').write(first_data)
    return df

def calc_broder_values(g):
    """
    calc_broder_values(g)
    calculate values for Broder bow-tie : SCC, IN, OUT, IN-tendrils, OUT-tendrils, Tubes, Disconnected
    :param g:   graph as source
    :return:    ---
    """
    logging.info(cs_ref, 'calculate values for Broder bow-tie')
    func_intro = "\nCalculate Broder Bow-tie values ... \n"
    print func_intro
    with open(dest_file, "a") as dat_file:
        dat_file.write(func_intro)

    bt_dict = {}

    cc = nx.strongly_connected_components(g)
    lc = g.subgraph(cc.next())
    scc = set(lc.nodes())

    scc_node = random.sample(scc,1)[0]
    shortest_path = nx.all_pairs_shortest_path_length(g)
    inc = {n for n in g.nodes() if scc_node in shortest_path[n]}
    inc -= scc

    outc = set()
    for n in scc:
        outc |= set(shortest_path[n].keys())
    outc -= scc

    tubes = set()
    in_tendrils = set()
    out_tendrils = set()
    disconnected = set()
    remainder = set(g.nodes()) - scc - inc - outc

    inc_out = set()

    for n in scc:
        inc_out |= set(shortest_path[n].keys())
    inc_out = inc_out - scc - inc - outc

    for n in remainder:
        if n in inc_out:
            if set(shortest_path[n].keys()) & outc:
                tubes.add(n)
            else:
                in_tendrils.add(n)
        elif set(shortest_path[n].keys()) & outc:
            out_tendrils.add(n)
        else:
            disconnected.add(n)                     # all should have density = 0 (no connections)

    bt_dict.update({'IN-tendrils': in_tendrils})
    bt_dict.update({'IN': inc})
    bt_dict.update({'SCC': scc})
    bt_dict.update({'OUT': outc})
    bt_dict.update({'OUT-tendrils': out_tendrils})
    bt_dict.update({'Tubes': tubes})
    bt_dict.update({'Disconnected': disconnected})
    return bt_dict

def output_broder_values(bt_dict):
    """
    output_broder_values(bt_dict)
    output values obtained for Broder bow-tie to output data file
    :param bt_dict: broder dictionary of bow-tie values
    :return:        ---
    """
    logging.info(cs_ref, 'output values for Broder bow-tie')
    func_intro = "\nBRODER BOW-TIE VALUES ARE ... \n"
    print func_intro
    with open(dest_file, "a") as dat_file:
        dat_file.write(func_intro)

def draw_broder_bar_chart(bt_dict):
    """
    draw_broder_bar_chart(bt_dict)
    plot the values previously calculated for Broder as bar-chart
    :param bt_dict:
    :return:
    """
    logging.info(cs_ref, 'draw a bar-chart for each Broder bow-tie value')
    func_intro = "\nPLOT BAR-CHART of BRODER BOW-TIE VALUES ... \n"
    print func_intro
    with open(dest_file, "a") as dat_file:
        dat_file.write(func_intro)
    plt.figure(1)
    plt.title("Broder - compare Bow-tie values")
    plt.bar(range(len(bt_dict)), bt_dict.values(), align='center')
    plt.xticks(range(len(bt_dict)), bt_dict.keys())
    plt.show()

def draw_broder_pie_chart(bt_dict):
    """
    draw_broder_pie_chart(bt_dict)
    plot the % ratio of each previously calculated for Broder as pie-chart
    :param bt_dict:
    :return:
    """
    logging.info(cs_ref, 'draw a bar-chart for each Broder bow-tie value')
    func_intro = "\nPLOT BAR-CHART of BRODER BOW-TIE VALUES ... \n"
    print func_intro
    with open(dest_file, "a") as dat_file:
        dat_file.write(func_intro)

    labels = []
    values = []
    sizes = []
    for key, value in bt_dict.iteritems():
        labels.append(key)
        values.append(value)
    total = sum(values)
    for i in range(len(values)):
        sizes[i] = values[i]/total * 100
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'orange', 'lightcoral', 'green', 'yellow' ]
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.show()

#   #############################################################################################
#   MAIN
#   #############################################################################################
if __name__ == '__main__':
    dest_file = create_output_data_file(graph)
    bow_tie_dict = calc_broder_values(graph)
    output_broder_values(bow_tie_dict)
    draw_broder_pie_chart(bow_tie_dict)
    raw_input("Press Enter to Continue ...\n")        # basically - pause!