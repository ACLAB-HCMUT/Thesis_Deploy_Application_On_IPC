import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class UserView:
    def __init__(self, root):
        self.root = root
        self.root.title("IoT Application")
        self.root.geometry("400x300")

        # Form container
        self.form_frame = ttk.Frame(self.root)
        self.form_frame.pack(pady=20)

        # Username
        self.username_label = ttk.Label(self.form_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.form_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password
        self.password_label = ttk.Label(self.form_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.form_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Confirm Password (for registration only) 
        self.confirm_password_label = ttk.Label(self.form_frame, text="Confirm Password:")
        self.confirm_password_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.confirm_password_label.grid(row=2, column=0, padx=5, pady=5)
        self.confirm_password_entry = ttk.Entry(self.form_frame, width=30, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)
        self.confirm_password_label.grid_remove()  # Hide this field initially
        self.confirm_password_entry.grid_remove()  # Hide this field initially
        

        # Message Label
        self.message_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.message_label.pack(pady=10)

        # Action Button for Login or Register
        self.action_button = ttk.Button(self.root, text="Login", bootstyle=PRIMARY)
        self.action_button.pack(pady=10)

        # Button to switch between Login and Register
        self.switch_button = ttk.Button(self.root, text="Register", bootstyle=LINK)
        self.switch_button.pack(pady=10)

        # Variable to track form type (login or register)
        self.is_login_form = True

    def toggle_form(self):
        if self.is_login_form:
            # Switch to Register form
            self.action_button.config(text="Register")
            self.switch_button.config(text="Back to Login")
            self.confirm_password_entry.grid()  # Show confirm password field
            self.set_message("Register a new account", bootstyle=INFO)
            self.is_login_form = False
        else:
            # Switch to Login form
            self.action_button.config(text="Login")
            self.switch_button.config(text="Register")
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
        self.message_label.config(text=message, bootstyle=bootstyle)

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)
