import unittest
from tkinter import StringVar, filedialog
from customtkinter import CTk
from unittest.mock import MagicMock, mock_open, patch
from interface.vp_graph import GraphVisualiser, Node, Edge
from interface.utils import *
import json
import os
from PIL import Image

class TestVPGraphIntegration(unittest.TestCase):
    print("###########GRAPH VISUALISER INTEGRATION TESTS###########\n") 
    def setUp(self):
        self.app = GraphVisualiser()

        self.app.start_node_var = StringVar()
        self.app.end_node_var = StringVar()
        self.app.weight_var = StringVar()

        self.app.resize_move_node = MagicMock()
        self.app.update_info_text = MagicMock()

        # Mocking canvas methods
        self.app.canvas = MagicMock()
        
        self.app.top_margin = 50
               


        

    # INTEGRATION TESTS BASED ON USER STORIES IN DISSERTATION TESTING CHAPTER 5.2 AND APPENDICES #  


    # GV User Story 1: Create a node
    def test_creating_node(self):
        initial_node_count = len(self.app.nodes)
        
        # Simulate a user clicking on the canvas to create a node
        # Note: (10, 10) should be within the bounds of the canvas.
        self.app.create_node(100, 100, "A")
        
        # Check if a new node has been added
        new_node_count = len(self.app.nodes)
        self.assertEqual(new_node_count, initial_node_count + 1)

        # Check if visual representation on canvas has been created
        self.app.canvas.create_oval.assert_called_with(82, 82, 118, 118, fill="blue", outline="black", width=3)
        self.app.canvas.create_text.assert_called_with(100, 100, text="A", font=("Arial", 14))

        # Check if the node has the correct identifier
        new_node = self.app.nodes[-1]
        self.assertEqual(new_node.identifier, "A")

    
    # GV User Story 2: Connecting Nodes with an Edge
    def test_connecting_nodes_with_edge(self):
        # Create two nodes
        self.app.create_node(100, 100, "A")
        self.app.create_node(200, 200, "B")
        
        # Reset the mock for create_oval here to clear previous calls
        self.app.canvas.create_oval.reset_mock()

        self.start_node = self.app.nodes[0]
        self.end_node = self.app.nodes[1]

        initial_edge_count = len(self.app.edges)
        
        # Set up the conditions as if a user has selected the nodes and entered a weight
        self.app.start_node_var.set(self.start_node.identifier)
        self.app.end_node_var.set(self.end_node.identifier)  
        weight = 5
        self.app.weight_var.set(str(weight)) 
        
        # Simulate the user clicking the "Create Edge" button
        self.app.manual_create_edge()
        
        # Check if a new edge has been added
        new_edge_count = len(self.app.edges)
        self.assertEqual(new_edge_count, initial_edge_count + 1)
        
        # Assert that create_oval is called once, which would be for the midpoint of the edge
        self.app.canvas.create_oval.assert_called_once_with(
            142.0, 142.0, 158.0, 158.0, fill='white', outline='black'
        )
            
        # Retrieve the actual edge created
        created_edge = self.app.edges[-1]
        
        # Check if the edge has the correct start and end nodes and weight
        self.assertEqual(created_edge.start_node, self.start_node)
        self.assertEqual(created_edge.end_node, self.end_node)
        self.assertEqual(created_edge.weight, weight)
    

    # GV User Story 3: Deleting a Node
    def test_deleting_node(self):
        # Simulating graph creation
        self.app.create_node(100, 100, "A")
        self.app.create_node(200, 200, "B")
        self.app.create_edge(Edge(self.app.nodes[0], self.app.nodes[1], 5))
        self.app.create_node(300, 300, "C")
        self.app.create_edge(Edge(self.app.nodes[1], self.app.nodes[2], 10))

        initial_node_count = len(self.app.nodes)
        initial_edge_count = len(self.app.edges)

        node_to_delete = self.app.nodes[1]
        
        # Set up the conditions as if a user has selected the node to delete from dropdown
        self.app.delete_node_var.set(node_to_delete.identifier)
        
        # Simulate the user clicking the "Delete Node" button
        self.app.delete_node()
        
        # Check if the node and its edges have been removed from the internal state
        new_node_count = len(self.app.nodes)
        new_edge_count = len(self.app.edges)
        self.assertEqual(new_node_count, initial_node_count - 1)
        self.assertEqual(new_edge_count, initial_edge_count - 2)  # Two edges connected to node "B"

        # Assert the canvas.delete method was called for the node and its edges
        expected_delete_calls = 8  # For 2 edges there are 6 calls (3 calls per edge, one for each of line, text and midpoint oval) and 2 calls for the node (oval and text identifier)
        self.assertEqual(self.app.canvas.delete.call_count, expected_delete_calls)
    

    # GV User story 4: Running Prim's Algorithm
    def test_running_prims_algorithm(self):
        # Create a connected graph
        self.app.create_node(100, 100, "A")
        self.app.create_node(200, 200, "B")
        self.app.create_node(300, 300, "C")
        self.app.create_edge(Edge(self.app.nodes[0], self.app.nodes[1], 5))
        self.app.create_edge(Edge(self.app.nodes[1], self.app.nodes[2], 10))

        # User selects a start node from the “Source” dropdown menu
        start_node_identifier = self.app.nodes[0].identifier
        self.app.start_vertex_var.set(start_node_identifier)

        # User clicks the "Run Prim's" button
        self.app.generate_mst()

        # Verify the start node is highlighted as the source
        self.app.canvas.itemconfig.assert_called_with(self.app.nodes[0].id, fill="orange", outline="red", width=3)
        
        # Simulate clicking the "Next Step" button to progress through the algorithm steps
        for _ in range(len(self.app.nodes) - 1):
            self.app.next_step()
        
        # After running Prim's algorithm, verify the MST is fully highlighted
        mst_edges = [edge for edge in self.app.edges if edge.is_mst_edge]
        for edge in mst_edges:
            self.app.canvas.itemconfig.assert_any_call(edge.line_id, fill="orange", width=3)
        
        # Check if the info text widget was updated with Prim's related information
        self.app.update_info_text.assert_called()
    

    # GV User story 5: Importing a graph
    def test_importing_graph(self):
        
        # Prepare a sample graph JSON structure
        self.sample_graph = {
            "nodes": [{"id": "A", "x": 100, "y": 100}, {"id": "B", "x": 200, "y": 200}, {"id": "C", "x": 300, "y": 300}],
            "edges": [{"start": "A", "end": "B", "weight": 5}, {"start": "B", "end": "C", "weight": 10}]
        }
        # Write the sample graph to a JSON file
        self.sample_graph_path = '/Users/jamesdonnelly/Third_Year/CSC3002_Computer_Science_Project/code/prims_implementation/testImportFiles/integration_test.json'

        # Right before importing, ensure the application is in a clean state
        self.assertEqual(len(self.app.nodes), 0)
        self.assertEqual(len(self.app.edges), 0)

        with open(self.sample_graph_path, 'w') as f:
            json.dump(self.sample_graph, f)
        
        with patch.object(filedialog, 'askopenfilename', return_value=self.sample_graph_path):
            # User clicks the "Import Graph" menu option and selects the JSON file
            self.app.import_graph()

        # After import_graph, verify the state and mock call counts
        self.assertEqual(len(self.app.nodes), len(self.sample_graph['nodes']))
        self.assertEqual(len(self.app.edges), len(self.sample_graph['edges']))
        self.assertEqual(self.app.canvas.create_oval.call_count, len(self.sample_graph['nodes']) + len(self.sample_graph['edges']))   # Adding edges length to account for midpoint ovals
        self.assertEqual(self.app.canvas.create_text.call_count, len(self.sample_graph['nodes']) + len(self.sample_graph['edges']))   # Adding edges length to account for meight text in midpoint oval
        self.assertEqual(self.app.canvas.create_line.call_count, len(self.sample_graph['edges']))


    # GV User story 6: Exporting a graph
    def test_exporting_graph(self):
        # Create a graph with 2 nodes and an edge
        self.app.create_node(100, 100, "A")
        self.app.create_node(200, 200, "B")
        self.app.create_edge(Edge(self.app.nodes[0], self.app.nodes[1], 5))

        # Mock the asksaveasfilename method to simulate a file save dialog
        with patch('tkinter.filedialog.asksaveasfilename', return_value='/Users/jamesdonnelly/Third_Year/CSC3002_Computer_Science_Project/code/prims_implementation/testImportFiles/integration_export.json'):
            # Mock the open function to simulate file writing
            with patch('builtins.open', mock_open()) as mocked_file:
                # User clicks the "Export" button 
                self.app.export_graph_to_json()

                # Check the mocked file was called correctly indicating the file was written
                mocked_file.assert_called_once_with('/Users/jamesdonnelly/Third_Year/CSC3002_Computer_Science_Project/code/prims_implementation/testImportFiles/integration_export.json', 'w')
                handle = mocked_file()
                # Check the 'write' method was called once and capture the JSON data written
                handle.write.assert_called_once()
                written_data = handle.write.call_args[0][0]
                # Convert the written data back to a dictionary
                exported_graph = json.loads(written_data)

        # Verify the exported graph matches the nodes and edges created
        expected_graph = {
            "nodes": [{"id": node.identifier, "x": node.x, "y": node.y} for node in self.app.nodes],
            "edges": [
                {"start": edge.start_node.identifier, "end": edge.end_node.identifier, "weight": edge.weight}
                for edge in self.app.edges
            ]
        }
        self.assertEqual(exported_graph, expected_graph)
    

    # GV User story 7: Taking a screenshot
    def test_taking_screenshot(self):
        # Mock the filedialog.asksaveasfilename to simulate file save dialog
        with patch('tkinter.filedialog.asksaveasfilename', return_value='/Users/jamesdonnelly/Third_Year/CSC3002_Computer_Science_Project/code/prims_implementation/testImportFiles/screenshot.png'):
            # Mock the ImageGrab.grab to simulate taking a screenshot
            with patch('PIL.ImageGrab.grab', return_value=MagicMock(spec=Image.Image)) as mock_grab:
                # Mock the image save method to simulate saving the file
                mock_save = MagicMock()
                mock_grab.return_value.save = mock_save

                # User clicks the "Screenshot" button
                self.app.screenshot_canvas()

                # Check that the grab method was called to take a screenshot
                mock_grab.assert_called_once()

                # Check that the save method was called to save the screenshot
                mock_save.assert_called_once_with('/Users/jamesdonnelly/Third_Year/CSC3002_Computer_Science_Project/code/prims_implementation/testImportFiles/screenshot.png')

                # Assert the save dialog was called with the expected file types
                filedialog.asksaveasfilename.assert_called_once_with(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                    title="Save screenshot as..."
                )
    

    # GV User story 8: Resetting the canvas
    def test_resetting_graph(self):
        # Simulating graph creation
        self.app.create_node(100, 100, "A")
        self.app.create_node(200, 200, "B")
        self.app.create_edge(Edge(self.app.nodes[0], self.app.nodes[1], 5))
        self.app.create_node(300, 300, "C")
        self.app.create_edge(Edge(self.app.nodes[1], self.app.nodes[2], 10))

        # Mock the messagebox to simulate user confirmation for reset
        with patch('tkinter.messagebox.askyesno', return_value=True):
            # User clicks the "Reset Graph" button
            self.app.reset_graph()

            # Check that the canvas is cleared
            self.app.canvas.delete.assert_called_with("all")

            # Verify that the internal state is also reset
            self.assertEqual(len(self.app.nodes), 0)
            self.assertEqual(len(self.app.edges), 0)

            # The status label should indicate that the graph has been reset
            self.assertEqual(self.app.status_label.cget("text"), "Graph has been reset")


    # GV User story 9: Resizing the canvas
    def test_resizing_canvas(self):
        # Create some nodes and edges for the graph
        self.app.create_node(100, 100, "A")  # Node A at 100x100
        self.app.create_node(200, 200, "B")  # Node B at 200x200

        # Assume initial canvas size
        initial_width = self.app.canvas.winfo_width()
        initial_height = self.app.canvas.winfo_height()
        self.app.canvas_old_width = initial_width
        self.app.canvas_old_height = initial_height

        # Mock the canvas width and height properties
        self.app.canvas.winfo_width = MagicMock(return_value=400)
        self.app.canvas.winfo_height = MagicMock(return_value=400)

        # Simulate the canvas resize event
        self.app.on_canvas_resize(event=MagicMock(width=400, height=400))

        # Check if the resize_move_node method was called for each node
        self.assertEqual(self.app.resize_move_node.call_count, len(self.app.nodes))

        # For each node, check if the node was repositioned correctly based on the new size
        for node in self.app.nodes:
            # Calculate expected new position
            expected_x = node.x * (400 / initial_width)
            expected_y = node.y * (400 / initial_height)
            self.app.resize_move_node.assert_any_call(node, expected_x, expected_y)
    

    # GV User story 10: Moving a node
    def test_moving_node_and_connected_edges(self):
        self.app.canvas.winfo_width.return_value = 300
        self.app.canvas.winfo_height.return_value = 300

        # Simulating graph creation
        self.app.create_node(100, 100, "A")
        self.app.create_node(200, 200, "B")
        connected_edge = Edge(self.app.nodes[0], self.app.nodes[1], 10)
        self.app.create_edge(connected_edge)

        self.app.selected_node = self.app.nodes[0] 

        # Capture initial positions of the node and edge
        initial_node_x, initial_node_y = self.app.selected_node.x, self.app.selected_node.y
        initial_edge_coords = (self.app.selected_node.x, self.app.selected_node.y, connected_edge.end_node.x, connected_edge.end_node.y)

        # Simulate dragging the node "A" to a new position (150, 150).
        event = MagicMock(x=150, y=150)
        self.app.drag_handler(event)

        # After the drag operation
        new_node_x, new_node_y = self.app.selected_node.x, self.app.selected_node.y
        new_edge_coords = (self.app.selected_node.x, self.app.selected_node.y, connected_edge.end_node.x, connected_edge.end_node.y)

        # Debug output
        print(f"Initial node position: ({initial_node_x}, {initial_node_y}), New node position: ({new_node_x}, {new_node_y})")
        print(f"Initial edge coords: {initial_edge_coords}, New edge coords: {new_edge_coords}")

        # Check node position was updated
        self.assertNotEqual((initial_node_x, initial_node_y), (new_node_x, new_node_y), "Node position did not change.")
        self.assertEqual(new_node_x, 150, "Node X position not updated correctly.")
        self.assertEqual(new_node_y, 150, "Node Y position not updated correctly.")

        # Check edge position was updated
        expected_new_edge_coords = (150, 150, connected_edge.end_node.x, connected_edge.end_node.y)
        self.assertEqual(new_edge_coords, expected_new_edge_coords, "Edge position not updated correctly.")
    

    # GV User story 11: Showing only MST edges on canvas
    def test_showing_only_mst_edges(self):
        self.app.canvas = MagicMock()
        # Simulating graph creation
        self.app.create_node(100, 100, "A")
        self.app.create_node(200, 200, "B")
        self.app.create_node(300, 300, "C")
        self.app.create_edge(Edge(self.app.nodes[0], self.app.nodes[1], 5))
        self.app.create_edge(Edge(self.app.nodes[1], self.app.nodes[2], 10))
        self.app.create_edge(Edge(self.app.nodes[0], self.app.nodes[2], 15))

        # User selects a start node from the “Source” dropdown menu for Prim's algorithm
        start_node_identifier = self.app.nodes[0].identifier
        self.app.start_vertex_var.set(start_node_identifier)

        # Run Prim's algorithm to completion to identify the MST edges
        self.app.start_vertex_var.set("A")  
        self.app.generate_mst()
        for _ in range(len(self.app.nodes) - 1):
            self.app.next_step()

        self.app.canvas.itemconfigure = MagicMock()

        # Simulate the "Show MST only" button action
        self.app.toggle_mst_view()
        
        # Check if itemconfig was called
        try:
            # Verify if itemconfig was called at all
            self.app.canvas.itemconfigure.assert_called()
        except AssertionError:
            # If not, print the call_args_list for debug
            print("itemconfig call_args_list:", self.app.canvas.itemconfigure.call_args_list)
            raise
    

    # GV User story 12: Removing an edge
    def test_remove_edge(self):
        # Simulating graph creation with one edge
        self.app.create_node(100, 100, "A")
        self.app.create_node(200, 200, "B")
        self.app.create_edge(Edge(self.app.nodes[0], self.app.nodes[1], 5))

        initial_edge_count = len(self.app.edges)

        # User selects an edge from the “Delete Edge” dropdown menu.
        edge_to_delete = self.app.edges[0]
        edge_identifier = f"{edge_to_delete.start_node.identifier} - {edge_to_delete.end_node.identifier}"
        self.app.delete_edge_var.set(edge_identifier)

        # User clicks the "Delete Edge" button
        self.app.delete_edge()

        # Check if the edge has been removed from the internal state
        new_edge_count = len(self.app.edges)
        self.assertEqual(new_edge_count, initial_edge_count - 1)

        # The visual representation of the chosen edge is removed from the canvas
        self.app.canvas.delete.assert_any_call(edge_to_delete.line_id)
        self.app.canvas.delete.assert_any_call(edge_to_delete.text_id)
        self.app.canvas.delete.assert_any_call(edge_to_delete.midpoint_id)

        # Assert the edge is no longer in the list of edges
        self.assertNotIn(edge_to_delete, self.app.edges)


        
  



if __name__ == '__main__':
    unittest.main()

    