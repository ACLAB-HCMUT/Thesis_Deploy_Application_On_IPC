import customtkinter as ctk

class Sidebar:
    def __init__(self, root, app):
        sidebar = ctk.CTkFrame(root, width=200)
        sidebar.grid(row=1, column=0, sticky="nsew")

        buttons = [
            ("Home", app.show_home_page),
            ("Login", app.show_login_page),
            ("Register", app.show_register_page)
        ]

        for text, command in buttons:
            button = ctk.CTkButton(sidebar, text=text, command=command)
            button.pack(pady=10, padx=10, fill="x")
