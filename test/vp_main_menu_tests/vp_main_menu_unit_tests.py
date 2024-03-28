import unittest
import tkinter
from unittest.mock import patch, MagicMock
from interface.vp_main_gui import MainMenu

class TestMainMenu(unittest.TestCase):
    
    def setUp(self):
        self.app = MainMenu()
        visualiser_patch = patch('interface.vp_main_gui.VisualisingPrims')
        complexity_patch = patch('interface.vp_main_gui.ComplexityAnalyser')
        ctk_toplevel_patch = patch('customtkinter.CTkToplevel')

        self.addCleanup(visualiser_patch.stop)
        self.addCleanup(complexity_patch.stop)
        self.addCleanup(ctk_toplevel_patch.stop)

        self.mock_visualiser = visualiser_patch.start()
        self.mock_complexity = complexity_patch.start()
        self.mock_toplevel = ctk_toplevel_patch.start()

        self.app.launch_graph_visualiser = MagicMock()
        self.app.launch_complexity_analyser = MagicMock()
        self.app.launch_what_is_prims = MagicMock()
        self.app.launch_help = MagicMock()
        self.app.launch_exit = MagicMock()
        self.mock_toplevel_instance = MagicMock()
        self.mock_toplevel.return_value = self.mock_toplevel_instance
        self.mock_toplevel_instance.mainloop = MagicMock()


    def tearDown(self):
        try:
            self.app.destroy()
        except tkinter.TclError:
            pass  # Ignore the error if the window is already closed


    # Test window title
    def test_window_title(self):
        self.assertEqual(self.app.title(), "Visualising Prim's")
    

    # Test button initialization and correct text
    def test_button_initialization(self):
        self.assertIsNotNone(self.app.graph_visualiser_button)
        self.assertEqual(self.app.graph_visualiser_button.cget("text"), "Prim's Visualiser")

        self.assertIsNotNone(self.app.complexity_analyser_button)
        self.assertEqual(self.app.complexity_analyser_button.cget("text"), "Complexity Analyser")

        self.assertIsNotNone(self.app.what_is_prims_button)
        self.assertEqual(self.app.what_is_prims_button.cget("text"), "What is Prim's?")

        self.assertIsNotNone(self.app.help_button)
        self.assertEqual(self.app.help_button.cget("text"), "Help")

        self.assertIsNotNone(self.app.exit_button)
        self.assertEqual(self.app.exit_button.cget("text"), "Exit")


    # Test if VisualisingPrims & ComplexityAnalyser classes are called when the button is clicked
    def test_launch_graph_visualiser(self):
        self.app.graph_visualiser_button.invoke()
        self.mock_visualiser.assert_called_once()

    def test_launch_complexity_analyser(self):
        self.app.complexity_analyser_button.invoke()
        self.mock_complexity.assert_called_once()
    

    def test_launch_what_is_prims(self):
        self.app.what_is_prims_button.invoke()
        self.mock_toplevel.assert_called_once_with(self.app)
    

if __name__ == "__main__":
    unittest.main()
