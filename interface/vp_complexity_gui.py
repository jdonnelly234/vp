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

        self.upper_left_frame_title = ctk.CTkLabel(self.left_frame, text="Specify parameters", font=TITLE_FONT)
        self.upper_left_frame_title.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        self.upper_left_frame = ctk.CTkFrame(self.left_frame, width=300, height=100)
        self.upper_left_frame.grid(row=1, column=0, pady=10, padx=10, sticky='w')

        parameter_tabview = ctk.CTkTabview(master=self.upper_left_frame, fg_color=FRAME_FG_COLOR, bg_color=FRAME_BG_COLOR)
        parameter_tabview.pack(fill='both', expand=True)

        comp_tab = parameter_tabview.add("No. of Comparisons")
        exec_tab = parameter_tabview.add("Execution Time")

        comp_tab_node_title = ctk.CTkLabel(comp_tab, text="Use the slider to specify no. of nodes")
        comp_tab_node_title.pack(padx=(20))
        comp_slider = ctk.CTkSlider(comp_tab, from_=10, to=250,number_of_steps=24, command=lambda value: self.update_slider_label(comp_slider_label, value))
        comp_slider.pack(padx=(10))
        comp_slider_label = ctk.CTkLabel(comp_tab, text="130")
        comp_slider_label.pack(padx=(10))
        comp_tab_analyse_button = ctk.CTkButton(comp_tab, text="Analyse")
        comp_tab_analyse_button.pack(padx=(30), pady = (30,10))

        exec_tab_node_title = ctk.CTkLabel(exec_tab, text="Use the slider to specify no. of nodes")
        exec_tab_node_title.pack(padx=(20))
        exec_slider = ctk.CTkSlider(exec_tab, from_=1000, to=16000, number_of_steps=15, command=lambda value: self.update_slider_label(exec_slider_label, value))
        exec_slider.pack(padx=(10))
        exec_slider_label = ctk.CTkLabel(exec_tab, text="8000")
        exec_slider_label.pack(padx=(10))
        exec_tab_analyse_button = ctk.CTkButton(exec_tab, text="Analyse")
        exec_tab_analyse_button.pack(padx=(30), pady = 30)

        self.lower_left_frame_title = ctk.CTkLabel(self.left_frame, text="View complexity metrics", font=TITLE_FONT)
        self.lower_left_frame_title.grid(row=6, column=0, pady=10, padx=10, sticky='w')

        self.lower_left_frame = ctk.CTkFrame(self.left_frame)
        self.lower_left_frame.grid(row=7, column=0, pady=10, padx=10, sticky='w')
     
    def update_slider_label(self, label, value):
        # Update the specified slider label based on the slider's current value
        label.configure(text=str(int(value)))