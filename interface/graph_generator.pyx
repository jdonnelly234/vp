# cython: language_level=3

from libc.stdlib cimport rand, srand
from libc.time cimport time
from libc.stdio cimport printf
import numpy as np
cimport numpy as cnp

# Initialize random seed
srand(time(NULL))

def generate_complete_graph(int num_nodes):
    cdef int i, j, weight
    cdef int num_edges = num_nodes * (num_nodes - 1) // 2
    edges = []
    weights = np.empty(num_edges, dtype=np.intc)
    
    # Generate edges and random weights
    k = 0
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            edges.append((i, j))
            weight = rand() % 10 + 1  # Generate weights [1, 10]
            weights[k] = weight
            k += 1
    
    # Combine nodes, edges, and weights into a graph representation
    E = {(start, end): weights[idx] for idx, (start, end) in enumerate(edges)}
    
    return range(num_nodes), edges, E
