import customtkinter as ctk
from views.pages.login_page import LoginPage
from views.pages.register_page import RegisterPage
from views.pages.home_page import HomePage
from views.components.header import Header
from views.components.sidebar import Sidebar
from views.components.footer import Footer

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Application")

        # Tạo các component chính
        self.header = Header(self.root)
        self.sidebar = Sidebar(self.root, self)

        # Frame nội dung để chuyển đổi các trang
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Footer component
        self.footer = Footer(self.root)

        # Đặt grid layout cho root window
        self.root.grid_rowconfigure(1, weight=1)  # Nội dung có thể co giãn
        self.root.grid_columnconfigure(1, weight=1)

        # Bắt đầu với trang đăng nhập
        self.show_login_page()

    def show_login_page(self):
        self.clear_content_frame()
        LoginPage(self.content_frame, self)

    def show_register_page(self):
        self.clear_content_frame()
        RegisterPage(self.content_frame, self)

    def show_home_page(self):
        self.clear_content_frame()
        HomePage(self.content_frame)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()