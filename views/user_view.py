import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import customtkinter
import os
from PIL import Image

# Set the appearance mode (dark/light)
customtkinter.set_appearance_mode("dark")  # You can also use "light"
customtkinter.set_default_color_theme("blue")  # Custom color theme (optional)

class UserView:
    def __init__(self, root):
        self.root = root
        # self.width = 900
        # self.height = 600

        # self.root.title("CustomTkinter Login Example")
        # self.root.geometry(f"{self.width}x{self.height}")
        # self.root.resizable(False, False)

        # Set the background color of the root window (Tkinter root window uses bg, not fg_color)
        self.root.configure(bg="#344955")

        # Create login frame with rounded corners and a background color
        self.login_frame = customtkinter.CTkFrame(self.root, corner_radius=20, fg_color="#232f34")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

        # Login label
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Login Page",
                                                  font=customtkinter.CTkFont(size=30, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=35, pady=(20, 20))

        # Username entry
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=35, pady=(20, 20))

        # Password entry
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="Password")
        self.password_entry.grid(row=2, column=0, padx=35, pady=(0, 20))

        # Login button with hover effect
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", width=200, fg_color="#F9AA33",
                                                    hover_color="#E6952D")
        self.login_button.grid(row=3, column=0, padx=60, pady=(0, 30))
        

        # Message Label
        # self.message_label = customtkinter.CTkLabel(self.root, text="", font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.message_label.pack(pady=10)

        # Action Button for Login or Register
        # self.action_button = ttk.Button(self.root, text="Login", bootstyle=PRIMARY)
        # self.action_button.pack(pady=10)

        # Button to switch between Login and Register
        # self.switch_button = ttk.Button(self.root, text="Register", bootstyle=LINK)
        # self.switch_button.pack(pady=10)

        # Variable to track form type (login or register)
        self.is_login_form = True

    def toggle_form(self):
        if self.is_login_form:
            # Switch to Register form
            self.action_button.configure(text="Register")
            self.switch_button.configure(text="Back to Login")
            self.confirm_password_entry.grid()  # Show confirm password field
            self.set_message("Register a new account", bootstyle=INFO)
            self.is_login_form = False
        else:
            # Switch to Login form
            self.action_button.configure(text="Login")
            self.switch_button.configure(text="Register")
            self.confirm_password_entry.grid_remove()  # Hide confirm password field
            self.set_message("Welcome back! Please login", bootstyle=INFO)
            self.is_login_form = True

    def get_username(self):
        return self.username_entry.get()

    def get_password(self):
        return self.password_entry.get()

    def get_confirm_password(self):
        return self.confirm_password_entry.get()

    def set_message(self, message, bootstyle=INFO):
        self.message_label.configure(text=message)

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)

    