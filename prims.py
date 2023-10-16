#
#Basic implementation for Prim's algorithm MST based on lecture notes
#

def prims(graph):
    Te = []         #Initialising MST edges as empty
    Tv = set()      #Initialising set of visited vertices as empty
    L = {}          #Initialising dictionary for all vertices

    #Starting MST on vertex u by changing graph vertices to a list and selecting first index
    u = list(graph.keys())[0]
    #Adding u to visited vertices
    Tv.add(u)

    #Initialise L for all vertices in graph
    for v in graph:
        if v != u:                      
            if (u, v) in graph[u]:
                L[v] = graph[u][(u, v)] #Set L[v] to weight of (u, v)
            else:
                L[v] = float("inf")     #Else weight of (u, v) is infinite
        

    #While there are unvisited vertices in graph
    while Tv != set(graph.keys()):
        minimum_weight = float("inf")   #Initialise minimum weight to be infinite
        w = None                        #Vertex being considered for addition to MST
        e = None                        #Edge that connects vertex w to current MST

        for v in graph:                 
            if v not in Tv:
                if (u, v) in graph[u]:        #If there is an edge (u, v) in graph
                    L[v] = graph[u][(u, v)]   #then L[v] is set to weight of edge (u, v)
                else:
                    L[v] = float("inf")       #else L[v] is set to infinity
                if L[v] < minimum_weight:
                    minimum_weight = L[v]     #Updating minimum weight to weight of edge (u, v) else infinity
                    w = v                     #Updating new MST vertex to v   
                    e = (u, v)                #Updating edge connected to new MST vertex to (u, v)

        Te.append(e)                        #Adding edge with minimum weight to MST
        Tv.add(w)                           #Adding vertex w to Tv since it has been visited

        for v in graph:                     #Update minimum weight for the rest of the vertices in graph
            if v not in Tv:                 
                if (w, v) in graph and graph[w][(w, v)] < L[v]:         #If (w, v) in graph and weight of (w, v) < Lv
                    L[v] = graph[w][(w, v)]                             #Update Lv to weight of (w, v)
    #Return edges in MST
    return Te

#Example graph from page
#graph = {
#    'A': {('A', 'B'): 2, ('A', 'C'): 5},
#    'B': {('B', 'A'): 2, ('B', 'C'): 7, ('B', 'D'):8},
#    'C': {('C', 'A'): 5, ('C', 'B'): 7, ('C', 'D'):4, ('C', 'E'): 5},
#    'D': {('D', 'B'): 8, ('D', 'C'): 4, ('D', 'F'): 10},
#    'E': {('E', 'C'): 5, ('E', 'F'): 7},
#    'F': {('F', 'D'): 10, ('F', 'E'): 7}
#}

#Example graph
graph = {
    'A': {('A', 'B'): 2, ('A', 'C'): 3},
    'B': {('B', 'A'): 2, ('B', 'C'): 4, ('B', 'D'): 5},
    'C': {('C', 'A'): 3, ('C', 'B'): 4, ('C', 'D'): 1},
    'D': {('D', 'B'): 5, ('D', 'C'): 1}
}

MST = prims(graph)
print("The minimum spanning tree for this graph is: ", MST)