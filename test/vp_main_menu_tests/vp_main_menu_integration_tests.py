from interface.vp_main_gui import MainMenu
from interface.vp_graph import GraphVisualiser
from interface.vp_complexity import ComplexityAnalyser
import unittest
from unittest.mock import MagicMock, patch
from tkinter import Tk


class TestVPMainIntegration(unittest.TestCase):
    print("###########MAIN MENU INTEGRATION TESTS###########\n") 

    def setUp(self):
        self.app = MainMenu()
    
    # MM User Story 1: Launching the graph visualiser
    # Test launch of graph visualiser instance from main menu using mock
    @patch('interface.vp_main_gui.GraphVisualiser')
    def test_launch_graph_visualiser(self, mock_visualiser):
        # Call the method that should open the graph visualiser
        self.app.launch_graph_visualiser()
        # Check if graph visualiser was instantiated
        mock_visualiser.assert_called_once()


    # MM User Story 2: Launching the complexity analyser
    # Test launch of complexity analyser instance from main menu using mock
    @patch('interface.vp_main_gui.ComplexityAnalyser')
    def test_launch_complexity_analyser(self, mock_analyser):
        # Call the method that should open the complexity analyser
        self.app.launch_complexity_analyser()
        # Check if complexity analyser was instantiated
        mock_analyser.assert_called_once()
    
    # MM User Story 3: Launching the help window
    # Test the launch_help method using flag from within method, this is easiest way to test it does what it is meant to
    def test_launch_help(self):
        # Ensure the flag starts as False or is not set
        self.assertFalse(hasattr(self.app, 'help_launched'))
        self.app.launch_help()
        self.assertTrue(self.app.help_launched)
    

    # MM User Story 4: Launching the what is prims window
    # Test the launch_what_is_prims method using flag from within method, this is easiest way to test it does what it is meant to
    def test_launch_what_is_prims(self):
        # Ensure the flag starts as False or is not set
        self.assertFalse(hasattr(self.app, 'what_is_prims_launched'))
        self.app.launch_what_is_prims()
        self.assertTrue(self.app.what_is_prims_launched)
    

    # MM User Story 5: Exiting the application from the main menu
    @patch('interface.vp_main_gui.sys.exit')  
    def test_exit_button(self, mock_exit):
        self.app.launch_exit()  # Simulate clicking the exit button
        mock_exit.assert_called_once()  # Check if sys.exit was called
    

if __name__ == '__main__':
    unittest.main()


