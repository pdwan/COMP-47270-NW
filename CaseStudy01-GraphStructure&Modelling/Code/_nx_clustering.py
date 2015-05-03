#!/usr/bin/python

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
import scipy as sp

src_file = "../../DataSets/social_twitter_combined.txt"
# src_file = "../../DataSets/social_facebook_combined.txt"
# src_file = "../../DataSets/social_gplus_combined.txt" not working also
# src_file = "../../DataSets/amazon_finefoods.txt" 
"""
ERROR : 
     Traceback (most recent call last):
	  File "nx_clustering.py", line 27, in <module>
	       G = nx.read_edgelist(src_file)
	  File "<string>", line 2, in read_edgelist
	  File "/usr/local/lib/python2.7/dist-packages/networkx-1.9.1-py2.7.egg/networkx/utils/decorators.py", line 220, in _open_file
	       result = func(*new_args, **kwargs)
	  File "/usr/local/lib/python2.7/dist-packages/networkx-1.9.1-py2.7.egg/networkx/readwrite/edgelist.py", line 369, in read_edgelist
	       data=data)
	  File "/usr/local/lib/python2.7/dist-packages/networkx-1.9.1-py2.7.egg/networkx/readwrite/edgelist.py", line 280, in parse_edgelist
	       "Failed to convert edge data (%s) to dictionary."%(d))
     TypeError: Failed to convert edge data ([u'Quality', u'Dog', u'Food']) to dictionary.
"""
G = nx.read_edgelist(src_file)

print "\nGraph Source file = \n", src_file 

cce = nx.clustering(G)
print "\nClustering Coefficients for nodes in graph = \n", cce

average_cce = nx.average_clustering(G)
print "\nAverage Clustering Coefficient for graph = ", average_cce

A = nx.to_scipy_sparse_matrix(G)
fig = plt.figure()
plt.spy(A)
fig.show()

raw_input("\nPress Enter to Continue ...\n")
