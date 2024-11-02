import customtkinter as ctk
from views.pages.login_page import LoginPage
from views.pages.register_page import RegisterPage
from views.pages.home_page import HomePage

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("400x300")
        self.root.title("Your App Name")
        self.show_login_page()

    def show_login_page(self):
        self.clear_window()
        self.login_page = LoginPage(self.root, self)

    def show_register_page(self):
        self.clear_window()
        self.register_page = RegisterPage(self.root, self)

    def show_home_page(self, username):
        """Hiển thị HomePage với tên người dùng."""
        self.clear_window()
        self.home_page = HomePage(self.root, self, username)  # Truyền username vào

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
