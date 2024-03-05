import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import platform
import itertools

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

        
    def analyse_comparisons(self):
        num_nodes = int(self.comp_slider.get())
        # Clear previous graph and metrics
        self.clear_graph()
        self.clear_metrics()

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


    def analyse_execution_time(self):
        num_nodes = int(self.exec_slider.get())  # Get the value from the execution time slider
        # Clear previous graph and metrics
        self.clear_graph()
        self.clear_metrics()

        execution_times = []
        nodes = list(range(2, num_nodes + 1))  # Start from 2 to avoid graphs with less than 2 nodes

        for n in nodes:
            graph = self.generate_complete_graph(n)
            start_time = time.perf_counter()
            _, num_comparisons = prim_minimum_spanning_tree(graph)  # Ignore the result, just measure time
            end_time = time.perf_counter()
            execution_times.append(end_time - start_time)
        
        # Display complexity metrics
        self.display_complexity_metrics(num_nodes, self.edges, _, execution_times[len(execution_times) - 1], num_comparisons, self.processor)

        self.visualize_execution_time(nodes, execution_times)
        
    
    def clear_graph(self):
        # Clear graph visualization
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def clear_metrics(self):
        # Clear complexity metrics within lower frame without destroying the frames themselves
        for widget in self.lower_left_frame.winfo_children():
            widget.destroy()

    def generate_complete_graph(self, num_nodes):
        # Reset to show correct number of nodes and comparisons on graph
        self.node_counter = 0  

        # Pre-allocate nodes list with placeholder nodes 
        self.nodes = [Node(0, 0, generate_node_identifier(i)) for i in range(num_nodes)]

        # Pre-allocate edges list and fill it using list comprehension
        self.edges = [
            Edge(self.nodes[i], self.nodes[j], random.randint(1, 10))
            for i, j in itertools.combinations(range(num_nodes), 2)
        ]

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
    

    def visualize_execution_time(self, nodes, execution_times):
        # Create a new Matplotlib figure and axis
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)

        ax.plot(nodes, execution_times, label='Execution Time', color='blue')
        ax.set_xlabel("Number of nodes")
        ax.set_ylabel("Execution time (seconds)")
        ax.set_title("Execution time of Prim's algorithm")
        ax.legend()
        ax.grid()

        # Embed the figure in the right frame
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def display_complexity_metrics(self, num_nodes, edges, mst_edges, execution_time, num_comparisons, processor):
        # Create and pack labels for each metric with headings
        ctk.CTkLabel(self.lower_left_frame, text=f"Processor: {processor}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP)
        ctk.CTkLabel(self.lower_left_frame, text=f"Number of Nodes: {num_nodes}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.lower_left_frame, text=f"Number of edges in original graph: {len(edges)}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.lower_left_frame, text=f"Number of edges in MST: {len(mst_edges)}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.lower_left_frame, text=f"Average Algorithm Execution Time: {execution_time:.6f} seconds", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.lower_left_frame, text=f"Number of Comparisons: {num_comparisons}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)

    
    def return_to_main_menu(self):
        self.destroy()
        from vp_main_gui import MainMenu    #Importing here to avoid circular import
        main_menu = MainMenu()  
        main_menu.mainloop() 

