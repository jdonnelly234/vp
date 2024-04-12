import customtkinter as ctk
from vp_graph import VisualisingPrims
from vp_complexity import ComplexityAnalyser
from config import *
from PIL import Image
import sys


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
        self.left_frame = ctk.CTkFrame(self, corner_radius=50, fg_color=BUTTON_FG_COLOR, background_corner_colors=[BUTTON_FG_COLOR, "#252424", "#252424", BUTTON_FG_COLOR], bg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky='nsew')  

        self.right_frame = ctk.CTkFrame(self, corner_radius=0, bg_color="transparent", fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky='nsew', padx=30)  

        # Configure the right frame for centered button placement
        for i in range(20):  
            self.right_frame.grid_rowconfigure(i, weight=1)

        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(2, weight=1)

        # Create and place buttons in the right frame
        self.graph_visualiser_button = ctk.CTkButton(self.right_frame, text="Graph Visualiser", command=self.launch_graph_visualiser, text_color=TITLE_COLOUR, fg_color=BUTTON_FG_COLOR, bg_color=FRAME_FG_COLOR, font=COMPLEXITY_SUBTITLE_FONT)
        self.graph_visualiser_button.grid(row=8, column=1, sticky='ew')

        self.complexity_analyser_button = ctk.CTkButton(self.right_frame, text="Complexity Analyser", command=self.launch_complexity_analyser, text_color=TITLE_COLOUR, fg_color=BUTTON_FG_COLOR, bg_color=FRAME_FG_COLOR, font=COMPLEXITY_SUBTITLE_FONT)
        self.complexity_analyser_button.grid(row=9, column=1, sticky='ew')

        self.what_is_prims_button = ctk.CTkButton(self.right_frame, text="What is Prim's?", command=self.launch_what_is_prims, text_color=TITLE_COLOUR, fg_color=BUTTON_FG_COLOR, bg_color=FRAME_FG_COLOR, font=COMPLEXITY_SUBTITLE_FONT)
        self.what_is_prims_button.grid(row=10, column=1, sticky='ew')

        self.help_button = ctk.CTkButton(self.right_frame, text="Help", command=self.launch_help, text_color=TITLE_COLOUR, fg_color=BUTTON_FG_COLOR, bg_color=FRAME_FG_COLOR, font=COMPLEXITY_SUBTITLE_FONT)
        self.help_button.grid(row=11, column=1, sticky='ew')

        self.exit_button = ctk.CTkButton(self.right_frame, text="Exit", command=self.launch_exit, text_color=TITLE_COLOUR, fg_color=BUTTON_FG_COLOR, bg_color=FRAME_FG_COLOR, font=COMPLEXITY_SUBTITLE_FONT)
        self.exit_button.grid(row=12, column=1, sticky='ew')

        self.main_title = ctk.CTkLabel(self.right_frame, text="Visualising Prim's", font=TITLE_FONT, text_color=TITLE_COLOUR)
        self.main_title.grid(row=4, column=1, pady=10, sticky='ew')


    def launch_graph_visualiser(self):
        self.withdraw()
        visualiser = VisualisingPrims()
        visualiser.mainloop()
        self.deiconify()  # Show the main menu again after the visualiser is closed, this fixes segmentation fault


    def launch_complexity_analyser(self):
        self.withdraw()
        complexity = ComplexityAnalyser()
        complexity.mainloop()


    def launch_help(self):
        self.help_launched = True  # Added flag for testing purposes

        # Create a Toplevel window for the help content
        help_window = ctk.CTkToplevel(self)
        help_window.title("Help")
        help_window.geometry("500x500") 

        help_window_width = 500
        help_window_height = 500

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int((screen_width - help_window_width) / 2)
        center_y = int((screen_height - help_window_height) / 2)

        help_window.geometry(f'{help_window_width}x{help_window_height}+{center_x}+{center_y}')

        # Create the tab view within the new Toplevel window
        helpTab = ctk.CTkTabview(help_window)

        guide_tab = helpTab.add("Guide")
        faq_tab = helpTab.add("FAQ")
        accessibility_tab = helpTab.add("Accessibility")

        # Guide tab
        which_guide_text = ctk.CTkLabel(guide_tab, text="Select a guide:", font=("Helvetica", 14, "bold"))
        which_guide_text.grid(row=0, column=0, padx=50, pady=20)
        
        guide_text = ctk.CTkLabel(guide_tab, text=VISUALISER_GUIDE_TEXT, wraplength=380, justify="left")
        guide_text.grid(row=1, column=0, columnspan=2, padx=50, pady=10)

        def guide_text_decider(choice):
            if choice == "Graph Visualiser":
                guide_text.configure(text=VISUALISER_GUIDE_TEXT, wraplength=380)
            elif choice == "Complexity Analyser":
                guide_text.configure(text=COMPLEXITY_GUIDE_TEXT, wraplength=380, justify="left")
                
        
        guide_selector = ctk.CTkComboBox(guide_tab, values=["Graph Visualiser", "Complexity Analyser"], width= 170, command = guide_text_decider, state="readonly")
        guide_selector.grid(row=0, column=1, padx=50, pady=20)
        guide_selector.set("Graph Visualiser")

        # FAQ tab
        faq_text = ctk.CTkLabel(faq_tab, text=FAQ_TEXT, wraplength=380, justify="left")
        faq_text.grid(row=0, column=0, padx=50, pady=20)

        # Accessibility tab
        colour_scheme_label = ctk.CTkLabel(accessibility_tab, text="Colour Scheme", font=COMPLEXITY_SUBTITLE_FONT)
        colour_scheme_label.grid(row=0, column=0, padx=50, pady=20)

        colour_scheme_selector = ctk.CTkComboBox(accessibility_tab, values=["Light Mode", "Dark Mode", "High Contrast", "Deuteranopia", "Tritanopia"], width= 170, state="readonly")
        colour_scheme_selector.grid(row=0, column=1, padx=50, pady=20)

        

        


        # Set the default tab to open
        helpTab.set("Guide")

        # Place the tab view in the window
        helpTab.pack(fill='both', expand=True)

    
    def launch_what_is_prims(self):
        self.what_is_prims_launched = True  # Added flag for testing purposes

        info_window = ctk.CTkToplevel(self)
        info_window.title("What is Prim's Algorithm?")
        info_window.geometry("500x400")  

        what_is_prims_width = 450
        what_is_prims_height = 300

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Find the center point
        center_x = int((screen_width - what_is_prims_width) / 2)
        center_y = int((screen_height - what_is_prims_height) / 2)

        # Set the position of the window to the center of the screen
        info_window.geometry(f'{what_is_prims_width}x{what_is_prims_height}+{center_x}+{center_y}')

        self.texts = [
            "Prim's algorithm is a greedy algorithm that finds a minimum spanning tree for a weighted undirected graph. The algorithm was developed in 1930 by Czech mathematician Vojtěch Jarník and later rediscovered and republished by computer scientists Robert C. Prim in 1957 and Edsger W. Dijkstra in 1959.",
            "The algorithm operates by finding a subset of the edges that forms a tree that includes every node, where the total weight of all the edges in the tree is minimized. The algorithm operates by building this tree one node at a time, from an arbitrary starting node, at each step adding the cheapest possible connection from the tree to another node",
            "Prim's algorithm is used in network designing, where the goal is to connect all points with the minimum total weighting for the connections. It is also used for planning road and railway networks that connect cities or towns, ensuring all locations are connected with the shortest total distance"
        ]

        self.current_text_index = 0

        self.info_label = ctk.CTkLabel(info_window, text="Prim's algorithm is a greedy algorithm that finds a minimum spanning tree for a weighted undirected graph. This means it finds a subset of the edges that forms a tree that includes every node, where the total weight of all the edges in the tree is minimized.", wraplength=380, justify="left")
        self.info_label.pack(pady=20, padx=20)

        def update_text(direction):
            self.current_text_index += direction
            
            # Disable the "Previous" button if on the first slide
            if self.current_text_index <= 0:
                self.current_text_index = 0
                prev_button.configure(state="disabled")
            else:
                prev_button.configure(state="normal")
            
            # Disable the "Next" button if on the last slide
            if self.current_text_index >= len(self.texts) - 1:
                self.current_text_index = len(self.texts) - 1
                next_button.configure(state="disabled")
            else:
                next_button.configure(state="normal")
            
            self.info_label.configure(text=self.texts[self.current_text_index])

        # Next and Previous buttons
        prev_button = ctk.CTkButton(info_window, text="Previous", state="disabled", command=lambda: update_text(-1))
        prev_button.pack(side="left", padx=(50, 10), pady=20)

        next_button = ctk.CTkButton(info_window, text="Next", command=lambda: update_text(1))
        next_button.pack(side="right", padx=(10, 50), pady=20)


    def launch_exit(self):
        self.destroy()
        sys.exit()


        