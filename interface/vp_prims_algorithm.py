#####################################################################################
# Implementation for Prim's algorithm MST based on PLK Chapter 8 - Graph Algorithms #
#####################################################################################


def prim_minimum_spanning_tree(graph):
    V, E, W = graph
    V = set(V)  # Set of vertices
    E = set(E)  # Set of edges
    Te = set()  # Set of edges in the minimum spanning tree
    Tv = set()  # Set of visited vertices
    u = next(iter(V))  # Starting vertex, choosing any vertex in V
    L = {}      # Dictionary for L values of each edge
    num_comparisons = 0

    Tv.add(u)           #Adding initial vertex to Tv

    # Initialize L(v) for all vertices
    for v in V - Tv:
        if (u, v) in E:
            L[v] = W[(u, v)]
        elif (v, u) in E:
            L[v] = W[(v, u)]
        else:
            L[v] = float("inf")

    
    
    i = 0
    while Tv != V:
        i += 1
        # Find w: L(w) = min{L(v) | v ∈ (V − Tv)}
        w = min((v for v in (V - Tv)), key=lambda v: L[v])


        # Find the associated edge e from TV
        e = None
        min_weight = float('inf')
        for v in Tv:
            edge_weight = W.get((v, w), W.get((w, v)))
            if edge_weight is not None:
                num_comparisons += 1  # Counting weight comparison only
                if edge_weight < min_weight:
                    e = (v, w) if (v, w) in E else (w, v)
                    min_weight = edge_weight


        # Add the edge e to TE
        Te.add(e)

        # Update TV
        Tv.add(w)

        

        # Update L(v) for v ∈ (V − Tv) if there is an edge (w, v) or (v, w) in E with weight less than L(v)
        for v in (V - Tv):
            edge_weight_vw = W.get((v, w))
            edge_weight_wv = W.get((w, v))
            
            # Check the edge weight and count the comparison
            if edge_weight_vw is not None:
                num_comparisons += 1  # Counting weight comparison
                if edge_weight_vw < L[v]:
                    L[v] = edge_weight_vw
            if edge_weight_wv is not None:
                num_comparisons += 1  # Counting weight comparison
                if edge_weight_wv < L[v]:
                    L[v] = edge_weight_wv
        
        

    return Te, num_comparisons