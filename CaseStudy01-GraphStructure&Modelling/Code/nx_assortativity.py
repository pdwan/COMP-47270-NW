#!/usr/bin/python

"""
Author      	Paula Dwan
Email       	paula.dwan@gmail.com
Student ID  	13208660
Subject     	COMP47270 (Computational Network Analysis and Modeling)
Date        	Jan-2015
Lecturer 	Dr. Neil Hurley

LABORATORY 1 

Use NetworkX to compute the following for the chosen networks
    (1) degree distribution | degree sequence 
    (2) assortativity cooefficient  				***
    (3) clustering cooefficient
    
"""

import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp

G = nx.read_edgelist("../../DataSets/social_facebook_combined.txt")

A = nx.to_scipy_sparse_matrix(G);
fig = plt.figure()
plt.spy(A)
fig.show()

"""
degree_assortativity_coefficient
     Compute degree assortativity of graph.
     Assortativity measures the similarity of connections in the graph with respect to the node degree.
"""
r = nx.degree_assortativity_coefficient(G)
print "Degree assortativity Co-efficient = ", r

"""
degree_pearson_correlation_coefficient
     Compute degree assortativity of graph.
     Assortativity measures the similarity of connections in the graph with respect to the node degree.
     This is the same as degree_assortativity_coefficient but uses the potentially faster scipy.stats.pearsonr function.
"""
rp = nx.degree_pearson_correlation_coefficient(G)
print "Pearson's Degree assortativity Co-efficient = ", rp

"""
average_neighbor_degree
     Returns the average degree of the neighborhood of each node.
"""
n = nx.average_neighbor_degree(G)
print "\nAverage Neighbor Degree = \n", n

"""
k_nearest_neighbors
     Compute the average degree connectivity of graph.
     The average degree connectivity is the average nearest neighbor degree of nodes with degree k. 
"""
k = nx.k_nearest_neighbors(G)
print "\nK Nearest Neighbors = \n", k

raw_input("\nPress Enter to Continue ...\n")

