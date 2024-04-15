from interface.vp_main_gui import MainMenu

class MainApplication:
    def __init__(self):
        self.main_menu = MainMenu()

    def run(self):
        self.main_menu.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run()