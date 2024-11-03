from tkinter import Frame, Label, Entry, Checkbutton, Button, BooleanVar
import customtkinter as ctk
from PIL import Image

class SignUpView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = Label(self, text="Create a new account")
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.fullname_label = Label(self, text="Full Name")
        self.fullname_input = Entry(self)
        self.fullname_label.grid(row=1, column=0, padx=10, sticky="w")
        self.fullname_input.grid(row=1, column=1, padx=(0, 20), sticky="ew")

        self.username_label = Label(self, text="Username")
        self.username_input = Entry(self)
        self.username_label.grid(row=2, column=0, padx=10, sticky="w")
        self.username_input.grid(row=2, column=1, padx=(0, 20), sticky="ew")

        self.password_label = Label(self, text="Password")
        self.password_input = Entry(self, show="*")
        self.password_label.grid(row=3, column=0, padx=10, sticky="w")
        self.password_input.grid(row=3, column=1, padx=(0, 20), sticky="ew")

        self.has_agreed = BooleanVar()
        self.agreement = Checkbutton(
            self,
            text="I've agreed to the Terms & Conditions",
            variable=self.has_agreed,
            onvalue=True,
            offvalue=False,
        )
        self.agreement.grid(row=4, column=1, padx=0, sticky="w")

        self.signup_btn = Button(self, text="Sign Up")
        self.signup_btn.grid(row=5, column=1, padx=0, pady=10, sticky="w")

        self.signin_option_label = Label(self, text="Already have an account?")
        self.signin_btn = Button(self, text="Sign In")
        self.signin_option_label.grid(row=6, column=1, sticky="w")
        self.signin_btn.grid(row=7, column=1, sticky="w")

        # Set up image
        # self.side_img_data = Image.open("assets/img/side_img.png")
        # self.email_icon_data = Image.open("assets/img/email_icon.png")
        # self.password_icon_data = Image.open("assets/img/password_icon.png")
        # self.google_icon_data = Image.open("assets/img/google_icon.png")

        # self.side_img = ctk.CTkImage(dark_image=self.side_img_data, light_image=self.side_img_data, size=(500, 600))
        # self.email_icon = ctk.CTkImage(dark_image=self.email_icon_data, light_image=self.email_icon_data, size=(20, 20))
        # self.password_icon = ctk.CTkImage(dark_image=self.password_icon_data, light_image=self.password_icon_data, size=(20, 20))
        # self.google_icon = ctk.CTkImage(dark_image=self.google_icon_data, light_image=self.google_icon_data, size=(17, 17))

        # # Configure grid layout
        # self.grid_columnconfigure(0, weight=0)
        # self.grid_columnconfigure(1, weight=1)

        # # Create side image
        # ctk.CTkLabel(self, text="", image=self.side_img).pack(expand=True, side="left")

        # # Create login frame
        # self.login_frame = ctk.CTkFrame(self, width=310, height=600, fg_color="#FFFFFF")
        # self.login_frame.pack_propagate(0)
        # self.login_frame.pack(expand=True, side="right")

        # # Login label
        # self.login_label = ctk.CTkLabel(self.login_frame, text="Create A New Account", font=ctk.CTkFont(size=30, weight="bold"), text_color="#601E88", anchor="w", justify="left").pack(anchor="w", pady=(50, 5), padx=(25, 0))

        # # Fullname input
        # self.fullname_label = ctk.CTkLabel(self.login_frame,text="  Full name:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        # self.fullname_input = ctk.CTkEntry(self.login_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        # self.fullname_input.pack(anchor="w", pady=(0, 20), padx=(25, 0))

        # # Email input
        # self.email_label = ctk.CTkLabel(self.login_frame,text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        # self.email_input = ctk.CTkEntry(self.login_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        # self.email_input.pack(anchor="w", pady=(0, 20), padx=(25, 0))

        # # Password input
        # self.email_label = ctk.CTkLabel(self.login_frame,text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.password_icon, compound="left").pack(anchor="w", padx=(25, 0))
        # self.password_input = ctk.CTkEntry(self.login_frame, width=225, show="*", fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        # self.password_input.pack(anchor="w", padx=(25, 0))

        # # Login button
        # self.login_btn = ctk.CTkButton(self.login_frame, text="Login", width=200, height=50, fg_color="#601E88", hover_color="#E6952D", text_color="#FFFFFF", font=("Arial Bold", 18))
        # self.login_btn.pack(anchor="w", pady=(40, 0), padx=(35, 0))

        # # Sign Up button
        # self.signup_btn = ctk.CTkButton(self.login_frame, text="Sign up", width=150, height=50, fg_color="#eeeee4", hover_color="#E6952D", text_color="#601E88", font=("Arial Bold", 18))
        # self.signup_btn.pack(anchor="w", pady=(20, 0), padx=(60, 0))