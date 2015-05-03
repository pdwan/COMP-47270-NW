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
    (1) degree distribution | degree sequence	***
    (2) assortativity cooefficient
    (3) clustering cooefficient
    
"""

import networkx as nx
import matplotlib.pyplot as plt		# plot cartesian graph (x-y) --> log(rank)-log(degree)
									# plot connected_component for same values as sub-graph
import numpy as np					# calculate slope using numpy

G = nx.gnp_random_graph(100, 0.02) 								# using sample graph to confirm implementation

# calculate degree sequence 
degree_sequence = sorted(nx.degree(G).values(),reverse = True) 	# degree sequence
print "Degree Sequence = \n", degree_sequence

dmax = max(degree_sequence)

# plot degree sequence 
plt.loglog(degree_sequence, 'b-', marker='o')
plt.title("Degree Rank Plot")
plt.ylabel("degree")
plt.xlabel("rank")

# calculate strongly connected component gcc & rank

gcc = sorted(nx.connected_component_subgraphs(G), key = len, reverse=True) [0]
pos = nx.spring_layout(gcc)

     # plot gcc & rank as sub-graph of cartesian

plt.axes([0.45, 0.45, 0.45, 0.45])
plt.axis('off')						# turn off x- and y- axes which would overwrite main graph
nx.draw_networkx_nodes(gcc, pos, node_size = 20)
nx.draw_networkx_nodes(gcc, pos, alpha = 0.4)

plt.savefig("degree_histogram.png")
plt.show()

raw_input("\nPress Enter to Continue ...\n")