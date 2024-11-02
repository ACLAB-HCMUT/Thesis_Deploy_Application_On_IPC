import customtkinter as ctk
from db import db

class LoginPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app

        # Frame Login căn giữa
        self.frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Tiêu đề
        title_label = ctk.CTkLabel(self.frame, text="Login to Your Account", font=("Arial", 20))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Trường nhập Username và Password
        self.username_entry = self.create_entry("Username", 1)
        self.password_entry = self.create_entry("Password", 2, show="*")

        # Tạo hàng chứa nút Login và Register
        button_frame = ctk.CTkFrame(self.frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Nút Login
        self.login_button = ctk.CTkButton(
            button_frame, text="Login", command=self.authenticate_user
        )
        self.login_button.grid(row=0, column=0, padx=10)

        # Nút Register
        self.register_button = ctk.CTkButton(
            button_frame, text="Register", command=self.app.show_register_page, fg_color="#007bff"
        )
        self.register_button.grid(row=0, column=1, padx=10)

        # Nhãn thông báo trạng thái
        self.status_label = ctk.CTkLabel(self.frame, text="")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Ràng buộc phím Enter để kích hoạt Login hoặc Register
        self.root.bind("<Return>", self.handle_enter_key)

        # Thiết lập Tab Order và Phím Space
        self.setup_tab_order()

    def create_entry(self, label_text, row, show=None):
        label = ctk.CTkLabel(self.frame, text=f"{label_text}:", font=("Arial", 14))
        label.grid(row=row, column=0, pady=5, padx=10, sticky="e")
        entry = ctk.CTkEntry(self.frame, width=200, show=show)
        entry.grid(row=row, column=1, pady=5, padx=10, sticky="w")
        return entry

    def setup_tab_order(self):
        """Thiết lập thứ tự focus cho các widget và hỗ trợ phím Space."""
        widgets = [
            self.username_entry,
            self.password_entry,
            self.login_button,
            self.register_button,
        ]

        # Ràng buộc Tab giữa các widget
        for i, widget in enumerate(widgets):
            widget.bind("<Tab>", lambda e, w=widgets[(i + 1) % len(widgets)]: w.focus_set())

            # Đảm bảo nút có thể nhận focus và hoạt động với phím Space
            if isinstance(widget, ctk.CTkButton):
                widget.bind("<space>", lambda e: self.invoke_widget(widget))
                widget.bind("<FocusIn>", lambda e, w=widget: self.on_focus(w))
                widget.bind("<FocusOut>", lambda e, w=widget: self.on_focus_out(w))

    def handle_enter_key(self, event):
        """Kích hoạt Login hoặc Register khi nhấn Enter."""
        focused_widget = self.root.focus_get()
        if focused_widget == self.login_button:
            self.invoke_widget(self.login_button)
        elif focused_widget == self.register_button:
            self.invoke_widget(self.register_button)

    def invoke_widget(self, widget):
        """Kích hoạt widget nếu có phương thức invoke."""
        if hasattr(widget, 'invoke'):
            widget.invoke()

    def on_focus(self, widget):
        """Thay đổi màu khi nút được focus."""
        widget.configure(fg_color="#3b5998")  # Màu khi nút có focus

    def on_focus_out(self, widget):
        """Khôi phục màu khi nút mất focus."""
        default_color = "#007bff" if widget == self.register_button else "#5cb85c"
        widget.configure(fg_color=default_color)

    def authenticate_user(self):
        """Xử lý đăng nhập."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Kiểm tra thông tin đăng nhập trong MongoDB
        user = db["users"].find_one({"username": username, "password": password})

        if user:
            self.status_label.configure(text="Login successful!", fg_color="green")
            self.app.show_home_page(username)  # Chuyển sang HomePage nếu đăng nhập thành công
        else:
            self.status_label.configure(text="Invalid username or password.", fg_color="red")