"""

Author      	Paula Dwan
Email       	paula.dwan@gmail.com
Student ID  	13208660
Subject     	COMP47270 (Computational Network Analysis and Modeling)
Date        	12-Jan-2015
Lecturer 	Dr. Neil Hurley

LABORATORY 1 

Use NetworkX to compute the following for the chosen networks
    (1) degree distribution
    (2) assortativity cooefficient
    (3) clustering cooefficient
    
"""


import networkx as nx
import matplotlib.pyplot as plt

G = nx.gnp_random_graph(100, 0.02)

degree_sequence = sorted(nx.degree(G).values(),reverse = True) # degree sequence
print "Degree Sequence = \n", degree_sequence

dmax = max(degree_sequence)

plt.loglog(degree_sequence, 'b-', marker='o')
plt.title("Degree Rank Plot")
plt.ylabel("Degree")
plt.xlabel("Rank")

# draw graph in inset

plt.axes([0.45, 0.45, 0.45, 0.45])

Gcc = sorted(nx.connected_component_subgraphs(G), key = len, reverse=True) [0]
pos = nx.spring_layout(Gcc)
plt.axis('off')
nx.draw_networkx_nodes(Gcc, pos, node_size = 20)
nx.draw_networkx_nodes(Gcc, pos, alpha = 0.4)

plt.savefig("degree_histogram.png")
plt.show()

raw_input("\nPress Enter to Continue ...\n")