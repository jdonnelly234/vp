import customtkinter as ctk
import tkinter as tk
from tkinter import OptionMenu, StringVar
from config import *
from utils import *

# GUI class that inherits from the custom tkinter class, handles all GUI related changes except canvas changes related to Prim's
class ComplexityGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Visualising Prim's")

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Find the center point
        center_x = int((screen_width - WINDOW_WIDTH) / 2)
        center_y = int((screen_height - WINDOW_HEIGHT) / 2)

        # Set the position of the window to the center of the screen
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}')

        # Minimum size for the window to avoid issues with resizing
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT) 

         # Create left and right frames for metrics and graph
        self.left_frame = ctk.CTkFrame(self, width=WINDOW_WIDTH * 0.25)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.right_frame = ctk.CTkFrame(self, width=WINDOW_WIDTH * 0.75)
        self.right_frame.pack(padx=20, pady=20)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
     
        