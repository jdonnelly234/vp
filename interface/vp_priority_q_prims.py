#####################################################################################
# Implementation for Prim's algorithm MST based on PLK Chapter 8 - Graph Algorithms #
#####################################################################################

import heapq

def prim_minimum_spanning_tree_with_priority_queue(graph):
    V, E, W = graph
    V = set(V)  # Set of vertices
    E = set(E)  # Set of edges
    Te = set()  # Set of edges in the minimum spanning tree
    Tv = set()  # Set of visited vertices
    u = next(iter(V))  # Starting vertex, choosing any vertex in V
    L = {v: float("inf") for v in V}  # Initialize L(v) for all vertices
    L[u] = 0  # Starting vertex weight is 0 to ensure it's picked first
    num_comparisons = 0

    print(f"Running Prims on graph with {len(V)} vertices and {len(E)} edges")
    # Priority queue of vertices outside the MST, initialized with all vertices. The priority is L[v].
    pq = [(weight, v) for v, weight in L.items()]
    heapq.heapify(pq)  # Convert list into a heap

    while pq:
        min_weight, w = heapq.heappop(pq)  # Get vertex with minimum L value
        
        if w in Tv:  # Skip if vertex is already visited
            continue

        Tv.add(w)  # Add w to the set of visited vertices

        # If w was reached from another vertex u, add the edge (u, w) to Te
        if w != u:  # For the first vertex u==w, so skip
            Te.add((u, w) if (u, w) in E else (w, u))

        # Update L(v) for vertices v connected to w
        for v in V - Tv:
            if (w, v) in E or (v, w) in E:
                edge_weight = W.get((w, v), W.get((v, w)))
                num_comparisons += 1  # Counting weight comparison
                if edge_weight is not None and edge_weight < L[v]:
                    L[v] = edge_weight
                    heapq.heappush(pq, (L[v], v))  # Update priority queue with new lower weight

        u = w  # Update u for edge addition check

    print(f"Prim's algorithm found a minimum spanning tree with {len(Te)} edges")
    return Te, num_comparisons
