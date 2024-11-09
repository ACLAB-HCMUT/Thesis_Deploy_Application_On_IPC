import customtkinter as ctk
from PIL import Image
<<<<<<< HEAD
import os
from constant import *
=======
>>>>>>> 3729710827dfcf61be214c7711f5aef27eb01601

class SignInView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set up image
<<<<<<< HEAD
        self.side_img_data = Image.open(os.path.join(base_path, "assets", "img", "side_img.png"))
        self.email_icon_data = Image.open(os.path.join(base_path, "assets", "img", "email_icon.png"))
        self.password_icon_data = Image.open(os.path.join(base_path, "assets", "img", "password_icon.png"))
        self.google_icon_data = Image.open(os.path.join(base_path, "assets", "img", "google_icon.png"))
=======
        self.side_img_data = Image.open("assets/img/side_img.png")
        self.email_icon_data = Image.open("assets/img/email_icon.png")
        self.password_icon_data = Image.open("assets/img/password_icon.png")
        self.google_icon_data = Image.open("assets/img/google_icon.png")
>>>>>>> 3729710827dfcf61be214c7711f5aef27eb01601

        self.side_img = ctk.CTkImage(dark_image=self.side_img_data, light_image=self.side_img_data, size=(500, 600))
        self.email_icon = ctk.CTkImage(dark_image=self.email_icon_data, light_image=self.email_icon_data, size=(20, 20))
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

        # Login label
        self.login_label = ctk.CTkLabel(self.login_frame, text="Login Page", font=ctk.CTkFont(size=30, weight="bold"), text_color="#601E88", anchor="w", justify="left").pack(anchor="w", pady=(50, 5), padx=(25, 0))

        # Email entry
        self.email_label = ctk.CTkLabel(self.login_frame,text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        self.email_entry = ctk.CTkEntry(self.login_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.email_entry.pack(anchor="w", pady=(0, 20), padx=(25, 0))

        # Password entry
        self.email_label = ctk.CTkLabel(self.login_frame,text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.password_icon, compound="left").pack(anchor="w", padx=(25, 0))
        self.password_entry = ctk.CTkEntry(self.login_frame, width=225, show="*", fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.password_entry.pack(anchor="w", padx=(25, 0))

        # Forgot password label
        self.forgot_password = ctk.CTkLabel(self.login_frame, text="Forgot your password?", font=("Arial", 12), text_color="#601E88", anchor="w")
        self.forgot_password.pack(anchor="w", pady=(5, 0), padx=(128, 0))

        # Login button
        self.login_btn = ctk.CTkButton(self.login_frame, text="Login", width=225, height=30, fg_color="#601E88", hover_color="#E6952D", text_color="#FFFFFF", font=("Arial Bold", 18))
        self.login_btn.pack(anchor="w", pady=(20, 0), padx=(25, 0))

        # Credentials status label
        self.cred_status_label = ctk.CTkLabel(self.login_frame, text="", font=("Arial", 12), text_color="#FF0000", anchor="w")
        self.cred_status_label.pack(anchor="w", pady=(5, 0), padx=(25, 0))

        # # OR label
        # self.or_label = ctk.CTkLabel(self.login_frame, text="OR", font=("Arial Bold", 12), text_color="#601E88", anchor="w").pack(anchor="w", pady=(5, 0), padx=(120, 0))

        # # Google login button
        # self.google_login_button = ctk.CTkButton(self.login_frame, text="Continue with Google", image=self.google_icon, width=225, height=30, fg_color="#601E88", hover_color="#E6952D", text_color="#FFFFFF", font=("Arial Bold", 16))
        # self.google_login_button.pack(anchor="w", pady=(5, 0), padx=(25, 0))

        # Sign Up label
        self.signup_label = ctk.CTkLabel(self.login_frame, text="Don't have an account? Sign up here", font=("Arial Bold", 12), text_color="#601E88", anchor="w")
        self.signup_label.pack(anchor="w", pady=(0, 0), padx=(25, 0))

        # Sign Up button
        # self.signup_btn = ctk.CTkButton(self.login_frame, text="Sign up", width=150, height=50, fg_color="#eeeee4", hover_color="#E6952D", text_color="#601E88", font=("Arial Bold", 18))
        # self.signup_btn.pack(anchor="w", pady=(20, 0), padx=(60, 0))