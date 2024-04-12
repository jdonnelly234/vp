import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import platform
import itertools
import numpy as np
import psutil
import os

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
        self.edges = []
        self.E = {}
        self.node_counter = 0  # Counter to keep track of the number of nodes
        self.processor = platform.processor()

        
    def analyse(self, analysis_type):
        if analysis_type == "comparisons":
            max_nodes = int(self.comp_slider.get())
            steps = int(self.comp_steps_slider.get())
        elif analysis_type == "execution_time":
            max_nodes = int(self.exec_slider.get())
            steps = int(self.exec_steps_slider.get())
        else:
            raise ValueError("Invalid analysis type provided. Choose either 'comparisons' or 'execution_time'.")

        self.clear_graph()
        self.clear_metrics()

        initial_range = list(range(2, max_nodes, steps))
        if max_nodes - initial_range[-1] > steps / 2:
            initial_range.append(max_nodes)
        
        nodes = initial_range
        comparisons = []
        execution_times = []

        for n in nodes:
            graph = self.generate_complete_graph(n)
            start_time = time.perf_counter()
            _, num_comparisons = prim_minimum_spanning_tree(graph)
            end_time = time.perf_counter()

            comparisons.append(num_comparisons)
            execution_time = end_time - start_time
            execution_times.append(execution_time)
            print(f"Prim's execution time on graph with {n} nodes: {execution_time} seconds")

        if analysis_type == "comparisons":
            self.display_complexity_metrics(max_nodes, int((max_nodes * (max_nodes - 1)) / 2) , _, (execution_times[len(execution_times) - 1])/len(execution_times), comparisons[-1], self.processor)
            self.visualize_complexity(nodes, comparisons)
        elif analysis_type == "execution_time":
            self.display_complexity_metrics(max_nodes, int((max_nodes * (max_nodes - 1)) / 2), _, (execution_times[len(execution_times) - 1])/len(execution_times), num_comparisons, self.processor)
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
        if num_nodes < 2:
            raise ValueError("Number of nodes must be at least 2 to generate a graph.")
        
        start_time = time.time()
        print(f"Generating graph with {num_nodes} nodes...")

        nodes = [generate_node_identifier(i) for i in range(num_nodes)]
        edges = list(itertools.combinations(nodes, 2))
        weights = [1] * len(edges)  # This creates a list with a "1" for each edge

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
        ax.plot(nodes, nsquared, label='$O(n^2)$ (Theoretical)', linestyle='dotted', color='blue', marker='.')

        # Labeling the plot
        ax.set_xlabel("Number of nodes")
        if comparisons[len(comparisons) - 1] > 900000:
            ax.set_ylabel("Number of comparisons (million)")
        else:
            ax.set_ylabel("Number of comparisons")
        ax.set_title(f"Time complexity of Prim's for a series of complete graphs up to {int(self.comp_slider.get())} nodes.")
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
        ax.plot(nodes, execution_times, label='Your graph', color='red', linestyle="dashed", marker='o')

        # Fit the O(n^2) curve
        # Use a polynomial of degree 2 because we're fitting an n^2 curve
        coefficients = np.polyfit(nodes, execution_times, 2)
        # Generate a polynomial function from the coefficients
        polynomial = np.poly1d(coefficients)
        # Calculate the fitted y-values
        fitted_execution_times = polynomial(nodes)

        # Plot the fitted O(n^2) curve
        ax.plot(nodes, fitted_execution_times, label='$O(n^2)$ (Theoretical)', linestyle='dotted', color='blue', marker='.')

        # Labeling the plot
        ax.set_xlabel("Number of nodes")
        ax.set_ylabel("Execution time (s)")
        ax.set_title(f"Execution time of Prim's algorithm on a series of complete graphs up to {int(self.exec_slider.get())} nodes.")
        ax.legend()
        ax.grid(True)

        # Embed the figure in the right frame (assuming 'self.right_frame' is your designated area for plots)
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def display_complexity_metrics(self, num_nodes, edges, mst_edges, execution_time, num_comparisons, processor):
        # Create and pack labels for each metric with headings
        ctk.CTkLabel(self.lower_left_frame, text=f"Maximum number of nodes specified: {num_nodes}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.lower_left_frame, text=f"Number of edges in max node graph: {edges}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.lower_left_frame, text=f"Number of edges in MST of max node graph: {int(num_nodes - 1)}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.lower_left_frame, text=f"Average Prim's execution time: {execution_time:.6f} seconds", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)
        ctk.CTkLabel(self.lower_left_frame, text=f"Number of comparisons: {num_comparisons}", font = COMPLEXITY_SUBTITLE_FONT, anchor='center').pack(side=tk.TOP, fill=tk.X)

    
    def return_to_main_menu(self):
        self.destroy()
        from vp_main_gui import MainMenu    #Importing here to avoid circular import
        main_menu = MainMenu()  
        main_menu.mainloop() 

