import tkinter as tk
from tkinter import Canvas, Label, Button, OptionMenu, StringVar, Entry
import random

class Node:
    def __init__(self, x, y, identifier):
        self.x = x
        self.y = y
        self.id = None  # To store the ID of the oval on the canvas
        self.text_id = None  # To store the ID of the text on the canvas
        self.identifier = identifier  # To store the identifier of the node


class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.line_id = None  # To store the ID of the line on the canvas
        self.text_id = None  # To store the ID of the text label for the weight


class GraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prim's Algorithm Visualizer")

        self.canvas = Canvas(self, width=800, height=600, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=8, sticky='nsew')  

        self.nodes = []  # List to store nodes
        self.edges = []  # List to store edges

        self.selected_node = None
        self.drag_start_pos = None

        # UI components
        self.status_label = Label(self, text="Graph Drawing Mode")
        self.status_label.grid(row=0, column=0, columnspan=4, sticky='nw')

        # Dropdown menus and weight input
        self.start_node_var = StringVar(self)
        self.end_node_var = StringVar(self)
        self.weight_var = StringVar(self)

        # Dropdown menus
        self.start_node_menu = OptionMenu(self, self.start_node_var, "Select Node")
        self.start_node_menu.grid(row=0, column=1, sticky='e')

        self.end_node_menu = OptionMenu(self, self.end_node_var, "Select Node")
        self.end_node_menu.grid(row=1, column=1, sticky='e')

        # Weight entry field
        self.weight_entry = Entry(self, textvariable=self.weight_var)
        self.weight_entry.grid(row=2, column=1, sticky='e')

        # Labels for the dropdown menus and weight input
        self.start_node_label = Label(self, text="Start Node:")
        self.start_node_label.grid(row=0, column=1, sticky='ne')

        self.end_node_label = Label(self, text="End Node:")
        self.end_node_label.grid(row=1, column=1, sticky='ne')

        self.weight_label = Label(self, text="Weight:")
        self.weight_label.grid(row=2, column=1, sticky='ne')
        
        # Buttons
        self.create_edge_button = Button(self, text="Create Edge", command=self.manual_create_edge)
        self.create_edge_button.grid(row=3, column=1, columnspan=2, pady=5)

        self.finalize_button = Button(self, text="Run Prim's", command=self.generate_mst)
        self.finalize_button.grid(row=4, column=1, columnspan=2, pady=5)

        self.reset_button = Button(self, text="Reset Graph", command=self.reset_graph)
        self.reset_button.grid(row=5, column=1, columnspan=2, pady=5)

        self.random_graph_button = Button(self, text="Generate Random Graph", command=self.generate_random_graph)
        self.random_graph_button.grid(row=6, column=1, columnspan=2, pady=5)


        # Text widget to display the L table and other information
        self.info_text_widget = tk.Text(self, height=10, width=50)
        self.info_text_widget.grid(row=8, column=0, columnspan=4)

        # Add a "Next Step" button to proceed through the algorithm
        self.next_step_button = Button(self, text="Next Step", command=self.next_step)
        self.next_step_button.grid(row=9, column=0, columnspan=2, pady=5)
        self.next_step_button.config(state='disabled')  # Disabled by default, enabled when Prim's starts

        self.node_counter = 0  # Counter to keep track of the number of nodes

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.left_click_handler)
        self.canvas.bind("<B1-Motion>", self.drag_handler)
        self.canvas.bind("<ButtonRelease-1>", self.release_handler)
    
        # Bind right-click events
        self.canvas.bind("<Button-3>", self.right_click_handler)

        # Configure the grid layout to allow for resizing
        self.columnconfigure(1, weight=1)
        for i in range(8):  # Assuming 8 is the number of rows you are using
            self.rowconfigure(i, weight=1)


    def generate_node_identifier(self):
        # Generates a unique identifier for each node
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        quotient, remainder = divmod(self.node_counter, len(alphabet))
        if quotient == 0:
            return alphabet[remainder]
        else:
            return self.generate_node_identifier(quotient - 1) + alphabet[remainder]

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


    def manual_create_edge(self):
        try:
            start_node_identifier = self.start_node_var.get()  # Get the identifier of the start node
            end_node_identifier = self.end_node_var.get()  # Get the identifier of the end node
            weight = float(self.weight_var.get())  # This might throw ValueError if not a valid float

            start_node = next((node for node in self.nodes if node.identifier == start_node_identifier), None)
            end_node = next((node for node in self.nodes if node.identifier == end_node_identifier), None)

            if not start_node or not end_node:
                raise ValueError("Invalid node selection.")

            if start_node == end_node:
                raise ValueError("Start node and end node cannot be the same.")
            
            if weight <= 0:
                raise ValueError("Weight must be a positive number.")

            edge = Edge(start_node, end_node, weight)
            self.create_edge(edge)
        except ValueError as e:
            print(f"Error creating edge: {e}")
            self.status_label.config(text=f"Error: {e}")


    def left_click_handler(self, event):
        x, y = event.x, event.y
        clicked_node = self.find_node(x, y)

        if clicked_node:
            # If a node is clicked, initiate the drag process
            self.selected_node = clicked_node
            self.drag_start_pos = (x, y)
        else:
            # If no node is clicked, create a new node
            node_identifier = self.generate_node_identifier()
            new_node = Node(x, y, node_identifier)
            new_node.id = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue")
            new_node.text_id = self.canvas.create_text(x, y, text=node_identifier, font=("Arial", 12))
            self.nodes.append(new_node)
            self.node_counter += 1
            self.update_node_options()  # Update dropdown menus when a new node is added

    def right_click_handler(self, event):
        x, y = event.x, event.y
        clicked_node = self.find_node(x, y)

        if clicked_node:
            # If a node is right-clicked, initiate the edge creation process
            self.selected_node = clicked_node
            self.selected_edge = Edge(clicked_node, None, 0)
            self.status_label.config(text="Drag to another node to create or connect an edge")

            # Bind additional events for right-click
            self.canvas.bind("<B2-Motion>", self.edge_drag_handler)
            self.canvas.bind("<ButtonRelease-2>", self.edge_release_handler)
            print("Right-clicked on an existing node")  

    def edge_drag_handler(self, event):
        x, y = event.x, event.y

        if hasattr(self, 'selected_edge') and self.selected_edge:
            # If an edge is being created or connected, update its end position
            self.canvas.delete(self.selected_edge.line_id)  # Delete the previous line
            self.selected_edge.end_node = Node(x, y)
            self.selected_edge.line_id = self.canvas.create_line(
                self.selected_edge.start_node.x, self.selected_edge.start_node.y,
                x, y, width=2, fill="black"  # Set the color to black
            )

    def edge_release_handler(self, event):
        x, y = event.x, event.y
        released_node = self.find_node(x, y)

        if self.selected_node and released_node and self.selected_node != released_node:
            if hasattr(self, 'selected_edge') and self.selected_edge:
                # If released on an existing node, create an edge
                self.selected_edge.end_node = released_node
                self.create_edge(self.selected_edge)
                self.status_label.config(text="Graph Drawing Mode")
            else:
                # If released on an empty area, delete the temporary edge
                if hasattr(self, 'selected_edge') and self.selected_edge:
                    self.canvas.delete(self.selected_edge.line_id)

        # Reset selected node and drag start position
        self.selected_node = None
        self.drag_start_pos = None

    # Handles scenarios where user drags nodes around
    def drag_handler(self, event):
        if self.selected_node:
            # New x, y coordinates after the drag
            new_x, new_y = event.x, event.y
        
            # Calculate the deltas
            dx = new_x - self.selected_node.x
            dy = new_y - self.selected_node.y

            # Update the position of the selected node
            self.selected_node.x = new_x
            self.selected_node.y = new_y
        
            # Move the node
            self.canvas.move(self.selected_node.id, dx, dy)
        
            # Move the text identifier along with the node
            self.canvas.move(self.selected_node.text_id, dx, dy)
        
            # Update connected edges
            for edge in self.edges:
                if edge.start_node == self.selected_node:
                    # If the selected node is the start node, update the start position of the edge
                    self.canvas.coords(edge.line_id, new_x, new_y, edge.end_node.x, edge.end_node.y)
                
                    # Also update the position of the weight label
                    mid_x = (new_x + edge.end_node.x) / 2
                    mid_y = (new_y + edge.end_node.y) / 2
                    self.canvas.coords(edge.text_id, mid_x, mid_y)
                
                elif edge.end_node == self.selected_node:
                    # If the selected node is the end node, update the end position of the edge
                    self.canvas.coords(edge.line_id, edge.start_node.x, edge.start_node.y, new_x, new_y)
                
                    # Also update the position of the weight label
                    mid_x = (edge.start_node.x + new_x) / 2
                    mid_y = (edge.start_node.y + new_y) / 2
                    self.canvas.coords(edge.text_id, mid_x, mid_y)
        
            # Bring the node and its text identifier to the top of the stack
            self.canvas.tag_raise(self.selected_node.id)
            self.canvas.tag_raise(self.selected_node.text_id)


    def release_handler(self, event):
        x, y = event.x, event.y
        released_node = self.find_node(x, y)

        if self.selected_node and released_node and self.selected_node != released_node:
            if hasattr(self, 'selected_edge') and self.selected_edge:
                # If released on an existing node, create an edge
                self.selected_edge.end_node = released_node
                self.create_edge(self.selected_edge)
                self.status_label.config(text="Graph Drawing Mode")
            else:
                # If released on an empty area, delete the temporary edge
                if hasattr(self, 'selected_edge') and self.selected_edge:
                    self.canvas.delete(self.selected_edge.line_id)

        # Reset selected node and drag start position
        self.selected_node = None
        self.drag_start_pos = None

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

        # Offset for the weight text to appear above the line
        text_offset = 20  # You can adjust this value as needed

        # Calculate the position for the weight text
        weight_text_x = mid_x
        weight_text_y = mid_y - text_offset

        # Create the text for the weight
        edge.text_id = self.canvas.create_text(weight_text_x, weight_text_y, text=str(edge.weight), font=("Arial", 12), fill="black")

        self.edges.append(edge)

        for node in self.nodes:
            self.canvas.tag_raise(node.id)
            self.canvas.tag_raise(node.text_id)

    # Finds the node that was clicked on for drag_handler and release_handler
    def find_node(self, x, y):
        for node in self.nodes:
            if (node.x - 10) <= x <= (node.x + 10) and (node.y - 10) <= y <= (node.y + 10):
                return node
        return None
    
    # Generates a random graph on the canvas to save user time
    def generate_random_graph(self):
        self.reset_graph()  # Clear the existing graph
        num_nodes = random.randint(3, 6)  # Choose a random number of nodes

        # Create random nodes
        for _ in range(num_nodes):
            x, y = random.randint(20, 780), random.randint(20, 580)  # Random position within canvas
            node_identifier = self.generate_node_identifier()
            new_node = Node(x, y, node_identifier)
            new_node.id = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue")
            new_node.text_id = self.canvas.create_text(x, y, text=node_identifier, font=("Arial", 12))
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
            start_node, end_node = random.sample(self.nodes, 2)  # Select two distinct nodes
            # Ensure uniqueness of edges
            if (start_node.identifier, end_node.identifier) not in created_edges and \
            (end_node.identifier, start_node.identifier) not in created_edges:

                weight = random.randint(1, 10)  # Random weight
                new_edge = Edge(start_node, end_node, weight)
                self.create_edge(new_edge)
                created_edges.add((start_node.identifier, end_node.identifier))



    def reset_graph(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Reset the lists
        self.nodes = []
        self.edges = []

        # Reset the node counter and update dropdown menus
        self.node_counter = 0
        self.update_node_options()

        # Reset UI components if necessary
        self.status_label.config(text="Graph Drawing Mode")

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

        return V, E, W
    
    # prim_minimum_spanning_tree function from correctPrims.py
    def prim_minimum_spanning_tree(self, graph, start_vertex):
        V, E, W = graph
        Te = set()  # Set of edges in the minimum spanning tree
        Tv = set()  # Set of visited vertices
        u = start_vertex  # Starting vertex
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

        self.update_info_text(f"Initial L table for vertex {u}: {L}\n")
        yield None, u # Pause the algorithm 

        while Tv != V:
            # Find w: L(w) = min{L(v) | v ∈ (V − Tv)}
            w = min((v for v in (V - Tv)), key=lambda v: L[v])

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
            Te.add(e)

            # Update TV
            Tv.add(w)

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
            self.update_info_text(f"Updated L table: {L}\nCurrent MST edges: {Te}\n")
            yield

        return Te
    
    def visualize_mst(self, edge_added):
        # Highlight only the added edge
        start_id, end_id = edge_added
        for edge in self.edges:
            if (edge.start_node.identifier == start_id and edge.end_node.identifier == end_id) or \
                (edge.start_node.identifier == end_id and edge.end_node.identifier == start_id):
                self.canvas.itemconfig(edge.line_id, fill="orange", width=3)
                break  # Once the edge is found and highlighted, exit the loop

    def highlight_node(self, node_identifier):
        # Find the node by its identifier and update its color to indicate it's been visited
        for node in self.nodes:
            if node.identifier == node_identifier:
                self.canvas.itemconfig(node.id, fill="orange")  # Colour visited node orange
                break  # Break out of the loop once the node is found and highlighted

    
    def generate_mst(self):
        try:
            if len(self.nodes) == 0:
                raise ValueError("No nodes in the graph.")

            V, E, W = self.extract_graph_data()

            # Get the start node identifier from the dropdown
            start_node_identifier = self.start_node_var.get()  
            if start_node_identifier == "Select Node":
                raise ValueError("Please select a start node for Prim's algorithm.")

            if not self.is_graph_connected(V, E):
                raise ValueError("Graph is disconnected. Prim's algorithm requires a connected graph.")

            # Initialize Prim's algorithm
            self.prim_generator = self.prim_minimum_spanning_tree((V, E, W), start_node_identifier)
            self.next_step_button.config(state='normal')  # Enable "Next Step" button

            # Start the first step of Prim's algorithm
            self.next_step()

        except ValueError as e:
            print(f"Error: {e}")
            self.status_label.config(text=f"Error: {e}")
    
    # Checks if the graph is connected using depth-first search
    def is_graph_connected(self, V, E):
        if not V:
            return False

        visited = set()

        def dfs(v):
            if v in visited:
                return
            visited.add(v)
            for u in V:
                if (v, u) in E or (u, v) in E:
                    dfs(u)

        # Start DFS from the first node in V
        dfs(next(iter(V)))

        return visited == V
    
    def next_step(self):
        try:
            # Proceed to the next step in the generator, which should return a pair (edge_added, node_visited)
            edge_added, node_visited = next(self.prim_generator)
        
            # Highlight the added edge
            if edge_added:
                self.visualize_mst(edge_added)
        
            # Highlight the visited node
            if node_visited:
                self.highlight_node(node_visited)

        except StopIteration:
            # Algorithm is complete if it gets here
            self.next_step_button.config(state='disabled')  # Disable the button since the algorithm is finished
            self.update_info_text("Prim's algorithm is complete.\n")

    def update_info_text(self, message):
        self.info_text_widget.insert(tk.END, message)
        self.info_text_widget.see(tk.END)  


if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()
