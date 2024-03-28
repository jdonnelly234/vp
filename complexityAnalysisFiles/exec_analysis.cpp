#include <iostream>
#include <set>
#include <unordered_map>
#include <chrono>
#include <vector>
#include <limits>

using namespace std;
using namespace std::chrono;

pair<set<pair<int, int>>, double> primMinimumSpanningTreeUniformWeight(int verticesCount) {
    auto startTime = high_resolution_clock::now();

    // Similar to Python, using set for vertices and visited vertices,
    // and unordered_map for L values to mirror Python's dictionary.
    set<int> V;
    for (int i = 0; i < verticesCount; ++i) V.insert(i);

    set<pair<int, int>> Te; // Set of edges in the minimum spanning tree, using pairs to represent edges.
    set<int> Tv; // Set of visited vertices.
    unordered_map<int, int> L; // Using unordered_map to store L values for each vertex, similar to Python's dict.

    int u = *V.begin(); // Starting vertex, akin to Python's next(iter(V)).
    Tv.insert(u);

    // Initialize L(v) for all vertices with uniform weight, mirroring the Python approach.
    for (int v : V) {
        if (v != u) L[v] = 1; // Assuming uniform weight of 1 for all edges, similar to Python.
    }

    while (Tv.size() != V.size()) {
        int w = -1;
        int minL = numeric_limits<int>::max();
        // Finding the vertex with minimum L value, equivalent to Python's min function on L.
        for (auto& pair : L) {
            if (Tv.find(pair.first) == Tv.end() && pair.second < minL) {
                w = pair.first;
                minL = pair.second;
            }
        }

        // Since we are using uniform weights, any vertex in Tv could technically be considered the "closest".
        int closest = *Tv.begin(); // Simplifying assumption due to uniform weights.
        Te.insert({closest, w});
        Tv.insert(w);

        // For uniform weights, no need to update L since all edges have the same weight.
    }

    auto endTime = high_resolution_clock::now();
    duration<double> execTime = duration_cast<duration<double>>(endTime - startTime);

    return {Te, execTime.count()};
}

int main() {
    vector<int> node_list = {2};
    for (int x = 500; x <= 20500; x += 500) {
        node_list.push_back(x);
    }

    for (int n : node_list) {
        auto [Te, execTime] = primMinimumSpanningTreeUniformWeight(n);
        cout << "Execution time for uniform weight with " << n << " nodes: " << execTime << " seconds\n";
    }

    return 0;
}
