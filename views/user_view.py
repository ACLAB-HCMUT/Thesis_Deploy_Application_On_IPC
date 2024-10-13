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

    def show_dashboard(self):
        # Load images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icons8-agriculture-color-70.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # Create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self.root, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Image Example", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        #sign out button
        self.sign_out_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=10, height=40, border_spacing=10, text="Sign Out")
        self.sign_out_button.grid(row=5, column=0, padx=20, pady=20, sticky="s")

        #appearance mode select
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Create home frame
        self.home_frame = customtkinter.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="CTkButton 1", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton 2", image=self.image_icon_image)
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton 3", image=self.image_icon_image)
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton 4", image=self.image_icon_image)
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # Create second frame
        self.second_frame = customtkinter.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.second_frame_button_1 = customtkinter.CTkButton(self.second_frame, text="CTkButton 1", image=self.image_icon_image)
        self.second_frame_button_1.grid(row=1, column=0, padx=20, pady=10)

        # Create third frame
        self.third_frame = customtkinter.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)

        self.third_frame_button_1 = customtkinter.CTkButton(self.third_frame, text="CTkButton 1 haha", image=self.image_icon_image)
        self.third_frame_button_1.grid(row=1, column=0, padx=20, pady=10)

        # Select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # Set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # Show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
