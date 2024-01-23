# In a new file, perhaps named main_menu.py
import customtkinter as ctk
from vp_graph_visualiser import VisualisingPrims

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Main Menu")
        self.geometry("300x200")  # Adjust the size as needed

        # Main menu buttons
        self.graph_visualiser_button = ctk.CTkButton(self, text="Graph Visualiser", command=self.launch_graph_visualiser)
        self.graph_visualiser_button.pack(pady=10)

        self.complexity_analyser_button = ctk.CTkButton(self, text="Complexity Analyser", command=self.launch_complexity_analyser)
        self.complexity_analyser_button.pack(pady=10)

        self.help_button = ctk.CTkButton(self, text="Help", command=self.launch_help)
        self.help_button.pack(pady=10)

    def launch_graph_visualiser(self):
        self.destroy()  # Close the main menu window
        visualiser = VisualisingPrims()
        visualiser.mainloop()

    def launch_complexity_analyser(self):
        ctk.messagebox.showinfo("Complexity Analyser", "This feature is under development.")

    def launch_help(self):
        ctk.messagebox.showinfo("Help", "How can we assist you?")
