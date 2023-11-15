import tkinter as tk
from tkinter import Canvas, Label, Button

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = None  # To store the ID of the oval on the canvas

class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.line_id = None  # To store the ID of the line on the canvas

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

        self.finalize_button = Button(self, text="Finalize Graph", command=self.finalize_graph)
        self.finalize_button.pack()

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.click_handler)
        self.canvas.bind("<B1-Motion>", self.drag_handler)
        self.canvas.bind("<ButtonRelease-1>", self.release_handler)

    def click_handler(self, event):
        x, y = event.x, event.y
        clicked_node = self.find_node(x, y)

        if clicked_node:
            # If a node is clicked, initiate the drag process
            self.selected_node = clicked_node
            self.drag_start_pos = (x, y)
        else:
            # If no node is clicked, create a new node
            new_node = Node(x, y)
            new_node.id = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue")
            self.nodes.append(new_node)

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
            # If released on an existing node, create an edge
            edge = Edge(self.selected_node, released_node, 0)
            self.create_edge(edge)

        # Reset selected node and drag start position
        self.selected_node = None
        self.drag_start_pos = None

    def create_edge(self, edge):
        # Create the edge and add it to the list
        self.edges.append(edge)
        self.canvas.create_line(
            edge.start_node.x, edge.start_node.y,
            edge.end_node.x, edge.end_node.y, width=2, fill="black"
        )

    def find_node(self, x, y):
        for node in self.nodes:
            if (node.x - 10) <= x <= (node.x + 10) and (node.y - 10) <= y <= (node.y + 10):
                return node
        return None

    def finalize_graph(self):
        # Implement this method to indicate that the graph is finalized
        # You can disable further editing or perform any necessary actions
        self.status_label.config(text="Graph Finalized")

if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()









