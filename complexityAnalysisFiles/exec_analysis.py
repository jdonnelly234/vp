import time


# For generating a complete graphs with uni
#def generate_complete_graph(node_count):
#
#    graph = {}
#        # Connect each node to every other node except itself
#    for i in range(node_count):
#        edges = [(j, 1) for j in range(node_count) if j != i]
#        graph[i] = edges
#    return graph

#node_count = 6000  # Example node count
#complete_graph = generate_complete_graph(node_count)
#print("Generated!")

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

def prim_minimum_spanning_tree_uniform_weight(vertices_count):
    start_time = time.perf_counter()
    V = set(range(vertices_count))  # Set of vertices
    Te = set()  # Set of edges in the minimum spanning tree
    Tv = set()  # Set of visited vertices
    u = next(iter(V))  # Starting vertex, choosing any vertex in V
    L = {}  # Dictionary for L values of each edge

    Tv.add(u)  # Adding initial vertex to Tv

    # Initialize L(v) for all vertices with uniform weight (e.g., 1 for simplicity)
    for v in V - Tv:
        L[v] = 1  # Assuming uniform weight of 1 for all edges

    while Tv != V:
        # Find w: L(w) = min{L(v) | v ∈ (V − Tv)}
        w = min((v for v in (V - Tv)), key=lambda v: L[v])

        # Add the edge (closest in Tv, w) to Te
        # In a complete graph with uniform weights, any vertex in Tv could serve as the "closest"
        closest = next(iter(Tv))  # Simplification for uniform weights
        Te.add((closest, w))

        # Update TV
        Tv.add(w)

        # In a uniform weight scenario, no need to update L since all edges have the same weight

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return Te, execution_time

# Example usage
node_list = [2]

for x in range(500, 20500, 500):
    node_list.append(x)

print(node_list)

for n in node_list:
    Te, exec_time = prim_minimum_spanning_tree_uniform_weight(n)
    print(f"Execution time for uniform weight with {n} nodes: {exec_time:.6f} seconds")

