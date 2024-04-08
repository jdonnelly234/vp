import unittest
from unittest.mock import MagicMock, mock_open, patch, call, create_autospec
from interface.vp_complexity import ComplexityAnalyser, Node, Edge
from interface.utils import *
from tkinter import Label, Frame
import itertools
from interface.vp_prims_algorithm import prim_minimum_spanning_tree
import time
import interface.config as config
import psutil
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt

class TestComplexityAnalyser(unittest.TestCase):
    print("###########COMPLEXITY ANALYSER UNIT TESTS###########\n") 

    def setUp(self) -> None:
        self.analyser = ComplexityAnalyser()
        self.analyser.comp_slider = MagicMock()
        self.analyser.comp_steps_slider = MagicMock()
        self.analyser.exec_slider = MagicMock()
        self.analyser.exec_steps_slider = MagicMock()

        # Mocking UI components that will be used or manipulated
        self.analyser.right_frame = MagicMock()
        self.analyser.lower_left_frame = MagicMock()
        

    # Test the instantiation of the ComplexityAnalyser class
    def test_analyser_instantiation(self):
        self.assertIsInstance(self.analyser, ComplexityAnalyser)
        self.assertEqual(self.analyser.nodes, [])
        self.assertEqual(self.analyser.edges, [])
        self.assertEqual(self.analyser.E, {})
        self.assertEqual(self.analyser.node_counter, 0)
    

    # Test analyse method correctly handles comparisons analysis
    def test_analyse_method_comparisons(self):
        # Setup common slider values
        self.analyser.comp_slider.get.return_value = 100
        self.analyser.comp_steps_slider.get.return_value = 10
        
        # Mocking methods called within analyse
        self.analyser.clear_graph = MagicMock()
        self.analyser.clear_metrics = MagicMock()
        self.analyser.generate_complete_graph = MagicMock()
        self.analyser.display_complexity_metrics = MagicMock()
        self.analyser.visualize_complexity = MagicMock()

        # Mock the return value of prim_minimum_spanning_tree to a fixed value to simplify test
        with patch('interface.vp_complexity.prim_minimum_spanning_tree', return_value=([], 10200)):
            # Mock time.perf_counter to simulate a fixed execution time of 0.0
            with patch('time.perf_counter', return_value=0.0):  
                self.analyser.analyse("comparisons")

                # Assertions and checks
                self.analyser.clear_graph.assert_called_once()
                self.analyser.clear_metrics.assert_called_once()
                self.analyser.generate_complete_graph.assert_called()
                self.analyser.display_complexity_metrics.assert_called()
                self.analyser.visualize_complexity.assert_called()

                self.assertEqual(self.analyser.generate_complete_graph.call_count, 11, "generate_complete_graph should be called 11 times based on slider settings")
                self.analyser.display_complexity_metrics.assert_called_with(100, 4950, [], 0.0, 10200, self.analyser.processor)
                self.analyser.visualize_complexity.assert_called_with([2, 12, 22, 32, 42, 52, 62, 72, 82, 92, 100], [10200] * 11)   # 11 comparison metrics generated since 11 calls to generate_complete_graph with subsequent calls to prim_minimum_spanning_tree



    # Test analyse method correctly handles execution time analysis
    def test_analyse_method_exec_time(self):
        # Setup common slider values
        self.analyser.exec_slider.get.return_value = 100
        self.analyser.exec_steps_slider.get.return_value = 10
        
        # Mocking methods called within analyse
        self.analyser.clear_graph = MagicMock()
        self.analyser.clear_metrics = MagicMock()
        self.analyser.generate_complete_graph = MagicMock()
        self.analyser.display_complexity_metrics = MagicMock()
        self.analyser.visualize_execution_time = MagicMock()

        # Mock the return value of prim_minimum_spanning_tree to a fixed value to simplify test
        with patch('interface.vp_complexity.prim_minimum_spanning_tree', return_value=([], 10200)):
            # Mock time.perf_counter to simulate a fixed execution time of 0.0
            with patch('time.perf_counter', return_value=0.0):  
                self.analyser.analyse("execution_time")

                # Assertions and checks
                self.analyser.clear_graph.assert_called_once()
                self.analyser.clear_metrics.assert_called_once()
                self.analyser.generate_complete_graph.assert_called()
                self.analyser.display_complexity_metrics.assert_called()
                self.analyser. visualize_execution_time.assert_called()

                self.assertEqual(self.analyser.generate_complete_graph.call_count, 11, "generate_complete_graph should be called 11 times based on slider settings")
                self.analyser.display_complexity_metrics.assert_called_with(100, 4950, [], 0.0, 10200, self.analyser.processor)
                self.analyser.visualize_execution_time.assert_called_with([2, 12, 22, 32, 42, 52, 62, 72, 82, 92, 100], [0.0] * 11)   # 11 comparison metrics generated since 11 calls to generate_complete_graph with subsequent calls to prim_minimum_spanning_tree
    


    # Test analyse method correctly handles invalid analysis type (this should never happen in the GUI)
    def test_analyse_method_invalid_type(self):
        with self.assertRaises(ValueError):
            self.analyser.analyse("invalid_type")
    


    # Test clear_graph method
    def test_clear_graph(self):
        self.analyser.right_frame = MagicMock(spec=Frame)
        mock_child_widget = create_autospec(Label, instance=True)
        self.analyser.right_frame.winfo_children.return_value = [mock_child_widget]
        self.assertEqual(len(self.analyser.right_frame.winfo_children()), 1, "Setup: Expected 1 widget in right_frame before clear_graph")

        self.analyser.clear_graph()

        # Verify that widget from right_frame is removed
        for widget in self.analyser.right_frame.winfo_children():
            widget.destroy.assert_called_once()
    


    # Test clear_metrics method
    def test_clear_metrics(self):
        self.analyser.lower_left_frame = MagicMock(spec=Frame)
        mock_child_widget = create_autospec(Label, instance=True)
        self.analyser.lower_left_frame.winfo_children.return_value = [mock_child_widget]
        self.assertEqual(len(self.analyser.lower_left_frame.winfo_children()), 1, "Setup: Expected 1 widget in lower_left_frame before clear_metrics")

        self.analyser.clear_metrics()

        # Verify that widget from right_frame is removed
        for widget in self.analyser.lower_left_frame.winfo_children():
            widget.destroy.assert_called_once()
    


    # Test the generation of a complete graph and its properties
    def test_generate_complete_graph_properties(self):
        n = 10
        nodes, edges, E = self.analyser.generate_complete_graph(n)
        
        expected_edges_count = n * (n - 1) / 2
        self.assertEqual(len(nodes), n, "Incorrect number of nodes")
        self.assertEqual(len(edges), expected_edges_count, "Incorrect number of edges")
        self.assertEqual(len(E), expected_edges_count, "Incorrect number of weighted edges")

        # Verify all possible pairs are present
        all_pairs = set(itertools.combinations(nodes, 2))
        generated_pairs = set((start, end) for start, end in edges)
        self.assertEqual(all_pairs, generated_pairs, "Not all possible node pairs are present in edges")

        # Check weights are within expected range 
        for weight in E.values():
            self.assertTrue(1 <= weight <= 11, "Edge weight out of expected range (1 to 10)")
    


    # Test the performance of generating a complete graph for max allowed number of nodes (6000)
    def test_generate_complete_graph_time(self):
        num_nodes = 4000  # Acceptable for it to take 5 seconds to generate a complete graph with 4000 nodes given the scale, this is the largest size of complete graph the CA will ever generate at one time
    
        start_time = time.time()
        nodes, edges, E = self.analyser.generate_complete_graph(num_nodes)
        end_time = time.time()
    
        execution_time = end_time - start_time
    
        # Assert that the execution time is within an acceptable range
        self.assertLess(execution_time, 11, "Execution time is too long")
    

    # Test the memory and CPU usage of generating a complete graph for max allowed number of nodes (4000)
    def test_generate_complete_graph_resources(self):
        num_nodes = 4000

        # Measure memory usage before
        process = psutil.Process()
        mem_before = process.memory_info().rss / (1024 * 1024)  # Memory in MB

        # Measure CPU times before
        cpu_times_before = process.cpu_times()

        # Execute the method
        self.analyser.generate_complete_graph(num_nodes)

        # Measure memory usage after
        mem_after = process.memory_info().rss / (1024 * 1024)  # Memory in MB

        # Measure CPU times after
        cpu_times_after = process.cpu_times()

        # Calculate the differences
        mem_usage = mem_after - mem_before
        cpu_usage = sum([getattr(cpu_times_after, attr) - getattr(cpu_times_before, attr) for attr in cpu_times_after._fields])
        print(f"Memory usage: {mem_usage} MB")

        # Ensure memory and CPU usage are within expected limits
        self.assertLess(mem_usage, 200, "Memory usage is too high")  # 17,997,000 edges * 8 bytes/edge = 143,976,000 bytes ≈ 143 MB, set to 200MB to account for other overheads in the program
        self.assertLess(cpu_usage, 8, "CPU time is too high")  # Sum of user CPU and system CPU time, set to 12s to account for development hardware but this could be faster on higher spec machines
    


    # Edge case for tesing the generation of a complete graph with invalid number of nodes, this should never happen due to the sliders but tested for completeness
    def test_generate_complete_graph_invalid_nodes(self):
        with self.assertRaises(ValueError):
            self.analyser.generate_complete_graph(1)


    # Test the display_complexity_metrics method
    @patch('interface.vp_complexity.ctk.CTkLabel')
    def test_display_complexity_metrics(self, mock_ctklabel):
        # Mock data
        num_nodes = 10
        edges = 45
        mst_edges = 9  
        execution_time = 0.005
        num_comparisons = 1234
        processor = "Intel"

        self.analyser.display_complexity_metrics(num_nodes, edges, mst_edges, execution_time, num_comparisons, processor)

        font = ('Helvetica', 14)
        expected_calls = [
            call(self.analyser.lower_left_frame, text=f"Maximum number of nodes specified: {num_nodes}", font=font, anchor='center'),
            call().pack(side='top', fill='x'),
            call(self.analyser.lower_left_frame, text=f"Number of edges in max node graph: {edges}", font=font, anchor='center'),
            call().pack(side='top', fill='x'),
            call(self.analyser.lower_left_frame, text=f"Number of edges in MST of max node graph: {mst_edges}", font=font, anchor='center'),
            call().pack(side='top', fill='x'),
            call(self.analyser.lower_left_frame, text=f"Average Prim's execution time: {execution_time:.6f} seconds", font=font, anchor='center'),
            call().pack(side='top', fill='x'),
            call(self.analyser.lower_left_frame, text=f"Number of comparisons: {num_comparisons}", font=font, anchor='center'),
            call().pack(side='top', fill='x'),
        ]

        mock_ctklabel.assert_has_calls(expected_calls, any_order=False)
    


    # Test Prim's returns correct MST
    def test_mst_correctness(self):
        # Setup a small graph with known MST
        nodes = ['A', 'B', 'C', 'D', 'E']
        edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('D', 'E')]
        weights = {('A', 'B'): 1, ('B', 'C'): 2, ('C', 'D'): 3, ('D', 'A'): 4, ('A', 'C'): 5, ('B', 'D'): 6, ('B', 'E'): 7, ('D', 'E'): 8}
        graph = (nodes, edges, weights)

        # Expected MST result
        expected_mst_edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('B', 'E')] 

        # Execute Prim's algorithm
        mst_edges, num_comparisons = prim_minimum_spanning_tree(graph)
        print(f"Number of comparisons: {num_comparisons}")

        # Validate MST
        self.assertEqual(set(mst_edges), set(expected_mst_edges), "MST does not match expected result")



    # Test Prim's returns number of comparisons within a correct range
    def test_comparisons_correctness(self):
        # Setup a small graph with known MST
        nodes = ['A', 'B', 'C', 'D', 'E']
        edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('D', 'E')]
        weights = {('A', 'B'): 1, ('B', 'C'): 2, ('C', 'D'): 3, ('D', 'A'): 4, ('A', 'C'): 5, ('B', 'D'): 6, ('B', 'E'): 7, ('D', 'E'): 8}
        graph = (nodes, edges, weights)

        # Expected MST result
        expected_mst_edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('B', 'E')]

        # Comparisons can vary slightly between different runs so allow a small range of values for this test
        min_expected_comparisons = 10  
        max_expected_comparisons = 15  

        # Execute Prim's algorithm
        mst_edges, num_comparisons = prim_minimum_spanning_tree(graph)
        print(f"Number of comparisons: {num_comparisons}")

        # Validate that the number of comparisons falls within the expected range
        self.assertTrue(min_expected_comparisons <= num_comparisons <= max_expected_comparisons, f"Number of comparisons ({num_comparisons}) does not fall within the expected range ({min_expected_comparisons}-{max_expected_comparisons})")
    


    # Test the performance of Prim's algorithm on a small graph in terms of execution time is within an acceptable range
    def test_prims_exec_time_small_graph(self):
        nodes = ['A', 'B', 'C', 'D', 'E']
        edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('D', 'E')]
        weights = {('A', 'B'): 1, ('B', 'C'): 2, ('C', 'D'): 3, ('D', 'A'): 4, ('A', 'C'): 5, ('B', 'D'): 6, ('B', 'E'): 7, ('D', 'E'): 8}
        graph = (nodes, edges, weights)

        start = time.perf_counter()
        mst_edges, num_comparisons = prim_minimum_spanning_tree(graph)
        end = time.perf_counter()

        exec_time = end - start
        print(f"Execution time of Prim's algorithm on small graph: {exec_time} seconds")
        max_exec_time = float(0000.5)
        self.assertTrue(exec_time <= max_exec_time, f"Execution time of Prim's algorithm on small graph is too high: {exec_time} seconds")
    


    # Test the performance of Prim's algorithm on a max nodes graph in terms of execution time is within an acceptable range
    def test_prims_exec_time_max_graph(self):
        num_nodes = 4000
        graph = self.analyser.generate_complete_graph(num_nodes)

        start = time.perf_counter()
        mst_edges, num_comparisons = prim_minimum_spanning_tree(graph)
        end = time.perf_counter()

        exec_time = end - start
        print(f"Execution time of Prim's algorithm on small graph: {exec_time} seconds")
        max_exec_time = float(20)
        self.assertTrue(exec_time <= max_exec_time, f"Execution time of Prim's algorithm on small graph is too high: {exec_time} seconds")
    

    # Due to the nature of the GUI and how matplotlib interacts with the Ctk Frames, it is quite challenging to test the visualization of the complexity metrics and execution time, 
    # therefore, these methods were manually tested during development using visual inspection and the plots were confirmed to be correct.


    

        


        
    

        
    

    
    


        
        

    
        
    
