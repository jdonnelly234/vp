import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import platform
import subprocess

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
        self.processor = platform.processor()

        self.generate_and_analyse_graph()

        

    def generate_and_analyse_graph(self):
        # Clear previous graph and metrics
        self.clear_graph()
        self.clear_metrics()

        # Prompt the user for the number of nodes
        num_nodes = simpledialog.askinteger("Number of Nodes", "Enter the number of nodes:", minvalue=5, maxvalue=250, parent=self)
        if num_nodes is None:
            return

        # Generate a complete graph with the specified number of nodes
        graph = self.generate_complete_graph(num_nodes)

        # Run Prim's algorithm on the generated graph
        start_time = time.time()
        minimum_spanning_tree, num_comparisons = prim_minimum_spanning_tree(graph)
        end_time = time.time()
        execution_time = end_time - start_time

        # Display complexity metrics
        self.display_complexity_metrics(num_nodes, self.edges, minimum_spanning_tree, execution_time, num_comparisons, self.processor)

        # Visualize the complexity
        self.visualize_complexity(num_nodes)

        restart_button = ctk.CTkButton(self.left_frame, text="Restart", command=self.generate_and_analyse_graph)
        restart_button.pack(side=tk.BOTTOM, pady=(50, 10))

        # Button to return to the main menu
        return_button = ctk.CTkButton(self.left_frame, text="Return to Main Menu", command=self.return_to_main_menu)
        return_button.pack(side=tk.BOTTOM, pady=(50,10))
    
    def clear_graph(self):
        # Clear graph visualization
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def clear_metrics(self):
        # Clear complexity metrics
        for widget in self.left_frame.winfo_children():
            widget.destroy()

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

        # Create edges between every pair of distinct nodes
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
        ax.set_title(f"Time complexity of Prim's for a complete graph with {num_nodes} nodes")
        ax.grid()

        # Embed the figure in the right frame
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def display_complexity_metrics(self, num_nodes, edges, mst_edges, execution_time, num_comparisons, processor):
        # Create and pack labels for each metric with headings
        ctk.CTkLabel(self.left_frame, text="Complexity Metrics", font=TITLE_FONT).pack(side=tk.TOP, pady=(10, 50))
        ctk.CTkLabel(self.left_frame, text=f"Processor: {processor}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP)
        ctk.CTkLabel(self.left_frame, text=f"Number of Nodes: {num_nodes}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.left_frame, text=f"Number of edges in original graph: {len(edges)}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.left_frame, text=f"Number of edges in MST: {len(mst_edges)}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.left_frame, text=f"Algorithm Execution Time: {execution_time:.6f} seconds", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.left_frame, text=f"Number of Comparisons: {num_comparisons}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)

    
    def return_to_main_menu(self):
        self.destroy()
        from vp_main_gui import MainMenu    #Importing here to avoid circular import
        main_menu = MainMenu()  
        main_menu.mainloop() 

