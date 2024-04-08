import unittest
from tkinter import StringVar
from unittest.mock import MagicMock, mock_open, patch
from interface.vp_graph import VisualisingPrims, Node, Edge
from interface.utils import *

class TestVPGraphEdge(unittest.TestCase):
    print("###########GRAPH VISUALISER EDGE TESTS###########\n") 

    def setUp(self):
        self.vp = VisualisingPrims()
        self.vp.start_node_var = StringVar()
        self.vp.end_node_var = StringVar()
        self.vp.weight_var = StringVar()
        self.vp.delete_node_var = MagicMock()
        self.vp.delete_edge_var = MagicMock()

        self.vp.canvas = MagicMock()
        self.vp.top_margin = 50  



    # Test if creating an edge between two existing nodes works and is added to graph d.s
    def test_create_edge(self):
        self.vp.create_node(100, 100, "A")
        self.vp.create_node(200, 200, "B")
        edge = Edge(self.vp.nodes[0], self.vp.nodes[1], 10)
        self.vp.create_edge(edge)
        self.assertEqual(len(self.vp.edges), 1)
        self.assertEqual(self.vp.edges[0].weight, 10)
    


    # Test creating an edge with the same start and end nodes 
    def test_create_edge_with_same_start_end_nodes(self):
        self.vp.create_node(100, 100, "A")
        
        # Simulate user selecting the same node for start and end, and setting weight
        self.vp.start_node_var.set("A")
        self.vp.end_node_var.set("A")
        self.vp.weight_var.set("10")  # Valid weight

        self.vp.manual_create_edge()
        
        expected_error_message = "Start node and end node cannot be the same."
        self.assertIn(expected_error_message, self.vp.status_label.cget("text"))
        self.assertEqual(len(self.vp.edges), 0)



    # Test creating an edge between two nodes that already have an edge between them 
    def test_create_edge_with_existing_edge(self):
        self.vp.create_node(100, 100, "A")
        self.vp.create_node(200, 200, "B")
        edge = Edge(self.vp.nodes[0], self.vp.nodes[1], 10)
        self.vp.create_edge(edge)

        self.assertEqual(len(self.vp.edges), 1)     # Verify edge was created
        
        self.vp.start_node_var.set("A")
        self.vp.end_node_var.set("B")
        self.vp.weight_var.set("10")  # Valid weight

        self.vp.manual_create_edge()
        
        expected_error_message = "Edge already exists between A and B."
        self.assertIn(expected_error_message, self.vp.status_label.cget("text"))
        self.assertEqual(len(self.vp.edges), 1)



    # Setup scenario with two nodes and an edge, then delete the edge
    def test_delete_edge(self):
        self.vp.create_node(100, 100, "A")
        self.vp.create_node(200, 200, "B")
        edge = Edge(self.vp.nodes[0], self.vp.nodes[1], 10)
        self.vp.create_edge(edge)
        self.assertEqual(len(self.vp.edges), 1)     # Verify edge was created
        self.vp.delete_edge_var = MagicMock()
        self.vp.delete_edge_var.get = MagicMock(return_value="A - B")
        self.vp.delete_edge()
        self.assertEqual(len(self.vp.edges), 0)     # Verify edge was deleted
    


    # Setup scenario with two nodes and an edge, then attempt to delete a non-existent edge
    def test_delete_non_existent_edge(self):
        self.vp.create_node(100, 100, "A")
        self.vp.create_node(200, 200, "B")
        edge = Edge(self.vp.nodes[0], self.vp.nodes[1], 10)
        self.vp.create_edge(edge)

        initial_edge_count = len(self.vp.edges)
        self.vp.delete_edge_var.get = MagicMock(return_value="A - C")
        self.vp.delete_edge()
        # Verify no edges were deleted
        self.assertEqual(len(self.vp.edges), initial_edge_count, "Deleting a non-existent edge should not change the edge count.")
    


    # Test edge creation with negative weight input
    def test_edge_creation_negative_weight(self):
        # Setup initial graph with 2 nodes
        self.vp.create_node(100, 100, "A")
        self.vp.create_node(200, 200, "B")

        self.vp.start_node_var.set("A")
        self.vp.end_node_var.set("B")
        self.vp.weight_var.set(int("-1"))  # Invalid weight

        self.vp.manual_create_edge()
        
        # Verify no edge was created
        expected_error_message = "Weight must be an integer."
        self.assertIn(expected_error_message, self.vp.status_label.cget("text"))
        self.assertEqual(len(self.vp.edges), 0, "No edge should be created with a negative weight.")
    


    # Test edge creation with non-numeric weight input
    def test_edge_creation_non_numeric_weight(self):
        # Attempt to create an edge with a non-integer weight
        self.vp.create_node(100, 100, "A")
        self.vp.create_node(200, 200, "B")
        self.vp.start_node_var.set("A")
        self.vp.end_node_var.set("B")
        self.vp.weight_var.set("abc")  # Invalid weight

        self.vp.manual_create_edge()
        
        # Verify no edge was created
        expected_error_message = "Weight must be an integer."
        self.assertIn(expected_error_message, self.vp.status_label.cget("text"))
        self.assertEqual(len(self.vp.edges), 0, "No edge should be created with a non-integer weight.")
    


    # Test edge creation with non-integer weight input
    def test_edge_creation_non_integer_weight(self):
        # Attempt to create an edge with a non-integer weight
        self.vp.create_node(100, 100, "A")
        self.vp.create_node(200, 200, "B")
        self.vp.start_node_var.set("A")
        self.vp.end_node_var.set("B")
        self.vp.weight_var.set("9.2")  # Invalid weight

        self.vp.manual_create_edge()
        
        # Verify no edge was created
        expected_error_message = "Weight must be an integer."
        self.assertIn(expected_error_message, self.vp.status_label.cget("text"))
        self.assertEqual(len(self.vp.edges), 0, "No edge should be created with a non-integer weight.")



    # Test edge creation with excessive weight input
    def test_edge_creation_excessive_weight(self):
        self.vp.create_node(100, 100, "A")
        self.vp.create_node(200, 200, "B")
        self.vp.start_node_var.set("A")
        self.vp.end_node_var.set("B")
        self.vp.weight_var.set("100")  

        self.vp.manual_create_edge()
        
        # Verify no edge was created
        expected_error_message = "Weight must be a positive integer greater than 0 and less than 100."
        self.assertIn(expected_error_message, self.vp.status_label.cget("text"))
        self.assertEqual(len(self.vp.edges), 0, "No edge should be created with an excessively large weight.")
    


    # Test edge creation with non-existent nodes 
    def test_create_edge_with_nonexistent_nodes(self):
        # Attempt to create an edge with one or both nodes not existing in the graph
        self.vp.nodes = []
        self.vp.start_node_var.set("X")  
        self.vp.end_node_var.set("Y")  
        self.vp.weight_var.set("10")  # Valid weight
        
        self.vp.manual_create_edge()
        
        expected_error_message = "Invalid node selection."
        self.assertIn(expected_error_message, self.vp.status_label.cget("text"))
        self.assertEqual(len(self.vp.edges), 0, "No edge should be created with invalid nodes.")