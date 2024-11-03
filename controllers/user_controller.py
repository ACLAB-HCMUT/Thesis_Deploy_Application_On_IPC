from PIL import Image
from views.user_view import UserView
from views.home_page import HomePage
from views.farm_page import display_farm_content
from views.settings_page import display_settings_content
import customtkinter
import os

class UserController:
    def __init__(self, model, view, root):
        self.model = model
        self.view = view
        self.root = root
        self.view.login_button.configure(command=self.handle_action)

    def handle_action(self):
        if self.view.is_login_form:
            self.login_user()
        else:
            self.register_user()

    def login_user(self):
        username = self.view.get_username()
        password = self.view.get_password()

        if self.model.login(username, password):
            # self.view.set_message(f"Welcome {username}!")
            # self.show_dashboard()
            # self.view.show_dashboard()
            HomePage.show_dashboard(self)
            
        # else:
        #     self.view.set_message("Invalid credentials!")

    def register_user(self):
        username = self.view.get_username()
        password = self.view.get_password()
        confirm_password = self.view.get_confirm_password()

        if password != confirm_password:
            self.view.set_message("Passwords do not match!")
            return

        if self.model.register(username, password):
            self.view.set_message(f"User {username} registered successfully!")
            self.view.clear_fields()
        else:
            self.view.set_message("User already exists!")

    def logout_user(self):
        # Clear the dashboard and show the login form again
        for widget in self.root.winfo_children():
            widget.destroy()