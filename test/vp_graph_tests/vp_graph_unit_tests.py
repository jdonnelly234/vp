import unittest
from tkinter import StringVar
from unittest.mock import MagicMock, mock_open, patch
from interface.vp_graph import VisualisingPrims, Node, Edge
from interface.utils import *

class TestVisualisingPrims(unittest.TestCase):
    def setUp(self):
        self.vp = VisualisingPrims()
        self.vp.start_node_var = StringVar()
        self.vp.end_node_var = StringVar()
        self.vp.weight_var = StringVar()
        self.vp.delete_node_var = MagicMock()
        self.vp.delete_edge_var = MagicMock()

        self.vp.canvas = MagicMock()
        self.vp.top_margin = 50  

    #             #
    # COMBO TESTS #
    #             #
        

    # Test creating multiple nodes and edges
    def test_multiple_nodes_and_edges(self):
        # Create multiple nodes
        for i, (x, y) in enumerate([(100, 100), (200, 200), (300, 300)]):
            self.vp.create_node(x, y, chr(65+i))  # ASCII for A, B, C

        self.assertEqual(len(self.vp.nodes), 3)

        # Create multiple edges
        for i in range(len(self.vp.nodes) - 1):
            edge = Edge(self.vp.nodes[i], self.vp.nodes[i+1], i+10)
            self.vp.create_edge(edge)

        self.assertEqual(len(self.vp.edges), 2)
        self.assertEqual(self.vp.edges[0].weight, 10)
        self.assertEqual(self.vp.edges[1].weight, 11)
    

    # Test creating a node and edge after Prim's
    def test_add_node_and_edge_after_prims(self):
        # Setup a known graph and run Prim's algorithm
        self.vp.nodes = [Node(100, 100, "A"), Node(200, 200, "B"), Node(300, 300, "C")]
        self.vp.edges = [Edge(self.vp.nodes[0], self.vp.nodes[1], 1), Edge(self.vp.nodes[1], self.vp.nodes[2], 2)]
        graph = (set(["A", "B", "C"]), {("A", "B"), ("B", "C")}, {("A", "B"): 1, ("B", "C"): 2})
        self.vp.prim_minimum_spanning_tree(graph)

        # Attempt to add a new node and edge
        initial_node_count = len(self.vp.nodes)
        initial_edge_count = len(self.vp.edges)
        
        self.vp.create_node(100, 100, "E")  
    
        # Find or create nodes "A" and "E" to use in creating a new Edge
        node_A = next((node for node in self.vp.nodes if node.identifier == "A"), None)
        node_E = next((node for node in self.vp.nodes if node.identifier == "E"), None)
        
        # Assuming node_A and node_E are not None and valid Node objects
        if node_A and node_E:
            new_edge = Edge(node_A, node_E, 3)  # Create a new Edge object
            self.vp.create_edge(new_edge)  # Add the new edge to the graph

        # Verify a node and an edge were added
        self.assertEqual(len(self.vp.nodes), initial_node_count + 1)
        self.assertEqual(len(self.vp.edges), initial_edge_count + 1)



    @patch('interface.vp_graph.random.randint')
    def test_generate_simple_graph(self, mock_randint):
        # Mock randint to return controlled values for testing
        mock_randint.side_effect = [
            3,  # num_nodes
            15, 100, 15, 200, 15, 300,  # Node positions for 3 nodes
            1, 1,  # Edge weights for the initial linear structure of 2 edges
            0,  
        ]

        self.vp.generate_random_graph("simple")
        self.assertTrue(3 <= len(self.vp.nodes) <= 5)
        self.assertTrue(len(self.vp.edges) >= 2)  # At least a linear structure

        for node in self.vp.nodes:
            self.assertTrue(15 <= node.x <= 785)  # Node X within canvas bounds considering margin
            self.assertTrue(73 <= node.y <= 553)  # Node Y within canvas bounds considering top_margin

        for edge in self.vp.edges:
            self.assertTrue(1 <= edge.weight <= 10)  # Edge weight within specified bounds
    
    

    @patch('interface.vp_graph.random.randint')
    def test_generate_complex_graph(self, mock_randint):
        # Adjust side_effect as needed for more complex graph testing
        mock_randint.side_effect = [7,  # num_nodes
                                    # Node positions (X, Y)
                                    15, 100,
                                    15, 200,
                                    15, 300,
                                    15, 400,
                                    15, 450,
                                    15, 470,
                                    15, 480,
                                    # Edge weights
                                    1, 1, 1, 1, 1, 1,
                                    # Additional edges
                                    1, 1, 1]

        self.vp.generate_random_graph("complex")
        self.assertTrue(7 <= len(self.vp.nodes) <= 10)
        self.assertTrue(len(self.vp.edges) > 6)  # At least a linear structure plus additional edges

        for node in self.vp.nodes:
            self.assertTrue(15 <= node.x <= 785)  # Node X within canvas bounds considering margin
            self.assertTrue(73 <= node.y <= 553)  # Node Y within canvas bounds considering top_margin

        for edge in self.vp.edges:
            self.assertTrue(1 <= edge.weight <= 10)  # Edge weight within specified bounds


    #             #
    # PRIMS TESTS #
    #             #
    

    # Test Prim's algorithm with a known graph and unique MST
    def test_prim_with_known_graph(self):
        self.vp.update_info_text = MagicMock()

        # Example graph with unique MST
        V = set(["A", "B", "C", "D"])
        E = {("A", "B"), ("B", "C"), ("C", "D"), ("A", "D"), ("B", "D")}
        W = {("A", "B"): 1, ("B", "C"): 2, ("C", "D"): 3, ("A", "D"): 4, ("B", "D"): 5}
        graph = (V, E, W)
        
        # Mock start vertex
        self.vp.start_vertex_var = MagicMock()
        self.vp.start_vertex_var.get.return_value = "A"
        
        mst_edges = set()
        # Step through the Prim's generator to collect MST edges
        for result in self.vp.prim_minimum_spanning_tree(graph):
            if result:  # result is None for yields that do not return an edge
                edge, _ = result  # Decompose the result to get just the edge
                mst_edges.add(edge)

        # Define the expected MST edges based on the given weights
        expected_mst_edges = {("A", "B"), ("B", "C"), ("C", "D")}
        self.assertEqual(mst_edges, expected_mst_edges)



    # Test Prim's with a known graph and multiple possible MSTs
    def test_prim_with_multiple_possible_msts(self):
        V = set(["A", "B", "C"])
        E = {("A", "B"), ("B", "C"), ("A", "C")}
        W = {("A", "B"): 1, ("B", "C"): 1, ("A", "C"): 1}  # Equal weights make multiple MSTs possible
        graph = (V, E, W)
        
        self.vp.start_vertex_var = MagicMock()
        self.vp.start_vertex_var.get.return_value = "A"

        mst_edges = set()
        for result in self.vp.prim_minimum_spanning_tree(graph):
            if result:  
                edge, _ = result  # Extract the edge part
                mst_edges.add(edge)

        valid_mst_options = [
            {("A", "B"), ("B", "C")},
            {("A", "B"), ("A", "C")},
            {("B", "C"), ("A", "C")}
        ]

        self.assertTrue(mst_edges in valid_mst_options)


    # Test Prim's with a disconnected graph
    def test_prims_with_disconnected_graph(self):
        # Setup a disconnected graph
        self.vp.nodes = [Node(100, 100, "A"), Node(200, 200, "B"), Node(300, 300, "C")]
        self.vp.edges = [Edge(self.vp.nodes[0], self.vp.nodes[1], 10)]
        self.vp.start_vertex_var.set = "A"
        
        # Mock the status_label to capture text changes
        self.vp.status_label = MagicMock()
        
        # Attempt to generate MST
        self.vp.generate_mst()
        
        # Since generate_mst() handles exceptions and updates the status_label text,
        # we check if the appropriate error message is displayed.
        expected_error_message = "Graph is disconnected. Prim's algorithm requires a connected graph."
        
        # Verify the status_label's text was updated with the expected error message
        actual_status_text = self.vp.status_label.configure.call_args[1]['text']
        self.assertIn(expected_error_message.lower(), actual_status_text.lower(),
                    "Expected error message about disconnected graph not found in status label.")



    #                     #
    # MISC FUNCTION TESTS #
    #                     #
        


    # Test is_graph_connected
    def test_graph_connectivity(self):
        # Create a connected graph
        V = {'A', 'B', 'C'}
        E = {('A', 'B'), ('B', 'C')}
        self.assertTrue(is_graph_connected(V, E))

        # Create a disconnected graph
        V = {'A', 'B', 'C', 'D'}
        E = {('A', 'B'), ('C', 'D')}
        self.assertFalse(is_graph_connected(V, E))



    # Test dragging a node updates its position correctly
    def test_drag_handler(self):
        self.vp.canvas.winfo_width.return_value = 300
        self.vp.canvas.winfo_height.return_value = 300
        
        self.vp.create_node(100, 100, "A")
        self.vp.selected_node = self.vp.nodes[0]
        event = MagicMock()
        event.x = 150
        event.y = 150
        self.vp.drag_handler(event)
        self.assertEqual(self.vp.nodes[0].x, 150)
        self.assertEqual(self.vp.nodes[0].y, 150)
    

    


    # Test importing and exporting graph data
    #def test_import_export_graph(self):
        #mock_graph_data = {
        #    "nodes": [{"id": "A", "x": 100, "y": 100}, {"id": "B", "x": 200, "y": 200}],
        #    "edges": [{"start": "A", "end": "B", "weight": 10}]
        #}
        #with patch('builtins.open', mock_open(read_data=mock_json)):
        #    self.vp.import_graph()  
        #    self.assertEqual(len(self.vp.nodes), 2)
        #    self.assertEqual(len(self.vp.edges), 1)

        #with patch('builtins.open', mock_open()) as mocked_file:
        #    self.vp.export_graph_to_json()
        #    mocked_file().write.assert_called_once_with(mock_json)
    

    

    
    
if __name__ == '__main__':
    unittest.main()
