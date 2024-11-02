# user_page.py
import tkinter as tk  # Import tkinter for GUI components

class UserPage:
    def __init__(self, root, main_view):
        self.root = root
        self.main_view = main_view
        self.setup_gui()  # Set up the GUI layout

    def setup_gui(self):
        # Set up your GUI components here
        self.main_view.pack()  # Pack the main view into the root window
        label = tk.Label(self.main_view, text="Welcome to the User Page!")
        label.pack()  # Add a label or other widgets as needed

    def run(self):
        self.root.mainloop()  # Start the main GUI loop
