package prims_implementation.complexityAnalysisFiles;

import java.util.HashSet;
import java.util.Set;
import java.util.HashMap;

public class ExecAnalysis {

    public static class ExecutionResult {
        Set<Pair<Integer, Integer>> spanningTreeEdges;
        double executionTime;

        public ExecutionResult(Set<Pair<Integer, Integer>> spanningTreeEdges, double executionTime) {
            this.spanningTreeEdges = spanningTreeEdges;
            this.executionTime = executionTime;
        }
    }

    public static ExecutionResult primMinimumSpanningTreeUniformWeight(int verticesCount) {
        long startTime = System.nanoTime();

        Set<Integer> V = new HashSet<>(); // Set of vertices
        for (int i = 0; i < verticesCount; i++) {
            V.add(i);
        }

        Set<Pair<Integer, Integer>> Te = new HashSet<>(); // Set of edges in the minimum spanning tree
        Set<Integer> Tv = new HashSet<>(); // Set of visited vertices
        HashMap<Integer, Integer> L = new HashMap<>(); // Dictionary for L values of each edge

        int u = V.iterator().next(); // Starting vertex
        Tv.add(u);

        // Initialize L(v) for all vertices with uniform weight
        for (int v : V) {
            if (v != u) L.put(v, 1); // Assuming uniform weight of 1 for all edges
        }

        while (Tv.size() != V.size()) {
            int w = -1;
            int minL = Integer.MAX_VALUE;
            for (var entry : L.entrySet()) {
                if (!Tv.contains(entry.getKey()) && entry.getValue() < minL) {
                    w = entry.getKey();
                    minL = entry.getValue();
                }
            }

            int closest = Tv.iterator().next(); // Simplification for uniform weights
            Te.add(new Pair<>(closest, w));
            Tv.add(w);

            // No need to update L since all edges have the same weight
        }

        long endTime = System.nanoTime();
        double executionTime = (endTime - startTime) / 1e9;

        return new ExecutionResult(Te, executionTime);
    }

    public static void main(String[] args) {
        int[] node_list = {2, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500, 13000, 13500, 14000, 14500, 15000, 15500, 16000, 16500, 17000, 17500, 18000, 18500, 19000, 19500, 20000};

        for (int n : node_list) {
            ExecutionResult result = primMinimumSpanningTreeUniformWeight(n);
            System.out.printf("Execution time for uniform weight with %d nodes: %.6f seconds%n", n, result.executionTime);
        }
    }

    static class Pair<T1, T2> {
        T1 first;
        T2 second;

        public Pair(T1 first, T2 second) {
            this.first = first;
            this.second = second;
        }
    }
}
