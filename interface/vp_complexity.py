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
import numpy as np

from node import Node
from edge import Edge
from vp_complexity_gui import ComplexityGUI
from utils import *
from config import *

from vp_prims_algorithm import prim_minimum_spanning_tree
from vp_priority_q_prims import prim_minimum_spanning_tree_with_priority_queue

class ComplexityAnalyser(ComplexityGUI):
    def __init__(self):
        super().__init__()

        self.nodes = []  # List to store nodes
        self.edges = []  # List to store edges
        self.node_counter = 0  # Counter to keep track of the number of nodes
        self.processor = platform.processor()

        
    def analyse_comparisons(self):
        max_nodes = int(self.comp_slider.get())
        steps = int(self.comp_steps_slider.get())

        self.clear_graph()
        self.clear_metrics()

        nodes = list(range(2, max_nodes + 1, steps))  # Start from 2 to avoid graphs with less than 2 nodes

        nodes.append(max_nodes)
        print(f"Steps: {steps}")
        print(f"Nodes: {nodes}")
        comparisons = []

        for n in nodes:
            graph = self.generate_complete_graph(n)
            start_time = time.time()
            _, num_comparisons = prim_minimum_spanning_tree(graph)
            end_time = time.time()
            comparisons.append(num_comparisons)

        print(f"Comparisons: {comparisons}")

        execution_time = end_time - start_time  # This would be more meaningful if averaged over runs

        # Display complexity metrics for the last measured node count, 
        self.display_complexity_metrics(nodes[-1], self.edges, _, execution_time, comparisons[-1], self.processor)

        # You might need to adjust the visualization function if it needs to handle varying numbers of nodes
        self.visualize_complexity(nodes, comparisons)


    def analyse_execution_time(self):
        max_nodes = int(self.exec_slider.get())  
        steps = int(self.exec_steps_slider.get())
        # Clear previous graph and metrics
        self.clear_graph()
        self.clear_metrics()

        nodes = list(range(2, max_nodes + 1, steps))  # Start from 2 to avoid graphs with less than 2 nodes
        nodes.append(max_nodes)
        print(f"Steps: {steps}")
        print(f"Nodes: {nodes}")
        execution_times = []
        
        for n in nodes:
            graph = self.generate_complete_graph(n)
            start_time = time.perf_counter()
            _, num_comparisons = prim_minimum_spanning_tree_with_priority_queue(graph)  # Ignore the result, just measure time
            end_time = time.perf_counter()
            execution_times.append(end_time - start_time)
            print(f"Prim's execution time on graph with {n} nodes: {end_time - start_time} seconds")
        
        # Display complexity metrics
        self.display_complexity_metrics(nodes[-1], self.edges, _, (execution_times[len(execution_times) - 1])/len(execution_times), num_comparisons, self.processor)

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
        start_time = time.time()
        print(f"Generating graph with {num_nodes} nodes...")

        nodes = [generate_node_identifier(i) for i in range(num_nodes)]
        edges = list(itertools.combinations(nodes, 2))
        weights = np.random.randint(1, 11, size=len(edges))

        # Combine nodes and weights
        E = {(start, end): weight for (start, end), weight in zip(edges, weights)}        

        end_time = time.time()
        print(f"Time to generate graph with {num_nodes} nodes: {end_time - start_time} seconds")
        
        return nodes, edges, E
    
    
    def visualize_complexity(self, nodes, comparisons):
        # Create a Matplotlib figure and axis for plotting
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)

        print(f"Comaprisons in visualising complexity function: {comparisons}")
        # Plot the number of comparisons against the number of nodes
        ax.plot(nodes, comparisons, label='Your graph', color='red', marker='o')

        # Optionally, plot theoretical complexity for comparison, e.g., O(n^2) or O(n log n), depending on the expected complexity
        # For demonstration, plotting an n^2 complexity curve
        nsquared = [n**2 for n in nodes]
        ax.plot(nodes, nsquared, label='n^2 (Theoretical)', linestyle='--', color='blue')

        # Labeling the plot
        ax.set_xlabel("Number of nodes")
        if comparisons[len(comparisons) - 1] > 900000:
            ax.set_ylabel("Number of comparisons (million)")
        else:
            ax.set_ylabel("Number of comparisons")
        ax.set_title(f"Time complexity of Prim's for a complete graph with {int(self.comp_slider.get())} nodes")
        ax.legend()
        ax.grid(True)

        # Embed the figure in the right frame (assuming 'self.right_frame' is your designated area for plots)
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    

    def visualize_execution_time(self, nodes, execution_times):
        # Create a Matplotlib figure and axis for plotting
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)

        print(f"Execution times: {execution_times}")
        # Plot the number of comparisons against the number of nodes
        ax.plot(nodes, execution_times, label='Your graph', color='red', marker='o')

        # Optionally, plot theoretical complexity for comparison, e.g., O(n^2) or O(n log n), depending on the expected complexity
        # For demonstration, plotting an n^2 complexity curve
        #nsquared = [n**2 for n in nodes]
        #ax.plot(nodes, nsquared, label='n^2 (Theoretical)', linestyle='--', color='blue')

        # Labeling the plot
        ax.set_xlabel("Number of nodes")
        ax.set_ylabel("Execution time (s)")
        ax.set_title(f"Execution time of Prim's for a complete graph with {int(self.exec_slider.get())} nodes")
        ax.legend()
        ax.grid(True)

        # Embed the figure in the right frame (assuming 'self.right_frame' is your designated area for plots)
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

