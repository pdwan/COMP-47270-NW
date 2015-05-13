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
                    Algorithm = Laplacian using eigen-vectors and k-means, with defined number of nodes to match
                    dataset sizes as used. So we have :
                    num_nodes   = 4039  --> Facebook
                    num_nodes   = 27770 --> cit-HepTh
                    num_nodes   = 34546 --> cit-HepPh
                    num_nodes   = 81306 --> Twitter
                    num_nodes   = 107614 --> Google +
"""

import networkx as nx
import matplotlib.pyplot as plt
import cs2_functions as nxc
from scipy.spatial import Delaunay
from scipy.cluster.vq import vq, kmeans
from datetime import datetime
import os.path as osp
import numpy as np
import scipy as sp
import random
import logging

cs_ref = 'CS 2 : Laplacian Amended : '

src_file = "../equiv-social_facebook_combined.txt" ; num_nodes = 50

# src_file = "../equiv-cit-HepTh.txt" ; num_nodes = 27770
# src_file = "../equiv-cit-HepPh.txt" ; num_nodes = 34546
# src_file = "../equiv-twitter_combined.txt" ; num_nodes = 81306
# src_file = "../equiv-gplus_combined.txt" ; num_nodes = 107614

def create_output_data_file():
    """
    create_output_data_file()
    create output data file using timestamp and name of data source file
    :return: df - destination file name
    """
    logging.info(cs_ref, 'create output data file')
    print(cs_ref, 'create output data file')
    current_date = '%Y%m%d-%H%M%S'
    head, tail = osp.split(src_file)
    first_data = "OUTPUT DATA FILE for " + cs_ref + src_file
    df = 'data/%s_%s' % (datetime.now().strftime(current_date), tail)
    open(df, 'w').write(first_data)
    return df

def placement():
    """
    placement()
    :return:
    """
    x = [random.random() for i in range(num_nodes)]
    y = [random.random() for i in range(num_nodes)]
    x = np.array(x)
    y = np.array(y)

    G = nx.empty_graph(
        num_nodes)
    print "graph.number_of_nodes() = ", G.number_of_nodes()
    pos = dict()
    for i in range(num_nodes):
        pos[i] = x[i], y[i]
    # plot_graph(G, pos, 10)

    points = np.column_stack((x, y))
    dl = Delaunay(points)
    tri = dl.simplices
    edges = np.zeros((2, 6 * len(tri)), dtype=int)
    data = np.ones(6 * len(points))
    j = 0
    for i in range(len(tri)):
        edges[0][j] = tri[i][0]
        edges[1][j] = tri[i][1]
        j += 1
        edges[0][j] = tri[i][1]
        edges[1][j] = tri[i][0]
        j += 1
        edges[0][j] = tri[i][0]
        edges[1][j] = tri[i][2]
        j += 1
        edges[0][j] = tri[i][2]
        edges[1][j] = tri[i][0]
        j += 1
        edges[0][j] = tri[i][1]
        edges[1][j] = tri[i][2]
        j += 1
        edges[0][j] = tri[i][2]
        edges[1][j] = tri[i][1]
        j += 1
    data = np.ones(6 * len(tri))
    A = sp.sparse.csc_matrix((data, (edges[0, :], edges[1, :])))
    for i in range(A.nnz):
        A.data[i] = 1.0
    G = nx.to_networkx_graph(A)
    # plot_graph(G, pos, 20)

    eigen_pos = dict()
    deg = A.sum(0)
    diags = np.array([0])
    D = sp.sparse.spdiags(deg, diags, A.shape[0], A.shape[1])  # diagonal matrix of degrees
    Dinv = sp.sparse.spdiags(1 / deg, diags, A.shape[0], A.shape[1])
    L = Dinv * (D - A)
    E, V = sp.sparse.linalg.eigs(L, 3, None, float(num_nodes), 'SM')
    V = V.real

    for i in range(num_nodes):
        eigen_pos[i] = V[i, 1].real, V[i, 2].real
    print("plot_graph(G, eigen_pos, 3)")
    plot_graph(G, eigen_pos, 9)
    features = np.column_stack((V[:, 1], V[:, 2]))
    cluster_nodes(G, features, pos, eigen_pos)

    raw_input("Press Enter to Continue ...")

    cluster_nodes(G, A.todense(), pos, eigen_pos)
    raw_input("Press Enter to Continue ...")


def plot_graph(G, pos, fignum):
    """
    plot_graph(G, pos, fignum)
    :param G:       graph to plot
    :param pos:     pos for graph tp plot
    :param fignum:  reference for figure when plotted
    :return:
    """
    label = dict()
    labelpos = dict()
    for i in range(G.number_of_nodes()):
        label[i] = i
        labelpos[i] = pos[i][0] + 0.02, pos[i][1] + 0.02
    plt.clf()
    plt.figure(fignum, figsize=(10,10))
    nx.draw_networkx_nodes(G, pos, node_size=40, hold=False, )
    nx.draw_networkx_edges(G, pos, hold=True)
    nx.draw_networkx_labels(G, labelpos, label, font_size=10, hold=True, )
    plt.savefig(str(fignum)+"laplacian_amended.png")
    plt.show()

def cluster_nodes(G, feat, pos, eigen_pos):
    '''
    cluster the nodes in the graph as specified by num_cluster, note num_clusters must match
    :param G:
    :param feat:
    :param pos:
    :param eigen_pos:
    :return:
    '''
    num_clusters=3
    book, distortion = kmeans(feat, num_clusters)
    codes, distortion = vq(feat, book)

    nodes = np.array(range(G.number_of_nodes()))
    cluster0 = nodes[codes == 0].tolist()
    cluster1 = nodes[codes == 1].tolist()
    cluster2 = nodes[codes == 2].tolist()
    print "\tW0 = \t", cluster0
    print "\tW1 = \t", cluster1
    print "\tW2 = \t", cluster2

    plt.figure(333) # positions of nodes per eigen
    plt.title("Eigen")
    nx.draw_networkx_nodes(G, eigen_pos, node_size=40, hold=True, nodelist=cluster0, node_color='m')
    nx.draw_networkx_nodes(G, eigen_pos, node_size=40, hold=True, nodelist=cluster1, node_color='b')
    nx.draw_networkx_nodes(G, eigen_pos, node_size=40, hold=True, nodelist=cluster2, node_color='g')
    plt.show()

    plt.figure(999)   # positions of nodes per Delaney tesselation
    plt.title("Delaney")
    nx.draw_networkx_nodes(G, pos, node_size=40, hold=True, nodelist=cluster0, node_color='m')
    nx.draw_networkx_nodes(G, pos, node_size=40, hold=True, nodelist=cluster1, node_color='b')
    nx.draw_networkx_nodes(G, pos, node_size=40, hold=True, nodelist=cluster2, node_color='g')
    plt.show()


if __name__ == '__main__':
    time_start = nxc.get_start_time()
    placement()
    time_taken = nxc.show_time_taken(time_start)
    print(time_taken)
