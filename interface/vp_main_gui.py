import customtkinter as ctk
from vp_graph import VisualisingPrims
from vp_complexity import ComplexityAnalyser
from config import *
from PIL import Image


class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Visualising Prim's")

        main_menu_window_width = 600
        main_menu_window_height = 600

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Find the center point
        center_x = int((screen_width - main_menu_window_width) / 2)
        center_y = int((screen_height - main_menu_window_height) / 2)

        # Set the position of the window to the center of the screen
        self.geometry(f'{main_menu_window_width}x{main_menu_window_height}+{center_x}+{center_y}')

        # Minimum and maximum size for the window
        self.minsize(main_menu_window_width, main_menu_window_height)
        self.maxsize(main_menu_window_width, main_menu_window_height)

        # Configure the grid for equal-sized columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Configure the grid for a single row
        self.grid_rowconfigure(0, weight=1)

        # Create left and right frames
        self.left_frame = ctk.CTkFrame(self, corner_radius=50, fg_color="#427BD2", background_corner_colors=["#427BD2", "#252424", "#252424", "#427BD2"], bg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky='nsew')  

        self.right_frame = ctk.CTkFrame(self, corner_radius=0, bg_color="transparent", fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky='nsew', padx=30)  

        # Configure the right frame for centered button placement
        for i in range(20):  
            self.right_frame.grid_rowconfigure(i, weight=1)

        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(2, weight=1)

        # Create and place buttons in the right frame
        self.graph_visualiser_button = ctk.CTkButton(self.right_frame, text="Prim's Visualiser", command=self.launch_graph_visualiser)
        self.graph_visualiser_button.grid(row=8, column=1, sticky='ew')

        self.complexity_analyser_button = ctk.CTkButton(self.right_frame, text="Complexity Analyser", command=self.launch_complexity_analyser)
        self.complexity_analyser_button.grid(row=9, column=1, sticky='ew')

        self.what_is_prims_button = ctk.CTkButton(self.right_frame, text="What is Prim's?", command=self.launch_what_is_prims)
        self.what_is_prims_button.grid(row=10, column=1, sticky='ew')

        self.help_button = ctk.CTkButton(self.right_frame, text="Help", command=self.launch_help)
        self.help_button.grid(row=11, column=1, sticky='ew')

        self.exit_button = ctk.CTkButton(self.right_frame, text="Exit", command=self.launch_exit)
        self.exit_button.grid(row=12, column=1, sticky='ew')

        self.main_title = ctk.CTkLabel(self.right_frame, text="Visualising Prim's", font=TITLE_FONT)
        self.main_title.grid(row=4, column=1, pady=10, sticky='ew')

    def launch_graph_visualiser(self):
        self.destroy()
        visualiser = VisualisingPrims()
        visualiser.mainloop()

    def launch_complexity_analyser(self):
        self.withdraw()
        complexity = ComplexityAnalyser()
        complexity.mainloop()

    def launch_help(self):
        print("Under development.....")
    
    def launch_what_is_prims(self):
        print("Under development.....")

    def launch_exit(self):
        self.destroy()