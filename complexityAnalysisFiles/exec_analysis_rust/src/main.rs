use std::collections::{HashSet, HashMap};

fn prim_minimum_spanning_tree_uniform_weight(vertices_count: usize) -> (HashSet<(usize, usize)>, f64) {
    let start_time = std::time::Instant::now();
    let mut te = HashSet::new(); // Set of edges in the minimum spanning tree
    let mut tv = HashSet::new(); // Set of visited vertices
    let mut l = HashMap::new(); // Dictionary for L values of each edge

    let u = 0; // Starting vertex, choosing any vertex in V

    tv.insert(u); // Adding initial vertex to Tv

    // Initialize L(v) for all vertices with uniform weight (e.g., 1 for simplicity)
    for v in 1..vertices_count {
        l.insert(v, 1); // Assuming uniform weight of 1 for all edges
    }

    while tv.len() != vertices_count {
        // Find w: L(w) = min{L(v) | v ∈ (V − Tv)}
        let w = (0..vertices_count)
            .filter(|v| !tv.contains(v))
            .min_by_key(|&v| l[&v])
            .unwrap();

        // Add the edge (closest in Tv, w) to Te
        // In a complete graph with uniform weights, any vertex in Tv could serve as the "closest"
        let closest = *tv.iter().next().unwrap(); // Simplification for uniform weights
        te.insert((closest, w));

        // Update TV
        tv.insert(w);

        // In a uniform weight scenario, no need to update L since all edges have the same weight
    }

    let execution_time = start_time.elapsed().as_secs_f64();
    (te, execution_time)
}

fn main() {
    let mut node_list = vec![2usize];

    for x in (500..=20000).step_by(500) {
        node_list.push(x);
    }

    for n in node_list {
        let (_te, exec_time) = prim_minimum_spanning_tree_uniform_weight(n);
        println!("Execution time for uniform weight with {} nodes: {:.6} seconds", n, exec_time);
    }
}
