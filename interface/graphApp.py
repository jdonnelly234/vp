import tkinter as tk
from tkinter import Canvas, Label, Button, OptionMenu, StringVar, Entry

class Node:
    def __init__(self, x, y, identifier):
        self.x = x
        self.y = y
        self.id = identifier  # To store the ID of the oval on the canvas
        self.id = None  # To store the ID of the oval on the canvas
        self.text_id = None  # To store the ID of the text on the canvas

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
        self.title("Graph Drawing App")

        self.canvas = Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack()

        self.nodes = []  # List to store nodes
        self.edges = []  # List to store edges

        self.selected_node = None
        self.drag_start_pos = None

        # UI components
        self.status_label = Label(self, text="Graph Drawing Mode")
        self.status_label.pack()

        # Dropdown menus and weight input
        self.start_node_var = StringVar(self)
        self.end_node_var = StringVar(self)
        self.weight_var = StringVar(self)

        # Initialize the dropdown menus with a default value
        self.start_node_menu = OptionMenu(self, self.start_node_var, "Select Node")
        self.start_node_menu.pack()

        self.end_node_menu = OptionMenu(self, self.end_node_var, "Select Node")
        self.end_node_menu.pack()

        self.weight_entry = Entry(self, textvariable=self.weight_var)
        self.weight_entry.pack()

        self.create_edge_button = Button(self, text="Create Edge", command=self.manual_create_edge)
        self.create_edge_button.pack()

        # Finalize Graph button
        self.finalize_button = Button(self, text="Finalize Graph", command=self.finalize_graph)
        self.finalize_button.pack()

        self.node_counter = 0  # Counter to keep track of the number of nodes
   
        # Reset Graph button
        self.reset_button = Button(self, text="Reset Graph", command=self.reset_graph)
        self.reset_button.pack()

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.left_click_handler)
        self.canvas.bind("<B1-Motion>", self.drag_handler)
        self.canvas.bind("<ButtonRelease-1>", self.release_handler)
    
        # Bind right-click events
        self.canvas.bind("<Button-3>", self.right_click_handler)


    def generate_node_identifier(self):
        # Generates a unique identifier for each node
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        quotient, remainder = divmod(self.node_counter, len(alphabet))
        if quotient == 0:
            return alphabet[remainder]
        else:
            return self.generate_node_identifier(quotient - 1) + alphabet[remainder]

    def update_node_options(self):
        # Update the options in the dropdown menus
        menu = self.start_node_menu["menu"]
        menu.delete(0, "end")
        for node in self.nodes:
            menu.add_command(label=f"Node {node.id}", command=tk._setit(self.start_node_var, f"Node {node.id}"))

        menu = self.end_node_menu["menu"]
        menu.delete(0, "end")
        for node in self.nodes:
            menu.add_command(label=f"Node {node.id}", command=tk._setit(self.end_node_var, f"Node {node.id}"))

    def manual_create_edge(self):
        # Create an edge from the selected options in the dropdown menus
        start_node_id = int(self.start_node_var.get().split()[1])
        end_node_id = int(self.end_node_var.get().split()[1])
        weight = float(self.weight_var.get())

        start_node = next(node for node in self.nodes if node.id == start_node_id)
        end_node = next(node for node in self.nodes if node.id == end_node_id)

        edge = Edge(start_node, end_node, weight)
        self.create_edge(edge)

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
            print("Right-clicked on an existing node")  # Add this line to print a message

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

    def drag_handler(self, event):
        if self.selected_node:
            x, y = event.x, event.y

            # Update the position of the selected node
            self.selected_node.x = x
            self.selected_node.y = y

            if self.drag_start_pos:
                # If a drag has started, update the position of the selected node
                self.canvas.move(self.selected_node.id, x - self.drag_start_pos[0], y - self.drag_start_pos[1])
                self.drag_start_pos = (x, y)

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

    def find_node(self, x, y):
        for node in self.nodes:
            if (node.x - 10) <= x <= (node.x + 10) and (node.y - 10) <= y <= (node.y + 10):
                return node
        return None

    def finalize_graph(self):
        # Implement this method to indicate that the graph is finalized
        # You can disable further editing or perform any necessary actions
        self.status_label.config(text="Graph Finalized")

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

if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()













