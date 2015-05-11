import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import random

# PRICE MODEL

Nmax = 1000;

indegrees=np.zeros(Nmax, dtype=int);
outdegrees=np.zeros(Nmax, dtype=int);
edges = np.zeros(Nmax*10,dtype=int);


N=1;
M = 0;
sumindegrees = 0

# c = average size of a bibliography
c = 20  

# set a = c(alpha - 2)

alpha = 3
a = c*(alpha - 2);

phi = c *1.0/(c+a);

for N in range(1,Nmax):

# add a new node and generate its edges

    for j in range(N):
        x = random.uniform(0,1)
        if (sumindegrees>0.0):
            compare = phi*indegrees[j]*1.0/sumindegrees + (1 - phi)/N
        else:
            compare = 0.5/N;

        if ((sumindegrees==0) or x < compare):
            edges[M] = j
            outdegrees[N] += 1
            indegrees[j] = indegrees[j]+1
            M = M+1
            sumindegrees=sumindegrees+1

for j in range(N):
    print indegrees[j],
    print outdegrees[j]

k=0
for j in range(N):
    for i in range(outdegrees[j]):
        print edges[k],
        k = k+1
    print
