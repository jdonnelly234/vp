#####################################################################################
# Implementation for Prim's algorithm MST based on PLK Chapter 8 - Graph Algorithms #
#####################################################################################


def prim_minimum_spanning_tree(graph):
    V, E, W = graph
    Te = set()  # Set of edges in the minimum spanning tree
    Tv = set()  # Set of visited vertices
    u = next(iter(V))  # Starting vertex, choosing any vertex in V
    L = {}      # Dictionary for L values of each edge

    Tv.add(u)           #Adding initial vertex to Tv

    # Initialize L(v) for all vertices
    for v in V - Tv:
        if (u, v) in E:
            L[v] = W[(u, v)]
        elif (v, u) in E:
            L[v] = W[(v, u)]
        else:
            L[v] = float("inf")

    print("Initial L table for vertex u:", L)
    print("\nStarting with vertex:", u)

    while Tv != V:
        # Find w: L(w) = min{L(v) | v ∈ (V − Tv)}
        w = min((v for v in (V - Tv)), key=lambda v: L[v])

        # Find the associated edge e from TV
        e = None
        min_weight = float('inf')
        for v in Tv:
            if (v, w) in E and W[(v, w)] < min_weight:
                e = (v, w)
                min_weight = W[(v, w)]
            elif (w, v) in E and W[(w, v)] < min_weight:
                e = (w, v)
                min_weight = W[(w, v)]

        # Add the edge e to TE
        Te.add(e)

        # Update TV
        Tv.add(w)

        print(f"\nAdded edge {e} to the minimum spanning tree.")
        print("Current minimum spanning tree edges:", Te)

        # Update L(v) for v ∈ (V − Tv) if there is an edge (w, v) or (v, w) in E with weight less than L(v)
        for v in (V - Tv):
            if (w, v) in E and W[(w, v)] < L[v]:
                L[v] = W[(w, v)]
            elif (v, w) in E and W[(v, w)] < L[v]:
                L[v] = W[(v, w)]

        print("\nUpdated L table after including vertex", w, ":", L)

    return Te

# Simple graph
#V = {'A', 'B', 'C', 'D'}
#E = {('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'D')}
#W = {('A', 'B'): 1, ('A', 'C'): 3, ('B', 'C'): 2, ('B', 'D'): 4, ('C', 'D'): 5}

V = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
E = {('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'F'), ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'I'), ('I', 'J'), ('J', 'K'), ('K', 'A'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'G'), ('G', 'I'), ('I', 'K'), ('K', 'B'), ('F', 'H')}
W = {('A', 'B'): 5, ('A', 'C'): 3, ('B', 'D'): 6, ('C', 'E'): 2, ('D', 'F'): 9, ('E', 'F'): 4, ('F', 'G'): 7, ('G', 'H'): 1, ('H', 'I'): 5, ('I', 'J'): 10, ('J', 'K'): 3, ('K', 'A'): 8, ('B', 'C'): 4, ('C', 'D'): 1, ('D', 'E'): 7, ('E', 'G'): 5, ('G', 'I'): 2, ('I', 'K'): 6, ('K', 'B'): 9, ('F', 'H'): 3}

graph = (V, E, W)

minimum_spanning_tree = prim_minimum_spanning_tree(graph)
print("\nFinal Minimum Spanning Tree:", minimum_spanning_tree)


