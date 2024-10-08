import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, LIGHT, INVERSE, LINK, SUCCESS, WARNING, DANGER, INFO
from PIL import Image, ImageTk
from views.user_view import UserView
from views.home_page import display_home_content
from views.farm_page import display_farm_content
from views.settings_page import display_settings_content

class UserController:
    def __init__(self, model, view, root):
        self.model = model
        self.view = view
        self.root = root

        # Set window transparency
        self.root.attributes("-alpha", 0.9)

        # Assign actions to buttons
        self.view.action_button.config(command=self.handle_action)
        self.view.switch_button.config(command=self.handle_action)

    def handle_action(self):
        if self.view.is_login_form:
            self.login_user()
        else:
            self.register_user()

    def login_user(self):
        username = self.view.get_username()
        password = self.view.get_password()

        if self.model.login(username, password):
            self.view.set_message(f"Welcome {username}!", bootstyle=SUCCESS)
            self.show_dashboard(username)
        else:
            self.view.set_message("Invalid credentials!", bootstyle=DANGER)

    def register_user(self):
        username = self.view.get_username()
        password = self.view.get_password()
        confirm_password = self.view.get_confirm_password()

        if password != confirm_password:
            self.view.set_message("Passwords do not match!", bootstyle=DANGER)
            return

        if self.model.register(username, password):
            self.view.set_message(f"User {username} registered successfully!", bootstyle=SUCCESS)
            self.view.clear_fields()
        else:
            self.view.set_message("User already exists!", bootstyle=WARNING)

    def show_dashboard(self, username):
        # Clear the login/register form
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create Navbar with Logo and Options
        navbar = ttk.Frame(self.root, bootstyle=PRIMARY)
        navbar.pack(side=tk.TOP, fill=tk.X)

        # Logo Section
        logo_frame = ttk.Frame(navbar, bootstyle=PRIMARY)
        logo_frame.pack(side=tk.LEFT, padx=20)

        # Load and display the logo image
        try:    
            logo_image = Image.open("/home/anhkhoa01010902/iot_desktop_app/controller/cee.jpg")  # Update path as necessary
            logo_image = logo_image.resize  ((40, 40))
            logo = ImageTk.PhotoImage(logo_image)

            logo_label = ttk.Label(logo_frame, image=logo, background="white")
            logo_label.image = logo  # Keep reference to avoid garbage collection
            logo_label.pack(side=tk.LEFT, padx=5)
        except Exception as e:
            print(f"Error loading logo image: {e}")

        # Display username next to the logo
        username_label = ttk.Label(logo_frame, text=username, font=("Arial", 14), bootstyle=INVERSE, background="white")
        username_label.pack(side=tk.LEFT, padx=5)

        # Navbar Options
        navbar_options_frame = ttk.Frame(navbar, bootstyle=PRIMARY)
        navbar_options_frame.pack(side=tk.RIGHT, padx=20)

        ttk.Button(navbar_options_frame, text="Notification", bootstyle=LINK).pack(side=tk.LEFT, padx=10)
        ttk.Button(navbar_options_frame, text="Farm", bootstyle=LINK, command=self.show_farm).pack(side=tk.LEFT, padx=10)
        ttk.Button(navbar_options_frame, text="Settings", bootstyle=LINK, command=self.show_settings).pack(side=tk.LEFT, padx=10)
        ttk.Button(navbar_options_frame, text="Logout", bootstyle=LINK, command=self.logout).pack(side=tk.LEFT, padx=10)

        # Sidebar setup
        self.sidebar = ttk.Frame(self.root, width=200, bootstyle=LIGHT)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Content Frame (This is the frame that will be updated dynamically)
        self.content = ttk.Frame(self.root)
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Sidebar buttons
        ttk.Button(self.sidebar, text="Home", bootstyle=LINK, command=self.show_home_page).pack(pady=10)
        ttk.Button(self.sidebar, text="Farm", bootstyle=LINK, command=self.show_farm).pack(pady=10)
        ttk.Button(self.sidebar, text="Settings", bootstyle=LINK, command=self.show_settings).pack(pady=10)

        # Show initial home page
        self.show_home_page()

    def show_home_page(self):
        self.update_content(display_home_content)

    def show_farm(self):
        self.update_content(display_farm_content)

    def show_settings(self):
        self.update_content(lambda frame: display_settings_content(frame, self.root))

    def update_content(self, content_function):
        # Clear the content frame before loading new content
        for widget in self.content.winfo_children():
            widget.destroy()

        # Call the content function to update the content frame
        content_function(self.content)

    def logout(self):
        # Clear the dashboard and show the login form again
        for widget in self.root.winfo_children():
            widget.destroy()

        # Reinitialize the login form
        self.view = UserView(self.root)
        self.view.action_button.config(command=self.handle_action)
        self.view.switch_button.config(command=self.handle_action)
        self.view.set_message("You have been logged out. Please log in again.", bootstyle=INFO)
