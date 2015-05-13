#!/usr/bin/python

"""

Author      	Paula Dwan
Email       	paula.dwan@gmail.com
Student ID  	13208660
Subject     	COMP47270 (Computational Network Analysis and Modeling)
Date        	Jan-2015
Lecturer 	Dr. Neil Hurley

LABORATORY | CASE STUDY 2 : laplacian.py
    
"""
# import the networkx network analysis package
import networkx as nx

# import the graphvisualisation package graphviz
from networkx import graphviz_layout
import pygraphviz

# import the plotting functionality from matplotlib
import matplotlib.pyplot as plt

#import Delaunay tesselation 
from scipy.spatial import Delaunay

# import kmeans
from scipy.cluster.vq import vq, kmeans, whiten

import numpy as np
import scipy as sp
import random

def placement():
    num_nodes = 100
    x = [random.random() for i in range(num_nodes)]
    y = [random.random() for i in range(num_nodes)]

    x = np.array(x)
    y = np.array(y)

    # Make a graph with num_nodes nodes and zero edges
    # Plot the nodes using x,y as the node positions

    G = nx.empty_graph(num_nodes)
    print "G.number_of_nodes() = ", G.number_of_nodes(), "\n"

    pos = dict()
    for i in range(num_nodes):
        pos[i] = x[i],y[i]


    plot_graph(G, pos, 1)

    # Now add some edges - use Delaunay tesselation to produce a planar graph. 
    # Delaunay tesselation covers the convex hull of a set of points with 
    # triangular simplices (in 2D)
    #
    # Aside : Paula 13-Jan-2015 
    #   planar graph - graph that can be plotted in 2-D with no overlaps.

    points = np.column_stack((x,y))
    dl = Delaunay(points)
    tri = dl.simplices

    edges = np.zeros((2, 6*len(tri)),dtype=int)
    data = np.ones(6*len(points))
    j=0
    for i in range(len(tri)):
        edges[0][j]=tri[i][0]
        edges[1][j]=tri[i][1]
        j = j+1
        edges[0][j]=tri[i][1]
        edges[1][j]=tri[i][0]
        j = j+1
        edges[0][j]=tri[i][0]
        edges[1][j]=tri[i][2];
        j = j+1
        edges[0][j]=tri[i][2]
        edges[1][j]=tri[i][0];
        j = j+1
        edges[0][j]=tri[i][1]
        edges[1][j]=tri[i][2]
        j=j+1
        edges[0][j]=tri[i][2]
        edges[1][j]=tri[i][1]
        j=j+1

    data=np.ones(6*len(tri))
    A = sp.sparse.csc_matrix((data,(edges[0,:],edges[1,:])))

    for i in range(A.nnz):
        A.data[i] = 1.0

    G = nx.to_networkx_graph(A)
    plot_graph(G,pos,2)

    # Use the eigenvectors of the normalised Laplacian to calculate placement positions
    # for the nodes in the graph

    #   eigen_pos holds the positions
    eigen_pos = dict()
    deg = A.sum(0)
    diags = np.array([0])
    D = sp.sparse.spdiags(deg,diags,A.shape[0],A.shape[1])  # diagonal matrix of degrees
    Dinv = sp.sparse.spdiags(1/deg,diags,A.shape[0],A.shape[1]) # inverse of 
    # Normalised laplacian : multiply by 1 / Deg previously 
    L = Dinv*(D - A)
    E, V = sp.sparse.linalg.eigs(L,3,None,100.0,'SM') # 100x100 martrix --> compress into 100 vector
    V = V.real

    for i in range(num_nodes):
        eigen_pos[i] = V[i,1].real,V[i,2].real

    # for n,nbrsdict in G.adjacency_iter():
    #     for nbr,eattr in nbrsdict.items(): 
    #         if 'weight' in eattr:
    #             print n,nbr,eattr['weight']

    plot_graph(G,eigen_pos,3)


    # Now let's see if the eigenvectors are good for clustering
    # Use k-means to cluster the points in the vector V

    features = np.column_stack((V[:,1], V[:,2]))
    print "cluster_nodes for e-vector values :-"
    cluster_nodes(G,features,pos,eigen_pos) 		# e-vectors

    # Finally, use the columns of A directly for clustering
    raw_input("Press Enter to Continue ...\n")

    print "cluster_nodes for Delaunay tesselation values :-"
    cluster_nodes(G,A.todense(),pos,eigen_pos) 	# Delaunay tesselationvalues

    raw_input("Press Enter to Continue ...\n")

def plot_graph(G,pos,fignum):

    label = dict()
    labelpos=dict()
    for i in range(G.number_of_nodes()):
        label[i] = i
        labelpos[i] = pos[i][0]+0.02, pos[i][1]+0.02


    fig=plt.figure(fignum,figsize=(8,8))
    fig.clf()
    nx.draw_networkx_nodes(G,
                            pos,
                            node_size=40,
                            hold=False,
                        )

    nx.draw_networkx_edges(G,pos, hold=True)
    nx.draw_networkx_labels(G,
                            labelpos,
                            label,
                            font_size=10,
                            hold=True,
                        )
    fig.show(1)

def cluster_nodes(G, feat, pos, eigen_pos):#
    book,distortion = kmeans(feat,3)
    codes,distortion = vq(feat, book)
    
    nodes = np.array(range(G.number_of_nodes()))
    W0 = nodes[codes==0].tolist()
    W1 = nodes[codes==1].tolist()
    W2 = nodes[codes==2].tolist()
    print "W0 = ", W0
    print "W1 = ", W1
    print "W2 = ", W2
    plt.figure(3) # position of nodes as per e-vectors
    nx.draw_networkx_nodes(G,
                           eigen_pos,
                           node_size=40,
                           hold=True,
                           nodelist=W0,
                           node_color='m'
                        )
    nx.draw_networkx_nodes(G,
                           eigen_pos,
                           node_size=40,
                           hold=True,
                           nodelist=W1,
                           node_color='b'
                        )
    plt.figure(2)	# positions of nodes per Delaney tesselation
    nx.draw_networkx_nodes(G,
                           pos,
                           node_size=40,
                           hold=True,
                           nodelist=W0,
                           node_color='m'
                        )
    nx.draw_networkx_nodes(G,
                           pos,
                           node_size=40,
                           hold=True,
                           nodelist=W1,
                           node_color='b'
                        )

if __name__ == '__main__':
    placement()