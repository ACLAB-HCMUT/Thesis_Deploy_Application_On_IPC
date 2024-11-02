import customtkinter as ctk

class Header:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, height=50)
        self.frame.pack(fill="x")

        app_name_label = ctk.CTkLabel(self.frame, text="Farmer Management", font=("Arial", 18))
        app_name_label.pack(pady=10)
