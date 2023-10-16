#
#Basic implementation for Prim's algorithm MST based on lecture notes
#

def prims(graph):
    Te = []         #Initialising MST as empty
    Tv = set()      #Initialising set of visited vertices as empty

    #Starting MST on vertex u by changing graph vertices to list format and selecting first index
    u = list(graph.keys())[0]
    #Adding u to visited vertices
    Tv.add(u)

    #While there are unvisited vertices in graph
    while Tv != set(graph.keys()):
        minimum_weight = float("inf")   #Initialise minimum weight to be infinite
        w = None                        #Vertex being considered for addition to MST
        e = None                        #Edge that connects vertx w to current MST

        for v in graph:                 
            if v not in Tv:
                if (u, v) in graph[u]:      #If there is an edge (u, v) in graph
                    Lv = graph[u][(u, v)]   #then Lv is set to weight of edge (u, v)
                else:
                    Lv = float("inf")       #else Lv is set to infinity
                if Lv < minimum_weight:
                    minimum_weight = Lv     #Updating minimum weight to weight of edge (u, v) else infinity
                    w = v                   #Updating new MST vertex to v   
                    e = (u, v)              #Updating edge to (u, v)

        Te.append(e)                        #Adding edge with minimum weight to MST
        Tv.add(w)                           #Adding vertex w to Tv since it has been visited

        for v in graph:                     #Update minimum weight for the rest of the vertices in graph
            if v not in Tv:                 
                if (w, v) in graph:         #If (w, v) in graph
                    Lv = graph[w][(w, v)]   #Update Lv to weight of (w, v)
    #Return edges in MST
    return Te

#Example graph from page
graph = {
    'A': {('A', 'B'): 2, ('A', 'C'): 5},
    'B': {('B', 'A'): 2, ('B', 'C'): 7, ('B', 'D'):8},
    'C': {('C', 'A'): 5, ('C', 'B'): 7, ('C', 'D'):4, ('C', 'E'): 5},
    'D': {('D', 'B'): 8, ('D', 'C'): 4, ('D', 'F'): 10},
    'E': {('E', 'C'): 5, ('E', 'F'): 7},
    'F': {('F', 'D'): 10, ('F', 'E'): 7}
}

MST = prims(graph)
print("The minimum spanning tree for this graph is: ", MST)