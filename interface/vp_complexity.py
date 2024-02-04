import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from node import Node
from edge import Edge
from vp_complexity_gui import ComplexityGUI
from utils import *
from config import *

from vp_prims_algorithm import prim_minimum_spanning_tree

class ComplexityAnalyser(ComplexityGUI):
    def __init__(self):
        super().__init__()

        self.nodes = []  # List to store nodes
        self.edges = []  # List to store edges
        self.node_counter = 0  # Counter to keep track of the number of nodes

        # Prompt the user for the number of nodes 
        num_nodes = simpledialog.askinteger("Number of Nodes", "Enter the number of nodes:", minvalue=10, maxvalue=100, parent=self)
        if num_nodes is None:
            return  

        # Generate a complete graph with the specified number of nodes
        graph = self.generate_complete_graph(num_nodes)

        print(graph)  

        # Run Prim's algorithm on the generated graph
        start_time = time.time()
        minimum_spanning_tree, num_comparisons = prim_minimum_spanning_tree(graph)
        end_time = time.time()
        execution_time = end_time - start_time

    
        complexity_info = f"Number of Nodes: {num_nodes}\n"
        complexity_info += f"Number of edges in original graph: {len(self.edges)}\n"
        complexity_info += f"Number of edges in MST: {len(minimum_spanning_tree)}\n"
        complexity_info += f"Algorithm Execution Time: {execution_time:.6f} seconds\n"
        complexity_info += f"Number of Comparisons: {num_comparisons}"

        self.display_complexity_metrics(complexity_info)

        self.visualize_complexity(num_nodes)



    def generate_complete_graph(self, num_nodes):
        # Reset to show correct number of nodes and comparisons on graph
        self.nodes = [] 
        self.edges = []  
        self.node_counter = 0  

        # Create num_nodes 
        for i in range(num_nodes):
            new_node = Node(0, 0, generate_node_identifier(self.node_counter))
            self.nodes.append(new_node)
            self.node_counter += 1

        # Create edges between every pair of distinct nodes to form a complete graph
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                start_node = self.nodes[i]
                end_node = self.nodes[j]
                weight = random.randint(1, 10)  
                new_edge = Edge(start_node, end_node, weight)
                self.edges.append(new_edge)
        
        return extract_graph_data(self.nodes, self.edges)   
    
    
    def visualize_complexity(self, num_nodes):
        comparisons = []  
        nodes = list(range(2, num_nodes + 1))  

        for n in nodes:
            graph = self.generate_complete_graph(n)
            _, num_comparisons = prim_minimum_spanning_tree(graph)
            comparisons.append(num_comparisons)

        nsquared = [n**2 for n in nodes]

        # Create a Matplotlib figure and axis
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)

        ax.plot(nodes, comparisons, label='Prims Algorithm', color='red')
        ax.plot(nodes, nsquared, linestyle='dashed', label="n^2")
        ax.set_xlabel("Number of nodes")
        ax.set_ylabel("Number of comparisons")
        ax.set_title("Prim's Algorithm Time Complexity for a complete graph with {num_nodes} nodes")
        ax.grid()

        # Embed the figure in the right frame
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def display_complexity_metrics(self, complexity_info):
        metrics_label = ctk.CTkLabel(self.left_frame, text=complexity_info)
        metrics_label.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

