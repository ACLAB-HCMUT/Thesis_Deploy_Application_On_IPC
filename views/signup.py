from tkinter import Frame, Label, Entry, Checkbutton, Button, BooleanVar
import customtkinter as ctk
from PIL import Image
import os
from constant import *

class SignUpView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set up image
        self.side_img_data = Image.open(os.path.join(base_path, "assets", "img", "side_img.png"))
        self.fullname_icon_data = Image.open(os.path.join(base_path, "assets", "img", "fullname_icon.png"))
        self.email_icon_data = Image.open(os.path.join(base_path, "assets", "img", "email_icon.png"))
        self.phone_icon_data = Image.open(os.path.join(base_path, "assets", "img", "phone_icon.png"))
        self.address_icon_data = Image.open(os.path.join(base_path, "assets", "img", "address_icon.png"))
        self.password_icon_data = Image.open(os.path.join(base_path, "assets", "img", "password_icon.png"))
        self.google_icon_data = Image.open(os.path.join(base_path, "assets", "img", "google_icon.png"))

        self.side_img = ctk.CTkImage(dark_image=self.side_img_data, light_image=self.side_img_data, size=(500, 600))
        self.fullname_icon = ctk.CTkImage(dark_image=self.fullname_icon_data, light_image=self.fullname_icon_data, size=(20, 20))
        self.email_icon = ctk.CTkImage(dark_image=self.email_icon_data, light_image=self.email_icon_data, size=(20, 20))
        self.phone_icon = ctk.CTkImage(dark_image=self.phone_icon_data, light_image=self.phone_icon_data, size=(20, 20))
        self.address_icon = ctk.CTkImage(dark_image=self.address_icon_data, light_image=self.address_icon_data, size=(20, 20))
        self.password_icon = ctk.CTkImage(dark_image=self.password_icon_data, light_image=self.password_icon_data, size=(20, 20))
        self.google_icon = ctk.CTkImage(dark_image=self.google_icon_data, light_image=self.google_icon_data, size=(17, 17))

        # Configure grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Create side image
        ctk.CTkLabel(self, text="", image=self.side_img).pack(expand=True, side="left")

        # Create login frame
        self.login_frame = ctk.CTkFrame(self, width=310, height=600, fg_color="#FFFFFF")
        self.login_frame.pack_propagate(0)
        self.login_frame.pack(expand=True, side="right")

        # Sign up label
        self.signup_label = ctk.CTkLabel(self.login_frame, text="Create New Account", font=ctk.CTkFont(size=28, weight="bold"), text_color="#601E88", anchor="w", justify="left").pack(anchor="w", pady=(50, 5), padx=(25, 0))

        # Fullname input
        self.fullname_label = ctk.CTkLabel(self.login_frame,text="  Full name:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.fullname_icon, compound="left").pack(anchor="w", pady=(15, 0), padx=(25, 0))
        self.fullname_input = ctk.CTkEntry(self.login_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.fullname_input.pack(anchor="w", pady=(0, 15), padx=(25, 0))

        # Email input
        self.email_label = ctk.CTkLabel(self.login_frame,text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.email_icon, compound="left").pack(anchor="w", padx=(25, 0))
        self.email_input = ctk.CTkEntry(self.login_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.email_input.pack(anchor="w", pady=(0, 15), padx=(25, 0))

        # Password input
        self.email_label = ctk.CTkLabel(self.login_frame,text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.password_icon, compound="left").pack(anchor="w", padx=(25, 0))
        self.password_input = ctk.CTkEntry(self.login_frame, width=225, show="*", fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.password_input.pack(anchor="w", pady=(0, 15), padx=(25, 0))

        # Phone number input
        self.phone_label = ctk.CTkLabel(self.login_frame, text="  Phone number:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.phone_icon, compound="left").pack(anchor="w", padx=(25, 0))
        self.phone_input = ctk.CTkEntry(self.login_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.phone_input.pack(anchor="w", pady=(0, 15), padx=(25, 0))

        # Address input
        self.address_label = ctk.CTkLabel(self.login_frame, text="  Address:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.address_icon, compound="left").pack(anchor="w", padx=(25, 0))
        self.address_input = ctk.CTkEntry(self.login_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.address_input.pack(anchor="w", pady=(0, 15), padx=(25, 0))

        # Sign Up button
        self.signup_btn = ctk.CTkButton(self.login_frame, text="Sign up", width=225, height=30, fg_color="#601E88", hover_color="#E6952D", text_color="#FFFFFF", font=("Arial Bold", 18))
        self.signup_btn.pack(anchor="w", pady=(20, 0), padx=(25, 0))

        # Back to login button
        self.login_btn = ctk.CTkButton(self.login_frame, text="Back to login", width=225, height=30, fg_color="#EEEEE4", hover_color="#E6952D", text_color="#601E88", font=("Arial Bold", 18))
        self.login_btn.pack(anchor="w", pady=(20, 0), padx=(25, 0))