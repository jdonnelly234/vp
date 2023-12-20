#
#Basic implementation for Prim's algorithm MST based on PLK Chapter 8 - Graph Algorithms
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
    
    print("Initial L table for vertex u: ")
    print(L)
    print(" ")

    #While there are unvisited vertices in graph
    while Tv != set(graph.keys()):
        print("Current Tv:", Tv)
        print("Current graph:", graph)
        print(" ")
        print("CURRENT U: ", u)

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
                print("Current v:", v)
                print("Current L:", L)
                print("Minimum weight:", minimum_weight)
                print("Current w:", w)
                print("Current e:", e)
                print(" ")

        if w is None:
            break;                      #Break if all vertices have been visited
        
        if w not in Tv:
            u = w                               #Update the current vertex to the latest MST vertex
            Te.append(e)                        #Adding edge with minimum weight to MST list
            Tv.add(w)                           #Adding vertex w to Tv set since it has been visited

        for v in graph:                     #Update minimum weight for the rest of the vertices in graph
            if v not in Tv:                 
                if (w, v) in graph and graph[w][(w, v)] < L[v]:         #If (v, w) in graph and weight of (v, w) < L[v]
                    L[v] = graph[w][(w, v)]                             #Update L[v] to weight of (v, w)
    
    #Return edges in MST
    return Te

#Simpler example graph from page
graph = {
    'A': {('A', 'B'): 2, ('A', 'C'): 5, ('A', 'D'): 4},
    'B': {('B', 'A'): 2, ('B', 'D'): 3},
    'C': {('C', 'A'): 5, ('C', 'D'): 1},
    'D': {('D', 'B'): 3, ('D', 'C'): 1, ('D', 'A'): 4}
}

#More complex example graph from page
complexGraph = {
    'A': {('A', 'B'): 5, ('A', 'C'): 10, ('A', 'D'): 8, ('A', 'E'): 7},
    'B': {('B', 'A'): 5, ('B', 'C'): 6, ('B', 'D'): 12},
    'C': {('C', 'A'): 10, ('C', 'B'): 6, ('C', 'D'): 15, ('C', 'E'): 9},
    'D': {('D', 'A'): 8, ('D', 'B'): 12, ('D', 'C'): 15, ('D', 'E'): 11},
    'E': {('E', 'A'): 7, ('E', 'C'): 9, ('E', 'D'): 11}
}

# Example graph for testing Prim's algorithm
testGraph = {
    'A': {('A', 'B'): 2, ('A', 'C'): 3, ('A', 'D'): 4},
    'B': {('B', 'A'): 2, ('B', 'C'): 1, ('B', 'E'): 5},
    'C': {('C', 'A'): 3, ('C', 'B'): 1, ('C', 'D'): 6, ('C', 'E'): 2},
    'D': {('D', 'A'): 4, ('D', 'C'): 6, ('D', 'E'): 8},
    'E': {('E', 'B'): 5, ('E', 'C'): 2, ('E', 'D'): 8}
}

MST = prims(testGraph)
print("The minimum spanning tree for this graph is: ", MST)



