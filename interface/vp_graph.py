import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time

from node import Node
from edge import Edge
from vp_graph_gui import GraphVisualiserGUI
from utils import *
from config import *
from PIL import ImageGrab
import sys

# Visualising Prim's main graph application class
class VisualisingPrims(GraphVisualiserGUI):
    def __init__(self):
        super().__init__()
        self.nodes = []  # List to store nodes
        self.edges = []  # List to store edges
        self.selected_node = None   # For storing the node that is currently selected for drag_handler
        self.drag_start_pos = None  # For storing the starting position of the drag for left_click_handler
        self.node_counter = 0  # Counter to keep track of the number of nodes

        # Bind the Configure event to handle canvas resizes
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.left_click_handler)
        self.canvas.bind("<B1-Motion>", self.drag_handler)

        self.canvas_old_width = self.canvas.winfo_reqwidth()
        self.canvas_old_height = self.canvas.winfo_reqheight()


    # For creating a new node
    def create_node(self, x, y, identifier):
        new_node = Node(x, y, identifier)
        new_node.id = self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill="blue", outline = "black", width = 3)
        new_node.text_id = self.canvas.create_text(x, y, text=identifier, font=("Arial", 14))
        self.nodes.append(new_node)
        self.node_counter += 1
        self.update_node_options()  # Update dropdown menus when a new node is added
    

    # Deletes a node and its edges
    def delete_node(self):
        node_identifier = self.delete_node_var.get()
        node_to_delete = next((node for node in self.nodes if node.identifier == node_identifier), None)

        if node_identifier == "":
            self.status_label.configure(text="Please select a node for deletion")

        if node_to_delete:
            # Remove the node visually
            self.canvas.delete(node_to_delete.id)
            self.canvas.delete(node_to_delete.text_id)
        
            # Remove the node from internal list
            self.nodes.remove(node_to_delete)

            # Remove edges connected to the node
            edges_to_remove = [edge for edge in self.edges if edge.start_node == node_to_delete or edge.end_node == node_to_delete]
            for edge in edges_to_remove:
                self.canvas.delete(edge.line_id)
                self.canvas.delete(edge.text_id)
                self.canvas.delete(edge.midpoint_id)
                self.edges.remove(edge)

            self.update_node_options()
            self.clear_info_text()
            self.next_step_button.configure(state='disabled')  # Disabled if canvas is clicked during Prim's
            self.toggle_mst_button.configure(state='disabled', text='Show MST only')  # Disabled if canvas is clicked during Prim's
            self.default_dropdown_labels()  # Reset the dropdown menus and weight entry field
            self.status_label.configure(text=f"Node {node_identifier} and its edges have been deleted")
            self.reset_node_and_edge_colors()  
            self.unhide_edges()

            # If no nodes are left, show placeholder text
            if self.nodes == 0:
                self.show_placeholder_text()
                self.canvas_screenshot_button.configure(state='disabled')  # Start as disabled



    # For creating an edge between two nodes
    def create_edge(self, edge):
        # Calculate the midpoint for the weight label
        mid_x = (edge.start_node.x + edge.end_node.x) / 2
        mid_y = (edge.start_node.y + edge.end_node.y) / 2

        # Create the edge and add it to the list
        edge.line_id = self.canvas.create_line(
            edge.start_node.x, edge.start_node.y,
            edge.end_node.x, edge.end_node.y, width=2, fill="black"
        )

        # Create an oval at the midpoint to serve as midpoint marker
        edge.midpoint_id = self.canvas.create_oval(
            mid_x - 8, mid_y - 8, mid_x + 8, mid_y + 8, fill="white", outline="black"
        )

        # Create the text for the weight
        edge.text_id = self.canvas.create_text(mid_x, mid_y, text=str(edge.weight), font=("Arial", 12), fill="black")

        self.edges.append(edge)

        print(f"Edge created in canvas: {edge.start_node.identifier} -> {edge.end_node.identifier}, Weight: {edge.weight}")

        # Ensure the text is above the oval
        self.canvas.tag_raise(edge.text_id)

        for node in self.nodes:
            self.canvas.tag_raise(node.id)
            self.canvas.tag_raise(node.text_id)

        self.update_edge_options()  # Update dropdown menu when a new edge is added


    # For manual edge creation using drop down menus, weight field and "Create Edge" button
    def manual_create_edge(self):
        try:
            start_node_identifier = self.start_node_var.get()  # Get the identifier of the start node
            end_node_identifier = self.end_node_var.get()  # Get the identifier of the end node
            weight_input = self.weight_var.get() # This might throw ValueError if not a valid float

            if "." in weight_input or not weight_input.isnumeric():
                raise ValueError("Weight must be an integer.")
            
            weight = int(weight_input)
            start_node = next((node for node in self.nodes if node.identifier == start_node_identifier), None)
            end_node = next((node for node in self.nodes if node.identifier == end_node_identifier), None)

            if not start_node or not end_node:
                raise ValueError("Invalid node selection.")

            if start_node == end_node:
                raise ValueError("Start node and end node cannot be the same.")
            
            if weight < 1 or weight > 99:
                raise ValueError("Weight must be a positive integer greater than 0 and less than 100.")
            
            if (start_node.identifier, end_node.identifier) in [(edge.start_node.identifier, edge.end_node.identifier) for edge in self.edges]:
                raise ValueError(f"Edge already exists between {start_node_identifier} and {end_node_identifier}.")

            print(f"Creating edge: {start_node.identifier} -> {end_node.identifier}, Weight: {weight}")
            edge = Edge(start_node, end_node, weight)
            
            self.create_edge(edge)
            self.reset_node_and_edge_colors()  # Reset colors of nodes and edges
            self.clear_info_text()  # Clear the info text widget
            self.next_step_button.configure(state='disabled')  # Disabled if canvas is clicked during Prim's
            self.toggle_mst_button.configure(state='disabled', text='Show MST only')  # Disabled if canvas is clicked during Prim's
            self.default_dropdown_labels()  # Reset the dropdown menus and weight entry field
            self.unhide_edges()
            self.status_label.configure(text=f"Edge {start_node_identifier} - {end_node_identifier} has been created with weight {weight}.")
            
        except ValueError as e:
            print(f"Error creating edge: {e}")
            self.status_label.configure(text=f"Error: {e}")


    # For deleting an edge
    def delete_edge(self):
        edge_identifier = self.delete_edge_var.get()
        if edge_identifier == "   ":
            self.status_label.configure(text="Please select an edge for deletion")
            return

        # Parse the edge identifier
        start_identifier, end_identifier = edge_identifier.split(' - ')
        
        # Find and remove the edge
        edge_to_delete = next((edge for edge in self.edges if edge.start_node.identifier == start_identifier and edge.end_node.identifier == end_identifier), None)
        if edge_to_delete:
            self.canvas.delete(edge_to_delete.line_id)
            self.canvas.delete(edge_to_delete.text_id)
            self.canvas.delete(edge_to_delete.midpoint_id)
            self.edges.remove(edge_to_delete)

            self.status_label.configure(text=f"Edge {edge_identifier} has been deleted")
            self.update_edge_options()  # Update dropdown menu when an edge is deleted
        
        self.delete_edge_var.set("   ")
        self.reset_node_and_edge_colors()  
        self.clear_info_text()  
        self.next_step_button.configure(state='disabled')  # Disabled if canvas is clicked during Prim's
        self.toggle_mst_button.configure(state='disabled', text='Show MST only')  # Disabled if canvas is clicked during Prim's
        self.default_dropdown_labels()  # Reset the dropdown menus and weight entry field
        self.unhide_edges()


    # Handles scenarios where user drags nodes around
    def drag_handler(self, event):
        if self.selected_node:
            # New x, y coordinates after the drag
            new_x = min(max(event.x, 15), self.canvas.winfo_width() - 15)
            new_y = min(max(event.y, self.top_margin), self.canvas.winfo_height() - 15)
        
            # Calculate the deltas
            dx = new_x - self.selected_node.x
            dy = new_y - self.selected_node.y

            # Update the position of the selected node
            self.selected_node.x = new_x
            self.selected_node.y = new_y
        
            # Move the node and its text identifier
            self.canvas.move(self.selected_node.id, dx, dy)
            self.canvas.move(self.selected_node.text_id, dx, dy)
        
            # Update connected edges
            for edge in self.edges:
                if edge.start_node == self.selected_node or edge.end_node == self.selected_node:
                    # Move edge
                    self.canvas.coords(edge.line_id, 
                                   edge.start_node.x, edge.start_node.y, 
                                   edge.end_node.x, edge.end_node.y)
                
                    # Calculate new midpoint position
                    mid_x = (edge.start_node.x + edge.end_node.x) / 2
                    mid_y = (edge.start_node.y + edge.end_node.y) / 2
                
                    # Move midpoint oval
                    if edge.midpoint_id is not None:
                        self.canvas.coords(edge.midpoint_id,
                                       mid_x - 8, mid_y - 8, 
                                       mid_x + 8, mid_y + 8)
                
                    # Move weight label
                    if edge.text_id is not None:
                        self.canvas.coords(edge.text_id, mid_x, mid_y)
                
                    # Bring edge, midpoint, and label to top
                    self.canvas.tag_raise(edge.midpoint_id)
                    self.canvas.tag_raise(edge.text_id)


    # Finds the node that was clicked on for left_click_handler
    def find_node(self, x, y):
        for node in self.nodes:
            if (node.x - 10) <= x <= (node.x + 10) and (node.y - 10) <= y <= (node.y + 10):
                return node
        return None
    

    # Handles all cases where user left clicks on the canvas
    def left_click_handler(self, event):
        x, y = event.x, max(event.y, self.top_margin)
        clicked_node = self.find_node(x, y)
        self.hide_placeholder_text()   # Hide the placeholder text
        self.reset_button.configure(state='normal') # Enable "Reset Graph" button when canvas is clicked and node is added
        self.canvas_screenshot_button.configure(state='normal')  

        self.status_label.configure(text="Graph Drawing Mode")

        if clicked_node:
            # If a node is clicked, initiate the drag process
            self.selected_node = clicked_node
            self.drag_start_pos = (x, y)
        else:
            self.reset_node_and_edge_colors()  # Reset colors of nodes and edges
            self.clear_info_text()  # Clear the info text widget    
            self.next_step_button.configure(state='disabled')  # Disabled if canvas is clicked during Prim's
            self.toggle_mst_button.configure(state='disabled', text='Show MST only')  # Disabled if canvas is clicked during Prim's
            self.default_dropdown_labels()  # Reset the dropdown menus and weight entry field
            
            # If canvas is clicked when only showing MST edges after Prim's, show all edges
            self.unhide_edges()

            # If no node is clicked, create a new node
            node_identifier = generate_node_identifier(self.node_counter)
            self.create_node(x, y, node_identifier)


    def generate_graph_dialog(self):
        # Ask for the complexity of the graph
        identifier = simpledialog.askstring("Graph Parameters", "Enter graph complexity (simple/complex):", parent=self)
        if identifier is None or identifier.lower() not in ["simple", "complex"]:  # Validate complexity input
            messagebox.showerror("Input Error", "Please enter 'simple' or 'complex' for graph complexity.")
            return

        self.generate_random_graph(identifier)
    

    # Generates a random graph on the canvas to save user time
    def generate_random_graph(self, identifier):
        self.reset_graph()  # Clear the existing graph
        
        if identifier == "simple":
            num_nodes = random.randint(3, 5)
        elif identifier == "complex":
            num_nodes = random.randint(7, 10)

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Create random nodes
        for _ in range(num_nodes):
            x = random.randint(15, canvas_width - 15)
            y = random.randint(self.top_margin, canvas_height - 15)
            node_identifier = generate_node_identifier(self.node_counter)
            new_node = Node(x, y, node_identifier)
            new_node.id = self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill="blue", outline = "black", width = 3)
            new_node.text_id = self.canvas.create_text(x, y, text=node_identifier, font=("Arial", 14))
            self.nodes.append(new_node)
            self.node_counter += 1

        self.update_node_options()

        # Start by creating a tree structure
        for i in range(1, len(self.nodes)):
            start_node = self.nodes[i - 1]
            end_node = self.nodes[i]
            weight = random.randint(1, 10)
            new_edge = Edge(start_node, end_node, weight)
            self.create_edge(new_edge)

        # Set to store created edges (start_node, end_node)
        created_edges = set((self.nodes[i-1].identifier, self.nodes[i].identifier) for i in range(1, len(self.nodes)))

        # Random number of additional edges
        num_additional_edges = random.randint(0, num_nodes * (num_nodes - 1) // 2 - num_nodes + 1)

        while len(created_edges) < num_additional_edges + num_nodes - 1:
            start_node, end_node = random.sample(self.nodes, 2)  # Select two unique nodes
            # Ensure uniqueness of edges
            if (start_node.identifier, end_node.identifier) not in created_edges and \
            (end_node.identifier, start_node.identifier) not in created_edges:

                weight = random.randint(1, 10)  # Random weight
                new_edge = Edge(start_node, end_node, weight)
                self.create_edge(new_edge)
                created_edges.add((start_node.identifier, end_node.identifier))

        self.status_label.configure(text="Generated random graph")
        self.reset_button.configure(state='normal') # Enable "Reset Graph" button when random graph is generated


    def reset_graph(self):
        self.canvas.delete("all")
        self.nodes = []
        self.edges = []
        self.node_counter = 0
        self.update_node_options()
        self.status_label.configure(text="Graph has been reset")
        self.clear_info_text()  # Clear the info text widget
        self.toggle_mst_button.configure(state='disabled', text='Show MST only')  
        self.default_dropdown_labels()
        self.reset_button.configure(state='disabled')
        self.show_placeholder_text()

        default_nodes = "No nodes available"
        default_edges = "No edges available"
        # Add placeholder instructions to dropdown menus
        self.start_node_menu.configure(values=[default_nodes])
        self.end_node_menu.configure(values=[default_nodes])
        self.start_vertex_menu.configure(values=[default_nodes])
        self.delete_node_menu.configure(values=[default_nodes])
        self.delete_edge_menu.configure(values=[default_edges])


    # For reset graph confirmation pop up
    def confirm_reset(self):
        # Confirmation dialog
        self.grab_set()  # Direct all events to the main window
        response = messagebox.askyesno("Reset Graph", "Are you sure you want to reset the graph?", parent=self)     # parent=self makes the messagebox appear in the center of the window
        self.grab_release()  # Release the grab after the file dialog is closed
        if response:
            self.reset_graph()


    # For importing a graph from a JSON file, note to self that canvas width = 624 and height=768
    def import_graph(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], parent=self)
            if not filepath:
                return

            with open(filepath, 'r') as file:
                data = json.load(file)

            # Perform all validation before modifying the graph
            for node_data in data["nodes"]:
                if node_data["x"] > 624 or node_data["y"] > 768:
                    raise ValueError(f"Node {node_data['id']} has invalid coordinates in the JSON file.")
                if not node_data["id"].isalpha() or len(node_data["id"]) > 1:
                    raise ValueError(f"Node identifier {node_data["id"]} must be a single letter.")

            for edge_data in data["edges"]:
                if edge_data["start"] not in [node["id"] for node in data["nodes"]] or \
                edge_data["end"] not in [node["id"] for node in data["nodes"]]:
                    raise ValueError("Invalid edge data in JSON file.")

            # Reset graph after data has been validated
            self.reset_graph()

            # Create nodes
            for node_data in data["nodes"]:
                self.create_node(node_data["x"], node_data["y"], node_data["id"])

            # Create edges
            for edge_data in data["edges"]:
                start_node = next(node for node in self.nodes if node.identifier == edge_data["start"])
                end_node = next(node for node in self.nodes if node.identifier == edge_data["end"])
                self.create_edge(Edge(start_node, end_node, edge_data["weight"]))

            self.status_label.configure(text="Graph has been successfully imported")
            self.reset_button.configure(state='normal')

        except json.JSONDecodeError:
            messagebox.showerror("Import Error", "Invalid JSON file format.", parent=self)
        except FileNotFoundError:
            messagebox.showerror("Import Error", "File not found.", parent=self)
        except ValueError as e:
            messagebox.showerror("Import Error", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Import Error", f"An error occurred: {e}", parent=self)
    

    def export_graph_to_json(self):
        if self.nodes == []:
            messagebox.showinfo("Export failed", "Canvas is empty. Please create a graph first.")
            self.status_label.configure(text="Click the canvas to create nodes, then use the left menus to create edges.")
            return
        graph_data = {
            "nodes": [{"id": node.identifier, "x": node.x, "y": node.y} for node in self.nodes],
            "edges": [{"start": edge.start_node.identifier, "end": edge.end_node.identifier, "weight": edge.weight} for edge in self.edges]
        }
        # Convert the dictionary to a JSON string
        graph_json = json.dumps(graph_data, indent=4)
        
        # Ask the user where to save the file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save your graph as JSON"
        )

        if file_path:  # If the user didn't cancel the dialog
            # Write the JSON data to the selected file
            with open(file_path, 'w') as file:
                file.write(graph_json)
            self.status_label.configure(text=f"Graph saved as {file_path}")
        else:
            self.status_label.configure(text="Graph export cancelled.")
    
   
    def screenshot_canvas(self):
        self.update_idletasks()  # Update the window layout
        self.update()  # Refresh the entire window to ensure it is drawn

        # Ask the user for a file name
        file_name = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                                                title="Save screenshot as...")
        if not file_name:  # User cancelled the operation
            return
        
        print("Canvas width: " + str(self.canvas_frame.winfo_width()))
        print("Canvas height: " + str(self.canvas_frame.winfo_height()))

        # Get the window ID (this works on Windows as well as on X11-based systems like most Linux distributions)
        window_id = self.winfo_id()

        
        x0 = self.canvas_frame.winfo_rootx()            # 58 is to cut off error messaging box
        y0 = self.canvas_frame.winfo_rooty() + 58
        x1 = x0 + self.canvas_frame.winfo_width()
        y1 = y0 + self.canvas_frame.winfo_height() - 58
        bbox = (x0, y0, x1, y1)

        screenshot = ImageGrab.grab(bbox=bbox)
        screenshot.save(file_name)
        messagebox.showinfo("Screenshot Saved", f"Screenshot saved to {file_name}")
    

    ##########################################
    # All of below is for Prim's integration #
    ##########################################


    # prim_minimum_spanning_tree function from correctPrims.py
    def prim_minimum_spanning_tree(self, graph):
        V, E, W = graph
        Te = set()  # Set of edges in the minimum spanning tree
        Tv = set()  # Set of visited vertices
        u = self.start_vertex_var.get() if self.start_vertex_var.get() in V else next(iter(V))  # Starting vertex
        L = {}      # Dictionary for L values of each edge

        Tv.add(u)           #Adding initial vertex to Tv

        print(graph)
        
        # Initialize L(v) for all vertices
        for v in V - Tv:
            if (u, v) in E:
                L[v] = W[(u, v)]
            elif (v, u) in E:
                L[v] = W[(v, u)]
            else:
                L[v] = float("inf")


        self.update_info_text(f"Starting with node {u}\n\n")
        self.update_info_text(f"Initial L table for node {u}:\n{L}\n\n")
        yield

        total_weight = 0

        while Tv != V:
            # Find w: L(w) = min{L(v) | v ∈ (V − Tv)}
            w = min((v for v in (V - Tv)), key=lambda v: L[v])                
            
            self.update_info_text(f"Choosing next node with smallest L value: {w}\n\n")

            # Find the associated edge e from TV
            e = None
            min_weight = float('inf')
            for v in Tv:
                if (v, w) in E and W[(v, w)] < min_weight:
                    e = (v, w)
                    min_weight = W[(v, w)]
                elif (w, v) in E and W[(w, v)] < min_weight:
                    e = (w, v)
                    min_weight = W[(w, v)]

            # Add the edge e to TE
            if e != None:
                Te.add(e)
                total_weight += min_weight   
                # Marks edge as part of MST for toggling button
                for edge in self.edges:
                    if (edge.start_node.identifier, edge.end_node.identifier) == e or \
                       (edge.end_node.identifier, edge.start_node.identifier) == e:
                        edge.is_mst_edge = True
                
            Tv.add(w)

            self.update_info_text(f"Added edge {e} to the MST.\n\n")
            yield e, w  # Pause the algorithm and return the added edge

            # Update L(v) for v ∈ (V − Tv) if there is an edge (w, v) or (v, w) in E with weight less than L(v)
            for v in (V - Tv):
                if (w, v) in E and W[(w, v)] < L[v]:
                    L[v] = W[(w, v)]
                elif (v, w) in E and W[(v, w)] < L[v]:
                    L[v] = W[(v, w)]
            
            self.update_info_text(f"Updated L table:\n{L}\n\n")
            yield
            
            self.update_info_text(f"Current visited nodes (Tv):\n {Tv}\n\n")
            self.update_info_text(f"Updated minimum spanning tree edges (Te):\n{Te}\n\n")
            yield
        
        self.update_info_text(f"Tv includes all nodes, therefore...\n\n-----Your final minimum spanning tree is----- \n\n {Te}\n\n The total weight of your MST is: {total_weight}\n\n---------------------------------------------")
        return Te


    # For starting Prim's on graph
    def generate_mst(self):
        try:
            self.clear_info_text()  # Clear the info text widget 
            self.start_time = time.time()  # Record start time

            if len(self.nodes) == 0:
                raise ValueError("Please add nodes and edges to the canvas.")
            
            if len(self.nodes) == 1:
                raise ValueError("Please add more than one node to the canvas.")
            
            self.reset_node_and_edge_colors()  # Reset colors of nodes and edges
            self.unhide_edges()  # Unhide all edges if they were hidden from previous Prim's run
            self.toggle_mst_button.configure(state='disabled', text='Show MST only')  # Disabled if Run Prims is clicked 

            V, E, W = extract_graph_data(self.nodes, self.edges)

            if not is_graph_connected(V, E):   # Check if the graph is connected
                raise ValueError("Graph is disconnected. Prim's algorithm requires a connected graph.")

            if not self.start_vertex_var.get() or self.start_vertex_var.get() == "Source":     # Check if a starting vertex is selected
                raise ValueError("Select a source node to begin Prim's algorithm on your graph.")
            
            # Initialize Prim's algorithm
            self.prim_generator = self.prim_minimum_spanning_tree((V, E, W))
            self.next_step_button.configure(state='normal')  # Enable "Next Step" button

            # Highlight the starting node
            start_node_identifier = self.start_vertex_var.get() # Highlights starting node
            self.highlight_node(start_node_identifier)  # Highlight the starting node

            # Start the first step of Prim's algorithm
            self.next_step()

        except ValueError as e:
            print(f"Error: {e}")
            self.status_label.configure(text=f"Error: {e}")
    

    # For proceeding through the algorithm with "Next Step" button using generator
    def next_step(self):
        try:
            # Proceed to the next step in the generator
            result = next(self.prim_generator)
            self.status_label.configure(text="Running Prim's algorithm...")
            self.finalize_button.configure(text="Click to start again")
        
            if result is not None:
                edge_added, node_visited = result
                # Highlight the added edge
                if edge_added:
                    self.visualize_mst(edge_added)
                # Highlight the visited node
                if node_visited:
                    self.highlight_node(node_visited)

        except StopIteration:
            # Algorithm is complete if it gets here
            self.end_time = time.time()
            execution_time = self.end_time - self.start_time
            self.next_step_button.configure(state='disabled')  # Disable next step button since prim's is finished
            self.toggle_mst_button.configure(state='normal')  # Enable toggle button when algorithm finishes
            self.update_info_text(f"\nCompleted in {execution_time:.2f} seconds.\n\n")
            self.status_label.configure(text="Prim's algorithm completed, your minimum spanning tree has been highlighted.")


    # For highlighting MST edges
    def visualize_mst(self, edge_added):
        # Highlight only the added edge
        start_id, end_id = edge_added
        for edge in self.edges:
            if (edge.start_node.identifier == start_id and edge.end_node.identifier == end_id) or \
                (edge.start_node.identifier == end_id and edge.end_node.identifier == start_id):
                self.canvas.itemconfig(edge.line_id, fill="orange", width=3)
                break  


    # For highlighting MST nodes
    def highlight_node(self, node_identifier):    
        # Find the node by its identifier and update its color to indicate it's been visited
        for node in self.nodes:
            if self.start_vertex_var.get() == node.identifier:
                # If source node, outline in red
                self.canvas.itemconfig(node.id, fill="orange", outline="red", width=3)  
            elif node.identifier == node_identifier:
                self.canvas.itemconfig(node.id, fill="orange", outline="black", width = 0)  # Colour visited node orange
                break    


    # For toggling between showing the full graph and the MST
    def toggle_mst_view(self):
        for edge in self.edges:
            if not edge.is_mst_edge:
                # Hide or show the edge
                current_state = self.canvas.itemcget(edge.line_id, 'state')
                new_state = 'hidden' if current_state == 'normal' else 'normal'
                self.canvas.itemconfigure(edge.line_id, state=new_state)
                self.canvas.itemconfigure(edge.midpoint_id, state=new_state)

                # Hide or show the weight label 
                current_state_text = self.canvas.itemcget(edge.text_id, 'state')
                new_state_text = 'hidden' if current_state_text == 'normal' else 'normal'
                self.canvas.itemconfigure(edge.text_id, state=new_state_text)
            
        # Update the button text based on the current state
        current_text = self.toggle_mst_button.cget('text')
        new_text = 'Show full graph' if current_text == 'Show MST only' else 'Show MST only'
        self.toggle_mst_button.configure(text=new_text)


    # For updating text in prim's textbox
    def update_info_text(self, message):
        self.info_text_widget.configure(state='normal')
        self.info_text_widget.insert(tk.END, message)
        self.info_text_widget.see(tk.END)
        self.info_text_widget.configure(state='disabled')


    # For clearing text in prim's textbox
    def clear_info_text(self):
        self.info_text_widget.configure(state='normal')
        self.info_text_widget.delete("1.0", tk.END)
        self.info_text_widget.configure(state='disabled')


    # For resetting colours of nodes and edges on canvas
    def reset_node_and_edge_colors(self):
        # Reset colors of nodes and edges
        for node in self.nodes:
            self.canvas.itemconfig(node.id, fill="blue", outline = "black", width = 3)  # Reset node color to blue
        for edge in self.edges:
            self.canvas.itemconfig(edge.line_id, width=2, fill="black")  # Reset edge color to black
    

    # For unhiding nodes and edges on canvas
    def unhide_edges(self):
        for edge in self.edges:     
                if not edge.is_mst_edge:
                    # Show the edge
                    current_state = self.canvas.itemcget(edge.line_id, 'state')
                    reset_state = 'normal' if current_state == 'hidden' else 'normal'
                    self.canvas.itemconfigure(edge.line_id, state=reset_state)
                    self.canvas.itemconfigure(edge.midpoint_id, state=reset_state)

                    # Show the weight label 
                    current_state_text = self.canvas.itemcget(edge.text_id, 'state')
                    reset_state_text = 'normal' if current_state_text == 'hidden' else 'normal'
                    self.canvas.itemconfigure(edge.text_id, state=reset_state_text)
    

    # Below is for handling graph dimensions wnen canvas is shrunk
    def on_canvas_resize(self, event):
        # Calculate the new dimensions
        new_width = event.width
        new_height = event.height
        
        # Assuming self.canvas_old_width and self.canvas_old_height hold the old dimensions
        # You need to initialize these somewhere in your code, probably in the __init__ method
        scale_x = new_width / self.canvas_old_width if self.canvas_old_width else 1
        scale_y = new_height / self.canvas_old_height if self.canvas_old_height else 1

        # Update the old dimensions with the new dimensions
        self.canvas_old_width = new_width
        self.canvas_old_height = new_height

        # Update the positions of all nodes based on the scale factors
        for node in self.nodes:
            self.resize_move_node(node, node.x * scale_x, node.y * scale_y)
        
    def resize_move_node(self, node, new_x, new_y):
        # Calculate deltas
        dx = new_x - node.x
        dy = new_y - node.y

        # Update the node's stored position
        node.x = new_x
        node.y = new_y

        # Move the node and its text identifier
        self.canvas.move(node.id, dx, dy)
        self.canvas.move(node.text_id, dx, dy)

        # Update connected edges
        for edge in self.edges:
            if edge.start_node == node or edge.end_node == node:
                # Update the edge line
                self.canvas.coords(edge.line_id, 
                                edge.start_node.x, edge.start_node.y, 
                                edge.end_node.x, edge.end_node.y)

                # Recalculate the midpoint for the edge
                mid_x = (edge.start_node.x + edge.end_node.x) / 2
                mid_y = (edge.start_node.y + edge.end_node.y) / 2

                # Update the position of the midpoint oval and the weight label
                self.canvas.coords(edge.midpoint_id,
                                mid_x - 8, mid_y - 8, 
                                mid_x + 8, mid_y + 8)
                self.canvas.coords(edge.text_id, mid_x, mid_y)

                # Ensure the edge, midpoint, and label are raised above other canvas items
                self.canvas.tag_raise(edge.midpoint_id)
                self.canvas.tag_raise(edge.text_id)



    def return_to_main_menu(self):
        self.destroy()
        from vp_main_gui import MainMenu    #Importing here to avoid circular import
        main_menu = MainMenu()  
        main_menu.mainloop() 

