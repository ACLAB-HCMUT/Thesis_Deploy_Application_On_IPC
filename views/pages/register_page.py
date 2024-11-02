import customtkinter as ctk
from db import db

class RegisterPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # Tham chiếu đến App để điều hướng

        # Frame Register căn giữa
        self.frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Tiêu đề
        title_label = ctk.CTkLabel(self.frame, text="Create a New Account", font=("Arial", 20))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Các trường đăng ký
        labels = ["Name", "Email", "Username", "Password", "Role"]
        self.entries = {}

        for idx, text in enumerate(labels):
            label = ctk.CTkLabel(self.frame, text=f"{text}:", font=("Arial", 14))
            label.grid(row=idx + 1, column=0, pady=5, padx=10, sticky="e")
            entry = ctk.CTkEntry(self.frame, width=200, show="*" if text == "Password" else None)
            entry.grid(row=idx + 1, column=1, pady=5, padx=10, sticky="w")
            self.entries[text.lower()] = entry

        # Tạo hàng chứa Register và Back Button
        button_frame = ctk.CTkFrame(self.frame)
        button_frame.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

        # Nút Register
        self.register_button = ctk.CTkButton(
            button_frame, text="Register", command=self.register_user, fg_color="#5cb85c"
        )
        self.register_button.grid(row=0, column=0, padx=10)

        # Nút Back to Login
        self.back_button = ctk.CTkButton(
            button_frame, text="Back to Login", command=self.app.show_login_page, fg_color="#ff6347"
        )
        self.back_button.grid(row=0, column=1, padx=10)

        # Ràng buộc phím Enter và Space cho các nút
        self.root.bind("<Return>", lambda e: self.invoke_widget(self.register_button))

        # Thiết lập Tab Order và Phím Space
        self.setup_tab_order()

    def setup_tab_order(self):
        """Thiết lập thứ tự focus cho các widget và hỗ trợ phím Space."""
        widgets = list(self.entries.values()) + [self.register_button, self.back_button]

        # Ràng buộc Tab giữa các widget
        for i, widget in enumerate(widgets):
            widget.bind("<Tab>", lambda e, w=widgets[(i + 1) % len(widgets)]: w.focus_set())

            # Đảm bảo nút có thể nhận focus và hoạt động với phím Space
            if isinstance(widget, ctk.CTkButton):
                widget.bind("<space>", lambda e: self.invoke_widget(widget))
                widget.bind("<FocusIn>", lambda e, w=widget: self.on_focus(w))
                widget.bind("<FocusOut>", lambda e, w=widget: self.on_focus_out(w))

    def invoke_widget(self, widget):
        """Kích hoạt widget nếu có phương thức invoke."""
        if hasattr(widget, 'invoke') and widget == self.root.focus_get():
            widget.invoke()

    def on_focus(self, widget):
        """Thay đổi màu khi nút được focus."""
        widget.configure(fg_color="#3b5998")  # Màu khi nút có focus

    def on_focus_out(self, widget):
        """Khôi phục màu khi nút mất focus."""
        default_color = "#5cb85c" if widget == self.register_button else "#ff6347"
        widget.configure(fg_color=default_color)

    def register_user(self):
        """Xử lý đăng ký người dùng."""
        user_data = {field: entry.get() for field, entry in self.entries.items()}
        if all(user_data.values()):
            try:
                db["users"].insert_one(user_data)
                print("Registration successful!")
                self.app.show_login_page()  # Quay lại Login sau khi đăng ký thành công
            except Exception as e:
                print(f"Error during registration: {e}")
        else:
            print("All fields are required!")
