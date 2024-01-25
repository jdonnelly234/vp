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

    print("\nStarting with vertex:", u)
    print(f"Initial L table for vertex {u}:", L)
    

    while Tv != V:
        # Find w: L(w) = min{L(v) | v ∈ (V − Tv)}
        w = min((v for v in (V - Tv)), key=lambda v: L[v])
               
        # Increment comparison count by (V - Tv) - 1 since min checks each element once
        num_comparisons += len(V - Tv) - 1  

        # Find the associated edge e from TV
        e = None
        min_weight = float('inf')
        for v in Tv:
            if (v, w) in E and W[(v, w)] < min_weight:
                e = (v, w)
                min_weight = W[(v, w)]
                num_comparisons += 1
            elif (w, v) in E and W[(w, v)] < min_weight:
                e = (w, v)
                min_weight = W[(w, v)]
                num_comparisons += 1

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
                num_comparisons += 1
            elif (v, w) in E and W[(v, w)] < L[v]:
                L[v] = W[(v, w)]
                num_comparisons += 1

        print("\nUpdated L table after including vertex", w, ":", L)

    return Te, num_comparisons