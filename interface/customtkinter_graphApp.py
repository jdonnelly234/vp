import customtkinter as ctk
from customtkinter import E, END, N, NO, S, W, X, Y, CTkInputDialog
import tkinter as tk
from tkinter import OptionMenu, StringVar, Entry, messagebox, filedialog, simpledialog
import random
import time
import json

# For node objects
class Node:
    def __init__(self, x, y, identifier):
        self.x = x  
        self.y = y  
        self.id = None  # To store the ID of the oval on the canvas
        self.text_id = None  # To store the ID of the text on the canvas
        self.identifier = identifier  # To store the identifier of the node

# For edge objects
class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.line_id = None  # To store the ID of the line on the canvas
        self.text_id = None  # To store the ID of the text label for the weight
        self.midpoint_id = None  # For the midpoint oval
        self.is_mst_edge = False  # Attribute to mark if the edge is part of the MST for toggling button

# Main application class for setting up UI and default values in fields
class GraphApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Visualising Prim's")

        # Set the window size
        window_width = 1200
        window_height = 800

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Find the center point
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)

        # Set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Minimum size for the window to avoid issues with resizing
        self.minsize(window_width, window_height) 

        self.top_margin = 50  # Margin to prevent nodes from being placed behind the status label

        # Frames for different sections
        self.left_frame = ctk.CTkFrame(self, width=200, fg_color="#2b2828", corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky='ns', rowspan=14)

        # Headings for UI sections 
        self.upper_left_frame_title = ctk.CTkLabel(self.left_frame, text="Create an edge", font=("Calibri", 20, "bold"))
        self.upper_left_frame_title.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        self.middle_left_frame_title = ctk.CTkLabel(self.left_frame, text="Delete a node or edge", font=("Calibri", 20, "bold"))
        self.middle_left_frame_title.grid(row=5, column=0, pady=10, padx=10, sticky='w')

        self.lower_left_frame_title = ctk.CTkLabel(self.left_frame, text="Other features", font=("Calibri", 20, "bold"))
        self.lower_left_frame_title.grid(row=8, column=0, pady=10, padx=10, sticky='w')

        self.canvas_frame = ctk.CTkFrame(self, width=624, height=768, fg_color="#2b2828", corner_radius=10, bg_color="#2b2828")
        self.canvas_frame.grid(row=0, column=1, sticky='nsew', rowspan=8)

        self.right_frame = ctk.CTkFrame(self, width=200, fg_color="#2b2828", corner_radius=0)
        self.right_frame.grid(row=0, column=2, sticky='ns', rowspan=8, columnspan=2)

        self.right_frame_title = ctk.CTkLabel(self.right_frame, text="Run Prim's algorithm", font=("Calibri", 20, "bold"))
        self.right_frame_title.grid(row=0, column=0, pady=10, padx=10, sticky='ew', columnspan=2)

        self.status_frame = ctk.CTkFrame(self, width=200)
        self.status_frame.grid(row=0, column=0, pady=12, padx=50, columnspan=4, sticky='n')

        # Initialize canvas
        self.canvas = ctk.CTkCanvas(self.canvas_frame, width=700, height=568, bg="white")
        self.canvas.pack(padx=10, pady=10, fill="both", expand=True)

        self.nodes = []  # List to store nodes
        self.edges = []  # List to store edges

        self.selected_node = None
        self.drag_start_pos = None

        # UI components
        self.status_label = ctk.CTkLabel(self.status_frame, text="Graph Drawing Mode", font=("Calibri", 12, "italic"))
        self.status_label.pack(pady=1, padx=1)  # Use pack to add padding inside the frame

        # Dropdown menus and weight input
        self.start_node_var = StringVar(self)
        self.end_node_var = StringVar(self)
        self.weight_var = StringVar(self)
        self.start_vertex_var = StringVar(self)
        self.delete_node_var = StringVar(self)
        
        # Dropdown menus for start/end node
        self.start_node_menu = OptionMenu(self, self.start_node_var, "Add nodes to see them here")
        self.start_node_menu.grid(in_=self.left_frame, row=1, column=0, pady=5, padx=10, sticky='e')

        self.end_node_menu = OptionMenu(self, self.end_node_var, "Add nodes to see them here")
        self.end_node_menu.grid(in_=self.left_frame, row=2, column=0, pady=5, padx=10, sticky='e')

        # Dropdown menu for node deletion
        self.delete_node_menu = OptionMenu(self.left_frame, self.delete_node_var, "Add nodes to see them here")
        self.delete_node_menu.grid(row=6, column=0, pady=10, padx=10, sticky='w')

        # Dropdown menu for edge deletion
        self.delete_edge_var = StringVar(self)
        self.delete_edge_var.set("   ") # Default value
        self.delete_edge_menu = OptionMenu(self.left_frame, self.delete_edge_var, "Add edges to see them here")
        self.delete_edge_menu.grid(row=7, column=0, pady=10, padx=10, sticky='w')

        # Dropdown menu for source vertex
        self.start_vertex_menu = OptionMenu(self.right_frame, self.start_vertex_var, "Add nodes to see them here")
        self.start_vertex_menu.grid(row=1, column=1, pady=10, padx=(1,10), sticky='e')
        self.start_vertex_var.set("Source")  # Default value

        # Weight entry field
        self.weight_entry = ctk.CTkEntry(self, textvariable=self.weight_var, width=50)
        self.weight_entry.grid(in_=self.left_frame, row=3, column=0, pady=10, padx=10, sticky='e')

        # Labels for the dropdown menus and weight input
        self.start_node_label = ctk.CTkLabel(self, text="Start Node")
        self.start_node_label.grid(in_=self.left_frame, row=1, column=0, sticky='w', padx=10, pady=10)

        self.end_node_label = ctk.CTkLabel(self, text="End Node")
        self.end_node_label.grid(in_=self.left_frame, row=2, column=0, sticky='w', padx=10)

        self.weight_label = ctk.CTkLabel(self, text="Weight", fg_color="#302c2c")
        self.weight_label.grid(in_=self.left_frame, row=3, column=0, sticky='w', padx=10)
        
        # Buttons
        self.create_edge_button = ctk.CTkButton(self, text="Create Edge", command=self.manual_create_edge)
        self.create_edge_button.grid(in_=self.left_frame, row=4, column=0, pady=10, padx=10, sticky='ew')

        self.finalize_button = ctk.CTkButton(self, text="Run Prim's", command=self.generate_mst)
        self.finalize_button.grid(in_=self.right_frame, row=1, column=0, pady=10, padx=10, sticky='ew')

        self.reset_button = ctk.CTkButton(self, text="Reset Graph", state="disabled", hover_color="#FF0000", command=self.confirm_reset)
        self.reset_button.grid(in_=self.left_frame, row=11, column=0, pady=10, padx=10, sticky='ew')

        self.random_graph_button = ctk.CTkButton(self, text="Generate a graph", command=self.generate_graph_dialog)
        self.random_graph_button.grid(in_=self.left_frame, row=9, column=0, pady=10, padx=10, sticky='ew')

        self.delete_node_button = ctk.CTkButton(self.left_frame, text="Delete Node", command=self.delete_node, width=20)
        self.delete_node_button.grid(row=6, column=0, pady=10, padx=10, sticky='e')

        self.delete_edge_button = ctk.CTkButton(self.left_frame, text="Delete Edge", command=self.delete_edge, width = 20)
        self.delete_edge_button.grid(row=7, column=0, pady=10, padx=10, sticky='e')

        # Text widget to display the L table and other information
        self.info_text_widget = ctk.CTkTextbox(self, height=500, width=300)
        self.info_text_widget.grid(in_=self.right_frame, row=2, column=0, columnspan = 2, pady=10, padx=10, sticky='ew')

        # Next Step button for proceeding through Prim's 
        self.next_step_button = ctk.CTkButton(self, text="Next Step", command=self.next_step)
        self.next_step_button.grid(in_=self.right_frame, row=4, pady=20, columnspan = 2)
        self.next_step_button.configure(state='disabled')  # Disabled by default, enabled when Prim's starts

        # MST toggle button
        self.toggle_mst_button = ctk.CTkButton(self.right_frame, text="Show MST only", command=self.toggle_mst_view)
        self.toggle_mst_button.grid(row=5, pady=10, columnspan = 2)
        self.toggle_mst_button.configure(state='disabled')  # Start as disabled

        # Import graph button
        self.import_graph_button = ctk.CTkButton(self, text="Import Graph", width=20, command=self.import_graph)
        self.import_graph_button.grid(in_=self.left_frame, row=10, column=0, pady=10, padx=10, sticky='ew')

        self.node_counter = 0  # Counter to keep track of the number of nodes

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.left_click_handler)
        self.canvas.bind("<B1-Motion>", self.drag_handler)
        
        # Placeholder for empty canvas message
        self.placeholder_text_id = self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text="Click on the canvas to create a node.",
            fill="#bbbbbb",  # Light grey color
            font=("TkDefaultFont", 18, "italic"),
            state="normal"  # Starts with the text shown
        )

        # Configure the grid layout to allow for resizing
        self.columnconfigure(1, weight=1)
        for i in range(8):  
            self.rowconfigure(i, weight=1)


    # Generic method to reset the dropdown menus and weight entry field to default values
    def default_dropdown_labels(self):
        self.start_vertex_var.set("Source")  # Default values for dropdowns
        self.start_node_var.set("")
        self.end_node_var.set("")
        self.weight_var.set("")
        self.delete_node_var.set("")
        self.finalize_button.configure(text="Run Prims")  # Reset the button text


    # Method to show the placeholder text
    def show_placeholder_text(self):
        if not self.nodes and not self.edges:  # If there are no nodes or edges
            self.canvas.itemconfig(self.placeholder_text_id, state="normal")
    

    # Method to hide the placeholder text
    def hide_placeholder_text(self):
        self.canvas.itemconfig(self.placeholder_text_id, state="hidden")
    

    # Generates a unique identifier for each node
    def generate_node_identifier(self):
        # Generates a unique identifier for each node
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        quotient, remainder = divmod(self.node_counter, len(alphabet))  # self.node_counter / alphabet legnth returns quotient and remainder
        if quotient == 0:   # self.node_counter < 26
            return alphabet[remainder]
        else:               # if number of nodes exceeds amount of letters in the alphabet, start doubling identifiers ie. AA, BB ....
            return self.generate_node_identifier(quotient - 1) + alphabet[remainder]


    # For updating all node related things in drop down menus
    def update_node_options(self):
        # Update the options in the dropdown menus for start nodes
        start_menu = self.start_node_menu["menu"]
        start_menu.delete(0, "end")
        for node in self.nodes:
            print(f"Adding {node.identifier} to start node menu")
            start_menu.add_command(label=node.identifier, command=tk._setit(self.start_node_var, node.identifier))
            
        # Update the options in the dropdown menus for end nodes
        end_menu = self.end_node_menu["menu"]
        end_menu.delete(0, "end")
        for node in self.nodes:
            print(f"Adding {node.identifier} to end node menu")
            end_menu.add_command(label=node.identifier, command=tk._setit(self.end_node_var, node.identifier))
        
        # Update the options in the dropdown menu for starting vertex
        start_vertex_menu = self.start_vertex_menu["menu"]
        start_vertex_menu.delete(0, "end")
        for node in self.nodes:
            start_vertex_menu.add_command(label=node.identifier, command=tk._setit(self.start_vertex_var, node.identifier))
        
        # Update the options in the dropdown menu for node deletion
        delete_node_menu = self.delete_node_menu["menu"]
        delete_node_menu.delete(0, "end")
        for node in self.nodes:
            delete_node_menu.add_command(label=node.identifier, command=tk._setit(self.delete_node_var, node.identifier))


    # For updating all edge related things in drop down menus
    def update_edge_options(self):
        # Update the options in the dropdown menu for edge deletion
        delete_edge_menu = self.delete_edge_menu["menu"]
        delete_edge_menu.delete(0, "end")
        for edge in self.edges:
            edge_identifier = f"{edge.start_node.identifier} - {edge.end_node.identifier}"
            delete_edge_menu.add_command(label=edge_identifier, command=tk._setit(self.delete_edge_var, edge_identifier))

        if not self.edges:  # Add placeholder text if no edges are left
            delete_edge_menu.add_command(label="No edges available")


    # Handles cases where user tries to manually create an edge using drop down menus
    def manual_create_edge(self):
        try:
            start_node_identifier = self.start_node_var.get()  # Get the identifier of the start node
            end_node_identifier = self.end_node_var.get()  # Get the identifier of the end node
            weight = int(self.weight_var.get())  # This might throw ValueError if not a valid float

            start_node = next((node for node in self.nodes if node.identifier == start_node_identifier), None)
            end_node = next((node for node in self.nodes if node.identifier == end_node_identifier), None)

            if not start_node or not end_node:
                raise ValueError("Invalid node selection.")

            if start_node == end_node:
                raise ValueError("Start node and end node cannot be the same.")
            
            if weight < 1 or weight > 99 or not isinstance(weight, int):
                raise ValueError("Weight must be a positive integer greater than 0 and less than 100.")
            
            if (start_node.identifier, end_node.identifier) in [(edge.start_node.identifier, edge.end_node.identifier) for edge in self.edges]:
                raise ValueError(f"Edge already exists between {start_node_identifier} and {end_node_identifier}.")

            print(f"Creating edge: {start_node.identifier} -> {end_node.identifier}, Weight: {weight}")
            edge = Edge(start_node, end_node, weight)
            
            self.create_edge(edge)

            # Reset colors of nodes and edges
            for node in self.nodes:
                self.canvas.itemconfig(node.id, fill="blue", outline = "black")  # Reset node color to blue
            for edge in self.edges:
                self.canvas.itemconfig(edge.line_id, width=2, fill="black")  # Reset edge color to black
            
            # Clears the info text widget 
            self.info_text_widget.configure(state='normal')
            self.info_text_widget.delete("1.0", tk.END)
            self.info_text_widget.configure(state='disabled') 

            self.next_step_button.configure(state='disabled')  # Disabled if canvas is clicked during Prim's

            self.toggle_mst_button.configure(state='disabled', text='Show MST only')  # Disabled if canvas is clicked during Prim's

            self.default_dropdown_labels()  # Reset the dropdown menus and weight entry field
            
        except ValueError as e:
            print(f"Error creating edge: {e}")
            self.status_label.configure(text=f"Error: {e}")


    # Handles all cases where user left clicks on the canvas
    def left_click_handler(self, event):
        x, y = event.x, max(event.y, self.top_margin)
        clicked_node = self.find_node(x, y)
        self.hide_placeholder_text()   # Hide the placeholder text
        self.reset_button.configure(state='normal') # Enable "Reset Graph" button when canvas is clicked and node is added
        self.status_label.configure(text="Graph Drawing Mode")

        if clicked_node:
            # If a node is clicked, initiate the drag process
            self.selected_node = clicked_node
            self.drag_start_pos = (x, y)
        else:
            # Reset colors of nodes and edges
            for node in self.nodes:
                self.canvas.itemconfig(node.id, fill="blue", outline = "black")  # Reset node color to blue
            for edge in self.edges:
                self.canvas.itemconfig(edge.line_id, width=2, fill="black")  # Reset edge color to black
            
            # Clears the info text widget 
            self.info_text_widget.configure(state='normal')
            self.info_text_widget.delete("1.0", tk.END)
            self.info_text_widget.configure(state='disabled') 

            self.next_step_button.configure(state='disabled')  # Disabled if canvas is clicked during Prim's

            self.toggle_mst_button.configure(state='disabled', text='Show MST only')  # Disabled if canvas is clicked during Prim's

            self.default_dropdown_labels()  # Reset the dropdown menus and weight entry field
            
            # There might be a better way of doing this but this works for now
            for edge in self.edges:     # If canvas is clicked when only showing MST edges, show all edges
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

            # If no node is clicked, create a new node
            node_identifier = self.generate_node_identifier()
            self.create_node(x, y, node_identifier)


    # For creating a new node
    def create_node(self, x, y, identifier):
        new_node = Node(x, y, identifier)
        new_node.id = self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill="blue", outline = "black")
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

            # Remove edges connected to this node
            edges_to_remove = [edge for edge in self.edges if edge.start_node == node_to_delete or edge.end_node == node_to_delete]
            for edge in edges_to_remove:
                self.canvas.delete(edge.line_id)
                self.canvas.delete(edge.text_id)
                self.canvas.delete(edge.midpoint_id)
                self.edges.remove(edge)

            # Update node identifiers and dropdown menus
            self.update_node_options()

            self.status_label.configure(text=f"Node {node_identifier} and its edges have been deleted")

            # Reset colors of nodes and edges
            for node in self.nodes:
                self.canvas.itemconfig(node.id, fill="blue", outline = "black")  # Reset node color to blue
            for edge in self.edges:
                self.canvas.itemconfig(edge.line_id, width=2, fill="black")  # Reset edge color to black
            
            # Clears the info text widget 
            self.info_text_widget.configure(state='normal')
            self.info_text_widget.delete("1.0", tk.END)
            self.info_text_widget.configure(state='disabled') 

            self.next_step_button.configure(state='disabled')  # Disabled if canvas is clicked during Prim's

            self.toggle_mst_button.configure(state='disabled', text='Show MST only')  # Disabled if canvas is clicked during Prim's

            self.default_dropdown_labels()  # Reset the dropdown menus and weight entry field

            # If no nodes are left, show placeholder text
            if not self.nodes:
                self.show_placeholder_text()

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

        # Create an oval at the midpoint to serve as a more visible midpoint marker
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

        # Reset colors of nodes and edges
        for node in self.nodes:
            self.canvas.itemconfig(node.id, fill="blue", outline = "black")  # Reset node color to blue
        for edge in self.edges:
            self.canvas.itemconfig(edge.line_id, width=2, fill="black")  # Reset edge color to black
            
        # Clears the info text widget 
        self.info_text_widget.configure(state='normal')
        self.info_text_widget.delete("1.0", tk.END)
        self.info_text_widget.configure(state='disabled') 

        self.next_step_button.configure(state='disabled')  # Disabled if canvas is clicked during Prim's

        self.toggle_mst_button.configure(state='disabled', text='Show MST only')  # Disabled if canvas is clicked during Prim's

        self.default_dropdown_labels()  # Reset the dropdown menus and weight entry field


    # Finds the node that was clicked on for drag_handler
    def find_node(self, x, y):
        for node in self.nodes:
            if (node.x - 10) <= x <= (node.x + 10) and (node.y - 10) <= y <= (node.y + 10):
                return node
        return None
    


    def generate_graph_dialog(self):
        
        # Ask for the complexity of the graph
        identifier = simpledialog.askstring("Graph Parameters", "Enter graph complexity (simple/complex):", parent=self)
        if identifier is None or identifier.lower() not in ["simple", "complex"]:  # Validate complexity input
            messagebox.showerror("Input Error", "Please enter 'simple' or 'complex' for graph complexity.")
            return

        self.generate_random_graph(identifier)
    

    # Generates a random graph on the canvas to save user time
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
            node_identifier = self.generate_node_identifier()
            new_node = Node(x, y, node_identifier)
            new_node.id = self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill="blue", outline = "black")
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



    # Resets the graph for blank canvas
    def reset_graph(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Reset the lists
        self.nodes = []
        self.edges = []

        # Reset the node counter and update dropdown menus
        self.node_counter = 0
        self.update_node_options()

        # Reset notificiation label
        self.status_label.configure(text="Graph has been reset")

        # Clears the info text widget 
        self.info_text_widget.configure(state='normal')
        self.info_text_widget.delete("1.0", tk.END)
        self.info_text_widget.configure(state='disabled') 

        # Disables the toggle button when graph is reset
        self.toggle_mst_button.configure(state='disabled', text='Show MST only')  

        # Reset the dropdown menus and weight entry field
        self.default_dropdown_labels()

        # Clear the dropdown menus
        self.start_node_menu["menu"].delete(0, "end")
        self.end_node_menu["menu"].delete(0, "end")
        self.start_vertex_menu["menu"].delete(0, "end")
        self.delete_node_menu["menu"].delete(0, "end")
        self.delete_edge_menu["menu"].delete(0, "end")

        # Add placeholder instruction
        self.start_node_menu["menu"].add_command(label="No nodes available")
        self.end_node_menu["menu"].add_command(label="No nodes available")
        self.start_vertex_menu["menu"].add_command(label="No nodes available")
        self.delete_node_menu["menu"].add_command(label="No nodes available")
        self.delete_edge_menu["menu"].add_command(label="No edges available")

        # Disable "Reset Graph" button
        self.reset_button.configure(state='disabled')

        # Show the placeholder text
        self.show_placeholder_text()


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

        



    ##########################################
    # All of below is for Prim's integration #
    ##########################################
    

    # Extracts the graph data from the drawn nodes and edges
    def extract_graph_data(self):
        V = set(node.identifier for node in self.nodes)
        E = set()
        W = {}

        for edge in self.edges:
            start_id = edge.start_node.identifier
            end_id = edge.end_node.identifier

            E.add((start_id, end_id))
            W[(start_id, end_id)] = edge.weight

        print(f"Vertices: {V}")
        print(f"Edges: {E}")
        print(f"Weights: {W}")

        return V, E, W
    

    # prim_minimum_spanning_tree function from correctPrims.py
    def prim_minimum_spanning_tree(self, graph):
        V, E, W = graph
        Te = set()  # Set of edges in the minimum spanning tree
        Tv = set()  # Set of visited vertices
        u = self.start_vertex_var.get() if self.start_vertex_var.get() in V else next(iter(V))  # Starting vertex
        L = {}      # Dictionary for L values of each edge

        Tv.add(u)           #Adding initial vertex to Tv
        
        # Initialize L(v) for all vertices
        for v in V - Tv:
            if (u, v) in E:
                L[v] = W[(u, v)]
            elif (v, u) in E:
                L[v] = W[(v, u)]
            else:
                L[v] = float("inf")

        print("Vertices: ", V)
        print("Edges: ", E)
        print("Weights: ", W)

        print("\nStarting with vertex:", u)

        self.update_info_text(f"Starting with vertex {u}\n\n")
        self.update_info_text(f"Initial L table for vertex {u}: {L}\n\n")
        yield

        total_weight = 0

        while Tv != V:
            # Find w: L(w) = min{L(v) | v ∈ (V − Tv)}
            w = min((v for v in (V - Tv)), key=lambda v: L[v])                
            
            self.update_info_text(f"Choosing next vertex with smallest L value: {w}\n\n")

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
            # Update TV
            Tv.add(w)

            self.update_info_text(f"Added edge {e} to the minimum spanning tree.\n\n")
            yield e, w  # Pause the algorithm and return the added edge

            print(f"\nAdded edge {e} to the minimum spanning tree.")
            print("Current minimum spanning tree edges:", Te)

            # Update L(v) for v ∈ (V − Tv) if there is an edge (w, v) or (v, w) in E with weight less than L(v)
            for v in (V - Tv):
                if (w, v) in E and W[(w, v)] < L[v]:
                    L[v] = W[(w, v)]
                elif (v, w) in E and W[(v, w)] < L[v]:
                    L[v] = W[(v, w)]

            print("\nUpdated L table after including vertex", w, ":", L)

            
            self.update_info_text(f"Updated L table: {L}\n\n")
            yield
            
            self.update_info_text(f"Current visited vertices: {Tv}\n\n")
            self.update_info_text(f"Updated minimum spanning tree edges: {Te}\n\n")
            yield
        
        self.update_info_text(f"All vertices have been visited, therefore...\n\n-----Your final minimum spanning tree is----- \n\n {Te}\n\n The total weight of your MST is: {total_weight}\n\n---------------------------------------------")
        return Te
    
    # For highlighting MST edges
    def visualize_mst(self, edge_added):
        # Highlight only the added edge
        start_id, end_id = edge_added
        for edge in self.edges:
            if (edge.start_node.identifier == start_id and edge.end_node.identifier == end_id) or \
                (edge.start_node.identifier == end_id and edge.end_node.identifier == start_id):
                self.canvas.itemconfig(edge.line_id, fill="orange", width=3)
                break  # Once the edge is found and highlighted, exit the loop

    # For highlighting MST nodes
    def highlight_node(self, node_identifier):    
        # Find the node by its identifier and update its color to indicate it's been visited
        for node in self.nodes:
            if self.start_vertex_var.get() == node.identifier:
                self.canvas.itemconfig(node.id, fill="orange", outline = "green")  # Outline starting node green to distinguish * MAKE OUTLINE THICKER *
            elif node.identifier == node_identifier:
                self.canvas.itemconfig(node.id, fill="orange", outline = "black")  # Colour visited node orange
                break  # Break out of the loop once the node is found and highlighted

    # For starting Prim's on graph
    def generate_mst(self):
        try:
            # Clears the info text widget 
            self.info_text_widget.configure(state='normal')
            self.info_text_widget.delete("1.0", tk.END)
            self.info_text_widget.configure(state='disabled')  

            self.start_time = time.time()  # Record start time
            if len(self.nodes) == 0:
                raise ValueError("Please add nodes and edges to the canvas.")
            
            # Reset colors of nodes and edges
            for node in self.nodes:
                self.canvas.itemconfig(node.id, fill="blue")  # Reset node color to blue
            for edge in self.edges:
                self.canvas.itemconfig(edge.line_id, width=2, fill="black")  # Reset edge color to black
            
            # Below for loop should be put into a method and called as it is reused in multiple places
            for edge in self.edges:     # If canvas is clicked when only showing MST edges, show all edges
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

            self.toggle_mst_button.configure(state='disabled', text='Show MST only')  # Disabled if Run Prims is clicked 

            V, E, W = self.extract_graph_data()

            if not self.is_graph_connected(V, E):   # Check if the graph is connected
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
    

    # Checks if the graph is connected using depth-first search
    def is_graph_connected(self, V, E):
        if not V:
            return False    # Return false if no vertices are present

        visited = set()     # For tracking all V that have been visited

        def dfs(v):
            if v in visited:
                return      # Returns immediately if vertex is in visited to stop duplicate additions
            visited.add(v)  # Adds v to visited if it was previously unvisited
            for u in V:
                if (v, u) in E or (u, v) in E:  # Checks if there is an edge between two vertices,
                    dfs(u)                      # if so, dfs recursively called

        # Start depth-first search from the first node in V
        dfs(next(iter(V)))

        return visited == V #  Only returns true if list of visited vertices matches original list of vertices, this would mean graph is connected
    
    # For proceeding through the algorithm with Next Step button
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


if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()
