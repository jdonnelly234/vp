import customtkinter as ctk
import tkinter as tk
from tkinter import OptionMenu, StringVar
from config import *
from utils import *

# GUI class that inherits from the custom tkinter class, handles all GUI related changes except canvas changes related to Prim's
class GraphVisualiserGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Visualising Prim's")

        window_width = 1200
        window_height = 800

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Find the center point
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)

        # Set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Minimum size for the window to avoid issues with resizing
        self.minsize(window_width, window_height) 


        self.top_margin = 50  # Margin to prevent nodes from being placed behind the status label


        # Frames for different sections
        self.left_frame = ctk.CTkFrame(self, width=200, fg_color=FRAME_FG_COLOR, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky='ns', rowspan=14)

        self.right_frame = ctk.CTkFrame(self, width=200, fg_color=FRAME_FG_COLOR, corner_radius=0)
        self.right_frame.grid(row=0, column=2, sticky='ns', rowspan=8, columnspan=2)

        self.canvas_frame = ctk.CTkFrame(self, width=624, height=768, fg_color=FRAME_FG_COLOR, corner_radius=10, bg_color=FRAME_BG_COLOR)
        self.canvas_frame.grid(row=0, column=1, sticky='nsew', rowspan=8)

        self.status_frame = ctk.CTkFrame(self, width=200)
        self.status_frame.grid(row=0, column=0, pady=12, padx=50, columnspan=4, sticky='n')


        # Headings for UI sections 
        self.upper_left_frame_title = ctk.CTkLabel(self.left_frame, text="Create an edge", font=TITLE_FONT)
        self.upper_left_frame_title.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        self.middle_left_frame_title = ctk.CTkLabel(self.left_frame, text="Delete a node or edge", font=TITLE_FONT)
        self.middle_left_frame_title.grid(row=5, column=0, pady=10, padx=10, sticky='w')

        self.lower_left_frame_title = ctk.CTkLabel(self.left_frame, text="Other features", font=TITLE_FONT)
        self.lower_left_frame_title.grid(row=8, column=0, pady=10, padx=10, sticky='w')

        self.right_frame_title = ctk.CTkLabel(self.right_frame, text="Run Prim's algorithm", font=TITLE_FONT)
        self.right_frame_title.grid(row=0, column=0, pady=10, padx=10, sticky='ew', columnspan=2)


        # Initialize canvas
        self.canvas = ctk.CTkCanvas(self.canvas_frame, width=700, height=568, bg="white")
        self.canvas.pack(padx=10, pady=10, fill="both", expand=True)


        # Initialising dropdown menus and weight input
        self.start_node_var = StringVar(self)
        self.end_node_var = StringVar(self)
        self.weight_var = StringVar(self)
        self.start_vertex_var = StringVar(self)
        self.delete_node_var = StringVar(self)
        self.delete_edge_var = StringVar(self)
        

        # Dropdown menus 
        self.start_node_menu = OptionMenu(self, self.start_node_var, "Add nodes to see them here")
        self.start_node_menu.grid(in_=self.left_frame, row=1, column=0, pady=5, padx=10, sticky='e')

        self.end_node_menu = OptionMenu(self, self.end_node_var, "Add nodes to see them here")
        self.end_node_menu.grid(in_=self.left_frame, row=2, column=0, pady=5, padx=10, sticky='e')

        self.delete_node_menu = OptionMenu(self.left_frame, self.delete_node_var, "Add nodes to see them here")
        self.delete_node_menu.grid(row=6, column=0, pady=10, padx=10, sticky='w')

        self.delete_edge_var.set("   ") # Default value
        self.delete_edge_menu = OptionMenu(self.left_frame, self.delete_edge_var, "Add edges to see them here")
        self.delete_edge_menu.grid(row=7, column=0, pady=10, padx=10, sticky='w')

        self.start_vertex_menu = OptionMenu(self.right_frame, self.start_vertex_var, "Add nodes to see them here")
        self.start_vertex_menu.grid(row=1, column=1, pady=10, padx=(1,10), sticky='e')
        self.start_vertex_var.set("Source")  # Default value


        # Weight entry field
        self.weight_entry = ctk.CTkEntry(self, textvariable=self.weight_var, width=50)
        self.weight_entry.grid(in_=self.left_frame, row=3, column=0, pady=10, padx=10, sticky='e')


        # Labels for the dropdown menus and weight input and status label
        self.start_node_label = ctk.CTkLabel(self, text="Start Node")
        self.start_node_label.grid(in_=self.left_frame, row=1, column=0, sticky='w', padx=10, pady=10)

        self.end_node_label = ctk.CTkLabel(self, text="End Node")
        self.end_node_label.grid(in_=self.left_frame, row=2, column=0, sticky='w', padx=10)

        self.weight_label = ctk.CTkLabel(self, text="Weight", fg_color="#302c2c")
        self.weight_label.grid(in_=self.left_frame, row=3, column=0, sticky='w', padx=10)

        self.status_label = ctk.CTkLabel(self.status_frame, text="Graph Drawing Mode", font=("Calibri", 12, "italic"))
        self.status_label.pack(pady=1, padx=1)  # Use pack to add padding inside the frame
        

        # Buttons
        self.create_edge_button = ctk.CTkButton(self, text="Create Edge", command=self.manual_create_edge)
        self.create_edge_button.grid(in_=self.left_frame, row=4, column=0, pady=10, padx=10, sticky='ew')

        self.finalize_button = ctk.CTkButton(self, text="Run Prim's", command=self.generate_mst)
        self.finalize_button.grid(in_=self.right_frame, row=1, column=0, pady=10, padx=10, sticky='ew')

        self.reset_button = ctk.CTkButton(self, text="Reset Graph", state="disabled", hover_color="#FF0000", command=self.confirm_reset)
        self.reset_button.grid(in_=self.left_frame, row=11, column=0, pady=10, padx=10, sticky='ew')

        self.random_graph_button = ctk.CTkButton(self, text="Generate a graph", command=self.generate_graph_dialog)
        self.random_graph_button.grid(in_=self.left_frame, row=9, column=0, pady=10, padx=10, sticky='ew')

        self.delete_node_button = ctk.CTkButton(self.left_frame, text="Delete Node", command=self.delete_node, width=20)
        self.delete_node_button.grid(row=6, column=0, pady=10, padx=10, sticky='e')

        self.delete_edge_button = ctk.CTkButton(self.left_frame, text="Delete Edge", command=self.delete_edge, width = 20)
        self.delete_edge_button.grid(row=7, column=0, pady=10, padx=10, sticky='e')

        self.next_step_button = ctk.CTkButton(self, text="Next Step", command=self.next_step)
        self.next_step_button.grid(in_=self.right_frame, row=4, pady=20, columnspan = 2)
        self.next_step_button.configure(state='disabled')  # Disabled by default, enabled when Prim's starts

        self.toggle_mst_button = ctk.CTkButton(self.right_frame, text="Show MST only", command=self.toggle_mst_view)
        self.toggle_mst_button.grid(row=5, pady=10, columnspan = 2)
        self.toggle_mst_button.configure(state='disabled')  # Start as disabled

        self.import_graph_button = ctk.CTkButton(self, text="Import Graph", width=20, command=self.import_graph)
        self.import_graph_button.grid(in_=self.left_frame, row=10, column=0, pady=10, padx=10, sticky='ew')


        # Text widget to display Prim's algorithm steps
        self.info_text_widget = ctk.CTkTextbox(self, height=500, width=300)
        self.info_text_widget.grid(in_=self.right_frame, row=2, column=0, columnspan = 2, pady=10, padx=10, sticky='ew')

        
        # Placeholder for empty canvas message
        self.placeholder_text_id = self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text="Click on the canvas to create a node.",
            fill="#bbbbbb",  # Light grey color
            font=("TkDefaultFont", 18, "italic"),
            state="normal"  # Starts with the text shown
        )


        # Configure the grid layout to allow for resizing
        self.columnconfigure(1, weight=1)
        for i in range(8):  
            self.rowconfigure(i, weight=1)
    

    # For updating all node related things in drop down menus
    def update_node_options(self):
        # Update the options in the dropdown menus for start nodes
        start_menu = self.start_node_menu["menu"]
        start_menu.delete(0, "end")
        for node in self.nodes:
            print(f"Adding {node.identifier} to start node menu")
            start_menu.add_command(label=node.identifier, command=tk._setit(self.start_node_var, node.identifier))
            
        # Update the options in the dropdown menus for end nodes
        end_menu = self.end_node_menu["menu"]
        end_menu.delete(0, "end")
        for node in self.nodes:
            print(f"Adding {node.identifier} to end node menu")
            end_menu.add_command(label=node.identifier, command=tk._setit(self.end_node_var, node.identifier))
        
        # Update the options in the dropdown menu for starting vertex
        start_vertex_menu = self.start_vertex_menu["menu"]
        start_vertex_menu.delete(0, "end")
        for node in self.nodes:
            start_vertex_menu.add_command(label=node.identifier, command=tk._setit(self.start_vertex_var, node.identifier))
        
        # Update the options in the dropdown menu for node deletion
        delete_node_menu = self.delete_node_menu["menu"]
        delete_node_menu.delete(0, "end")
        for node in self.nodes:
            delete_node_menu.add_command(label=node.identifier, command=tk._setit(self.delete_node_var, node.identifier))


    # For updating all edge related things in drop down menus
    def update_edge_options(self):
        # Update the options in the dropdown menu for edge deletion
        delete_edge_menu = self.delete_edge_menu["menu"]
        delete_edge_menu.delete(0, "end")
        for edge in self.edges:
            edge_identifier = f"{edge.start_node.identifier} - {edge.end_node.identifier}"
            delete_edge_menu.add_command(label=edge_identifier, command=tk._setit(self.delete_edge_var, edge_identifier))

        if not self.edges:  # Add placeholder text if no edges are left
            delete_edge_menu.add_command(label="No edges available")

    # Generic method to reset the dropdown menus and weight entry field to default values
    def default_dropdown_labels(self):
        self.start_vertex_var.set("Source")  # Default values for dropdowns
        self.start_node_var.set("")
        self.end_node_var.set("")
        self.weight_var.set("")
        self.delete_node_var.set("")
        self.finalize_button.configure(text="Run Prims")  # Reset the button text
    

    # Method to show the placeholder text on the canvas
    def show_placeholder_text(self):
        if not self.nodes and not self.edges:  # If there are no nodes or edges
            self.canvas.itemconfig(self.placeholder_text_id, state="normal")
    

    # Method to hide the placeholder text on the canvas
    def hide_placeholder_text(self):
        self.canvas.itemconfig(self.placeholder_text_id, state="hidden")