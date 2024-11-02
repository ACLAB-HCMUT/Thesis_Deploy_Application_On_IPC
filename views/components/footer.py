import customtkinter as ctk

class Footer:
    def __init__(self, root):
        footer = ctk.CTkFrame(root, height=50)
        footer.grid(row=2, column=0, columnspan=2, sticky="nsew")
        ctk.CTkLabel(footer, text="Footer", font=("Arial", 12)).pack()
