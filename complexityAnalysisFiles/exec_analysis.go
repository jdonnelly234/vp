package main

import (
	"fmt"
	"math"
	"time"
)

func primMinimumSpanningTreeUniformWeight(verticesCount int) ([][]int, float64) {
	startTime := time.Now()

	V := make(map[int]bool) // Set of vertices
	for i := 0; i < verticesCount; i++ {
		V[i] = true
	}

	Te := make([][]int, 0) // Set of edges in the minimum spanning tree
	Tv := make(map[int]bool) // Set of visited vertices

	// Starting vertex, choosing any vertex in V
	var u int
	for vertex := range V {
		u = vertex
		break
	}
	Tv[u] = true

	L := make(map[int]int) // Dictionary for L values of each edge
	for v := range V {
		if !Tv[v] {
			L[v] = 1 // Assuming uniform weight of 1 for all edges
		}
	}

	for len(Tv) < len(V) {
		var w, minL = -1, math.MaxInt32
		for v, lv := range L {
			if lv < minL && !Tv[v] {
				minL = lv
				w = v
			}
		}

		// In a complete graph with uniform weights, any vertex in Tv could serve as the "closest"
		var closest int
		for tv := range Tv {
			closest = tv
			break
		}
		Te = append(Te, []int{closest, w})

		Tv[w] = true
		delete(L, w)
	}

	endTime := time.Now()
	executionTime = endTime.Sub(startTime).Seconds()

	return Te, executionTime
}

func main() {
	nodeList := []int{2}

	for x := 500; x <= 20500; x += 500 {
		nodeList = append(nodeList, x)
	}

	fmt.Println(nodeList)

	for _, n := range nodeList {
		_, execTime := primMinimumSpanningTreeUniformWeight(n)
		fmt.Printf("Execution time for uniform weight with %d nodes: %.6f seconds\n", n, execTime)
	}
}
