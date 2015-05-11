import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp


#G = nx.gnp_random_graph(1000,0.02)

G = nx.read_edgelist("../../Data/SNAP/facebook_combined.txt")

A = nx.to_scipy_sparse_matrix(G);
fig=plt.figure()
plt.spy(A)
fig.show()

r = nx.degree_assortativity_coefficient(G)

print("Degree Assortativity Coefficient = ", r)

n = nx.average_neighbor_degree(G)
k = nx.k_nearest_neighbors(G)




