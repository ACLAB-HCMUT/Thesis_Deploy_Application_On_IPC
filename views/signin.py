import customtkinter as ctk

class SignInView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Create login frame with rounded corners and a background color
        self.login_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#232f34")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Login label
        self.login_label = ctk.CTkLabel(self.login_frame, text="Login Page", font=ctk.CTkFont(size=30, weight="bold"), text_color="#FFFFFF")
        self.login_label.grid(row=0, column=0, padx=35, pady=(20,20))

        # Email entry
        self.email_entry = ctk.CTkEntry(self.login_frame, width=200, placeholder_text="Email")
        self.email_entry.grid(row=1, column=0, padx=35, pady=(20, 20))

        # Password entry
        self.password_entry = ctk.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="Password")
        self.password_entry.grid(row=2, column=0, padx=35, pady=(0, 20))

        # Login button
        self.login_btn = ctk.CTkButton(self.login_frame, text="Login", width=200, fg_color="#F9AA33", hover_color="#E6952D")
        self.login_btn.grid(row=3, column=0, padx=60, pady=(0, 30))

        # Sign Up button
        self.signup_btn = ctk.CTkButton(self.login_frame, text="Sign up", width=200, fg_color="#F9AA33", hover_color="#E6952D")
        self.signup_btn.grid(row=4, column=0, padx=60, pady=(0, 30))