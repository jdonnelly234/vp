import unittest
from tkinter import StringVar
from unittest.mock import MagicMock, mock_open, patch
from interface.vp_graph import VisualisingPrims, Node, Edge
from interface.utils import *

class TestVPGraphNode(unittest.TestCase):
    def setUp(self):
        self.vp = VisualisingPrims()
        self.vp.start_node_var = StringVar()
        self.vp.end_node_var = StringVar()
        self.vp.weight_var = StringVar()
        self.vp.delete_node_var = MagicMock()
        self.vp.delete_edge_var = MagicMock()

        self.vp.canvas = MagicMock()
        self.vp.top_margin = 50  



    # Test creating a single node appends to graph d.s correctly
    def test_create_node(self):
        self.vp.create_node(100, 100, "A")
        self.assertEqual(len(self.vp.nodes), 1)
        self.assertEqual(self.vp.nodes[0].identifier, "A")
    


    # Test creating nodes at the canvas boundaries
    def test_node_creation_at_canvas_boundaries(self):
        self.vp.canvas.winfo_width.return_value = 700  
        self.vp.canvas.winfo_height.return_value = 568  
        
        # Test creation at each boundary (left, top, right, bottom)
        boundary_positions = [
            (0, 200),  # Left edge
            (300, 0),  # Top edge
            (700, 200),  # Right edge
            (300, 568)  # Bottom edge
        ]
        
        for x, y in boundary_positions:
            identifier = f"Node@({x},{y})"
            self.vp.create_node(x, y, identifier)
            created_node = self.vp.nodes[-1]  # Get the last created node
            self.assertEqual((created_node.x, created_node.y), (x, y), f"Node {identifier} was not created at the correct boundary position.")
    


    # Setup a scenario with a node and an edge, then delete the node
    def test_delete_node(self):
        self.vp.create_node(100, 100, "A")
        self.vp.delete_node_var = MagicMock()
        self.vp.delete_node_var.get = MagicMock(return_value="A")
        self.vp.delete_node()
        self.assertEqual(len(self.vp.nodes), 0)




    def test_delete_node_empty_input(self):
        self.vp.create_node(100, 100, "A")
        self.vp.delete_node_var = MagicMock()
        self.vp.delete_node_var.get = MagicMock(return_value="")
        self.vp.delete_node()
        expected_error_message = "Please select a node for deletion"
        self.assertIn(expected_error_message, self.vp.status_label.cget("text"))
        self.assertEqual(len(self.vp.nodes), 1, "Deleting a node with an empty identifier should not change the node count.")
    


    # Setup a scenario with a node and an edge, then attempt to delete a non-existent node
    def test_delete_non_existent_node(self):
        self.vp.create_node(100, 100, "A")
        self.vp.create_node(200, 200, "B")
        edge = Edge(self.vp.nodes[0], self.vp.nodes[1], 10)
        self.vp.create_edge(edge)

        initial_node_count = len(self.vp.nodes)
        self.vp.delete_node_var.get = MagicMock(return_value="C")
        self.vp.delete_node()

        # Verify no nodes were deleted
        self.assertEqual(len(self.vp.nodes), initial_node_count, "Deleting a non-existent node should not change the node count.")
    

    # Setup a scenario with a node and an edge, then delete the node and verify its connected edges are removed
    def test_delete_node_with_multiple_connected_edges(self):
        # Setup nodes and edges
        self.vp.create_node(100, 100, "A")
        self.vp.create_node(200, 200, "B")
        self.vp.create_node(300, 300, "C")
        self.vp.create_edge(Edge(self.vp.nodes[0], self.vp.nodes[1], 10))
        self.vp.create_edge(Edge(self.vp.nodes[0], self.vp.nodes[2], 15))
        self.vp.delete_node_var.get = MagicMock(return_value="A")
        self.vp.delete_node()
        # Verify that both edges connected to "A" are removed
        self.assertEqual(len(self.vp.edges), 0, "Edges connected to the deleted node were not correctly removed.")
        self.assertEqual(len(self.vp.nodes), 2, "Node was not correctly removed from the graph.")



    # Test node moves within canvas boundaries and updates edge positions when canvas is resized
    def test_move_node_canvas_resize(self):
        self.vp.nodes = [Node(100, 100, "A"), Node(200, 200, "B")]
        self.vp.edges = [Edge(self.vp.nodes[0], self.vp.nodes[1], 10)]
        for node in self.vp.nodes:
            node.id = MagicMock()  # Mock visual ID for canvas elements
            node.text_id = MagicMock()
        for edge in self.vp.edges:
            edge.line_id = MagicMock()
            edge.midpoint_id = MagicMock()
            edge.text_id = MagicMock()
        
        # Move node "A" to a new position
        new_x, new_y = 150, 150
        self.vp.resize_move_node(self.vp.nodes[0], new_x, new_y)
        
        # Check node's position was updated
        self.assertEqual((self.vp.nodes[0].x, self.vp.nodes[0].y), (new_x, new_y), "Node position did not update correctly.")
        
        # Verify node and text were moved on canvas
        self.vp.canvas.move.assert_any_call(self.vp.nodes[0].id, 50, 50)  # dx = 150 - 100, dy = 150 - 100
        self.vp.canvas.move.assert_any_call(self.vp.nodes[0].text_id, 50, 50)
        
        # Check that the connected edge's position was updated
        edge = self.vp.edges[0]
        expected_coords = (new_x, new_y, edge.end_node.x, edge.end_node.y)
        self.vp.canvas.coords.assert_any_call(edge.line_id, *expected_coords)
        
        # Verify midpoint and label of edge were updated
        mid_x, mid_y = (new_x + edge.end_node.x) / 2, (new_y + edge.end_node.y) / 2
        self.vp.canvas.coords.assert_any_call(edge.midpoint_id, mid_x - 8, mid_y - 8, mid_x + 8, mid_y + 8)
        self.vp.canvas.coords.assert_any_call(edge.text_id, mid_x, mid_y)


    # Test that the graph becomes disconnected after a node deletion and Prim's algorithm handles it.
    def test_graph_disconnect_after_node_deletion(self):
        # Setup a connected graph
        self.vp.nodes = [Node(100, 100, "A"), Node(200, 200, "B"), Node(300, 300, "C")]
        self.vp.edges = [Edge(self.vp.nodes[0], self.vp.nodes[1], 1), Edge(self.vp.nodes[1], self.vp.nodes[2], 2)]

        # Delete node B to disconnect the graph
        self.vp.delete_node_var.get = MagicMock(return_value="B")
        self.vp.delete_node()

        # Attempt to run Prim's algorithm
        self.vp.start_vertex_var.get = MagicMock(return_value="A")
        self.vp.generate_mst()
        
        expected_error_message = "Graph is disconnected. Prim's algorithm requires a connected graph."
        self.assertIn(expected_error_message, self.vp.status_label.cget("text"))



if __name__ == '__main__':
    unittest.main()
