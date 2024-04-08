import unittest
from tkinter import StringVar, filedialog
from customtkinter import CTk
from unittest.mock import MagicMock, mock_open, patch, create_autospec
from interface.vp_complexity import ComplexityAnalyser
from interface.utils import *
import json
import os
from PIL import Image

class TestComplexityAnalyser(unittest.TestCase):
    def setUp(self):
        self.analyser = ComplexityAnalyser()
        print("###########COMPLEXITY ANALYSER INTEGRATION TESTS###########\n")        
    
    # CA User Story 1: Gathering comparison related metrics for Prim’s algorithm
    @patch('interface.vp_complexity.ComplexityAnalyser.clear_graph')
    @patch('interface.vp_complexity.ComplexityAnalyser.clear_metrics')
    @patch('interface.vp_complexity.ComplexityAnalyser.display_complexity_metrics')
    @patch('interface.vp_complexity.ComplexityAnalyser.visualize_complexity')
    def test_comparison_integration(self, mock_visualize_complexity, mock_display_metrics, mock_clear_metrics, mock_clear_graph):
        with patch('tkinter.Tk.mainloop', new=MagicMock()):
            # Set the slider values
            self.analyser.comp_slider.set(100)
            self.analyser.comp_steps_slider.set(10)
            
            # Simulate user selecting comparisons and clicking "Analyse"
            self.analyser.analyse("comparisons")
            
            # Check if the correct methods were called as expected
            mock_clear_graph.assert_called_once()
            mock_clear_metrics.assert_called_once()
            mock_display_metrics.assert_called_once()
            mock_visualize_complexity.assert_called_once()
    

    # CA User Story 2: Gathering execution time related metrics for Prim’s algorithm
    @patch('interface.vp_complexity.ComplexityAnalyser.clear_graph')
    @patch('interface.vp_complexity.ComplexityAnalyser.clear_metrics')
    @patch('interface.vp_complexity.ComplexityAnalyser.display_complexity_metrics')
    @patch('interface.vp_complexity.ComplexityAnalyser.visualize_execution_time')
    def test_exec_time__integration(self, mock_visualize_execution_time, mock_display_metrics, mock_clear_metrics, mock_clear_graph):
        with patch('tkinter.Tk.mainloop', new=MagicMock()):
            # Set the slider values
            self.analyser.exec_slider.set(100)
            self.analyser.exec_steps_slider.set(10)
            
            # Simulate user selecting comparisons and clicking "Analyse"
            self.analyser.analyse("execution_time")
            
            # Check if the correct methods were called as expected
            mock_clear_graph.assert_called_once()
            mock_clear_metrics.assert_called_once()
            mock_display_metrics.assert_called_once()
            mock_visualize_execution_time.assert_called_once()


    # CA User Story 3: Returning to the main menu from the complxity analsyer
    @patch('interface.vp_main_gui.MainMenu', autospec=True)
    def test_ca_to_main_menu(self, mock_main_menu_class):                           # mock_main_menu_class is a mock of the MainMenu class
        # Mocking tkinter main loop to prevent GUI from opening
        with patch('tkinter.Tk.mainloop', new=MagicMock()):
            self.app = ComplexityAnalyser()
        
        main_menu_instance = mock_main_menu_class.return_value
        
        # Simulating user clicking main menu button 
        self.app.return_to_main_menu()

        # Check if ComplexityAnalyser instance was destroyed
        self.assertTrue(self.app.destroy)                         

        # Check if MainMenu was instantiated
        mock_main_menu_class.assert_called_once()

        # Check that the MainMenu instance is shown by asserting main loop was started
        main_menu_instance.mainloop.assert_called_once()



        