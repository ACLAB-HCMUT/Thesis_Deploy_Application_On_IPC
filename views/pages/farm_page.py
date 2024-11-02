# app/views/pages/farm_page.py
import tkinter as tk

class FarmPage(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        tk.Label(self, text="Farm Page").pack()
