import json
from tkinter import messagebox, filedialog
from interface.edge import Edge


# Checks if the graph is connected using depth-first search
def is_graph_connected(V, E):
    if not V:
        return False    # Return false if no vertices are present

    visited = set()     # For tracking all V that have been visited

    def dfs(v):
        if v in visited:
            return      # Returns immediately if vertex is in visited to stop duplicate additions
        visited.add(v)  # Adds v to visited if it was previously unvisited
        for u in V:
            if (v, u) in E or (u, v) in E:  # Checks if there is an edge between two vertices,
                dfs(u)                      # if so, dfs recursively called

    # Start depth-first search from the first node in V
    dfs(next(iter(V)))

    return visited == V #  Only returns true if list of visited vertices matches original list of vertices, this would mean graph is connected


# Extracts the graph data from the drawn nodes and edges for generating the MST
def extract_graph_data(nodes, edges):
    V = set(node.identifier for node in nodes)
    E = set()
    W = {}

    for edge in edges:
        start_id = edge.start_node.identifier
        end_id = edge.end_node.identifier

        E.add((start_id, end_id))
        W[(start_id, end_id)] = edge.weight

    return V, E, W


# Generates a unique identifier for each node
def generate_node_identifier(node_counter):
    # Generates a unique identifier for each node
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    quotient, remainder = divmod(node_counter, len(alphabet))  # node_counter is quotient and len(alphabet) remainder
    if quotient == 0:   # self.node_counter < 26
        return alphabet[remainder]
    else:               # if number of nodes exceeds amount of letters in the alphabet, start doubling identifiers ie. AA, BB ....
        return generate_node_identifier(quotient - 1) + alphabet[remainder]


