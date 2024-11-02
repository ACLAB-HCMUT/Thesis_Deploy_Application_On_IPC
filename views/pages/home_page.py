import customtkinter as ctk

class HomePage:
    def __init__(self, root, app, username):
        self.root = root
        self.app = app

        # Frame Home căn giữa
        self.frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Tiêu đề chào mừng
        welcome_label = ctk.CTkLabel(self.frame, text=f"Welcome, {username}!", font=("Arial", 24))
        welcome_label.pack(pady=20)

        # Nút Logout
        logout_button = ctk.CTkButton(
            self.frame, text="Logout", command=self.logout, fg_color="#ff6347"
        )
        logout_button.pack(pady=10)

    def logout(self):
        """Xử lý đăng xuất và quay lại trang Login."""
        self.app.show_login_page()
