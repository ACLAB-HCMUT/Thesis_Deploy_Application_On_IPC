import customtkinter as ctk
from PIL import Image
from controller.user_controller import UserController
from models.user_model import UserModel
from views.user_view import UserView
import os

def main():
    # Create the main application window
    root = ctk.CTk()  # Use CTk instead of Tk
    root.title("My Application")
    root.geometry("800x600")  # Set the window size

    # Set the appearance mode (optional)
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create instances of Model, View, and Controller
    user_model = UserModel()
    user_view = UserView(root)
    user_controller = UserController(user_model, user_view, root)

    # Configure grid for dynamic resizing
    root.grid_rowconfigure(0, weight=1)  # Allow the first row to expand
    root.grid_columnconfigure(1, weight=1)  # Allow the first column to expand

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()

