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
        self.left_frame = ctk.CTkFrame(self, width=WINDOW_WIDTH * 0.25, fg_color=FRAME_FG_COLOR, bg_color=FRAME_BG_COLOR)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.right_frame = ctk.CTkFrame(self, width=WINDOW_WIDTH * 0.75, fg_color=FRAME_BG_COLOR)
        self.right_frame.pack(padx=20, pady=20)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.right_frame_placeholder = ctk.CTkLabel(self.right_frame, text="Your complexity chart will be plotted here \n once the Analyse button is clicked...", font=COMPLEXITY_PLACEHOLDER_FONT, text_color=COMPLEXITY_PLACEHOLDER_COLOUR)
        self.right_frame_placeholder.pack(pady=310)

        self.upper_left_frame_title = ctk.CTkLabel(self.left_frame, text="Specify parameters", font=TITLE_FONT, text_color=TITLE_COLOUR)
        self.upper_left_frame_title.grid(row=0, column=0, pady=(15,10), padx=10, sticky='w')

        self.upper_left_frame = ctk.CTkFrame(self.left_frame, width=300, height=100)
        self.upper_left_frame.grid(row=1, column=0, pady=10, padx=10, sticky='w')

        self.lower_left_frame_title = ctk.CTkLabel(self.left_frame, text="View complexity metrics", font=TITLE_FONT, text_color=TITLE_COLOUR)
        self.lower_left_frame_title.grid(row=6, column=0, pady=(15,10), padx=10, sticky='w')

        self.lower_left_frame = ctk.CTkFrame(self.left_frame, width=360, height=300, fg_color=ANALYSER_FRAME_COLOR, corner_radius=10)
        self.lower_left_frame.grid(row=7, column=0, pady=10, padx=10, sticky='ew')

        self.lower_left_frame_placeholder = ctk.CTkLabel(self.lower_left_frame, text="Your complexity metrics will be displayed here \n once the Analyse button is clicked...", font=COMPLEXITY_PLACEHOLDER_FONT, text_color=COMPLEXITY_PLACEHOLDER_COLOUR)
        self.lower_left_frame_placeholder.pack(pady=100)

        self.parameter_tabview = ctk.CTkTabview(master=self.upper_left_frame, fg_color=ANALYSER_FRAME_COLOR, bg_color=FRAME_BG_COLOR, border_color=FRAME_BG_COLOR, segmented_button_fg_color=FRAME_FG_COLOR, segmented_button_selected_color=BUTTON_FG_COLOR, segmented_button_unselected_color=ANALYSER_FRAME_COLOR)
        self.parameter_tabview.pack(fill='both', expand=True)

        self.comp_tab = self.parameter_tabview.add("No. of Comparisons")
        self.exec_tab = self.parameter_tabview.add("Execution Time")

        # Node selector for the number of nodes in comparisons tab
        self.comp_tab_node_title = ctk.CTkLabel(self.comp_tab, text="Use the slider to specify max nodes:", font=COMPLEXITY_SUBTITLE_FONT, text_color=TITLE_COLOUR)
        self.comp_tab_node_title.pack(padx=(20))

        self.comp_slider = ctk.CTkSlider(self.comp_tab, from_=100, to=2000,number_of_steps=19, command=lambda value: self.update_slider_label(self.comp_slider_label, value), button_color=BUTTON_FG_COLOR)
        self.comp_slider.pack(padx=(10))

        self.comp_slider_label = ctk.CTkLabel(self.comp_tab, text="1050", font=COMPLEXITY_SUBTITLE_FONT, text_color=TITLE_COLOUR)
        self.comp_slider_label.pack(padx=(10))

        self.comp_slider.bind("<ButtonRelease-1>", lambda event, arg="comp": self.on_node_slider_change(arg, event))

        # Step selector for the number of steps in comparisons tab
        self.comp_tab_steps_title = ctk.CTkLabel(self.comp_tab, text="Specify the size of the step interval for the x axis:", font=COMPLEXITY_SUBTITLE_FONT, text_color=TITLE_COLOUR)
        self.comp_tab_steps_title.pack(padx=(20))
        self.comp_steps_slider = ctk.CTkSlider(self.comp_tab, from_=10, to=100,number_of_steps=10, command=lambda value: self.update_slider_label(self.comp_steps_slider_label, value), button_color=BUTTON_FG_COLOR)
        self.comp_steps_slider.pack(padx=(10))
        self.comp_steps_slider_label = ctk.CTkLabel(self.comp_tab, text="55", font=COMPLEXITY_SUBTITLE_FONT, text_color=TITLE_COLOUR)
        self.comp_steps_slider_label.pack(padx=(10))

        # Button to start the analysis in comparisons tab
        self.comp_tab_analyse_button = ctk.CTkButton(self.comp_tab, text="Analyse", command=self.analyse_comparisons, text_color=TITLE_COLOUR, fg_color=BUTTON_FG_COLOR, bg_color=ANALYSER_FRAME_COLOR, font=COMPLEXITY_SUBTITLE_FONT)
        self.comp_tab_analyse_button.pack(padx=(30), pady = (30,10))


        self.exec_tab_node_title = ctk.CTkLabel(self.exec_tab, text="Use the slider to specify max nodes:", font=COMPLEXITY_SUBTITLE_FONT, text_color=TITLE_COLOUR)
        self.exec_tab_node_title.pack(padx=(20))
        self.exec_slider = ctk.CTkSlider(self.exec_tab, from_=100, to=10000, number_of_steps=49, command=lambda value: self.update_slider_label(self.exec_slider_label, value), button_color=BUTTON_FG_COLOR)
        self.exec_slider.pack(padx=(10))
        self.exec_slider_label = ctk.CTkLabel(self.exec_tab, text="4950", font=COMPLEXITY_SUBTITLE_FONT, text_color=TITLE_COLOUR)
        self.exec_slider_label.pack(padx=(10))
        self.exec_slider.bind("<ButtonRelease-1>", lambda event, arg="exec": self.on_node_slider_change(arg, event))

        self.exec_tab_steps_title = ctk.CTkLabel(self.exec_tab, text="Specify the size of the step interval for the x axis:", font=COMPLEXITY_SUBTITLE_FONT, text_color=TITLE_COLOUR)
        self.exec_tab_steps_title.pack(padx=(20))
        self.exec_steps_slider = ctk.CTkSlider(self.exec_tab, from_=10, to=100,number_of_steps=10, command=lambda value: self.update_slider_label(self.exec_steps_slider_label, value), button_color=BUTTON_FG_COLOR)
        self.exec_steps_slider.pack(padx=(10))
        self.exec_steps_slider_label = ctk.CTkLabel(self.exec_tab, text="50", font=COMPLEXITY_SUBTITLE_FONT, text_color=TITLE_COLOUR)
        self.exec_steps_slider_label.pack(padx=(10))

        self.exec_tab_analyse_button = ctk.CTkButton(self.exec_tab, text="Analyse", command=self.analyse_execution_time, text_color=TITLE_COLOUR, fg_color=BUTTON_FG_COLOR, bg_color=ANALYSER_FRAME_COLOR, font=COMPLEXITY_SUBTITLE_FONT)
        self.exec_tab_analyse_button.pack(padx=(30), pady = (30,10))

        # Button to return to the main menu
        return_button = ctk.CTkButton(self.left_frame, text="Return to Main Menu", command=self.return_to_main_menu, text_color=TITLE_COLOUR, fg_color=BUTTON_FG_COLOR, bg_color=FRAME_FG_COLOR, font=COMPLEXITY_SUBTITLE_FONT)
        return_button.grid(row = 8, pady = 40)
     

    def update_slider_label(self, label, value):
        # Update the specified slider label based on the slider's current value
        label.configure(text=str(int(value)))
    

    def on_node_slider_change(self, identifier, event=None):
        if identifier == "comp":
            max_nodes = int(self.comp_slider.get()) 
            max_steps = max_nodes / 10
            min_steps = max_nodes / 20

            # Adjust the step slider's range. Assuming `self.step_slider` is your Tkinter Scale for steps
            self.comp_steps_slider.configure(from_=min_steps, to=max_steps)

            self.comp_steps_slider.set(max_steps - (min_steps / 2))
            self.update_slider_label(self.comp_steps_slider_label, max_steps - (min_steps / 2))
        elif identifier == "exec":
            max_nodes = int(self.exec_slider.get()) 
            max_steps = max_nodes / 5
            min_steps = max_nodes / 10

            # Adjust the step slider's range. Assuming `self.step_slider` is your Tkinter Scale for steps
            self.exec_steps_slider.configure(from_=min_steps, to=max_steps)

            self.exec_steps_slider.set(max_steps - (min_steps / 2))
            self.update_slider_label(self.exec_steps_slider_label, max_steps - (min_steps / 2))