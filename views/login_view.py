import customtkinter
import tkinter.messagebox as messagebox  # Import để sử dụng MessageBox


# Set appearance mode and color theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class LoginView(customtkinter.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, width=300, height=200)  # Đặt kích thước khung nhỏ hơn
        self.controller = controller

        # Set main window background color
        master.configure(bg="#2E2E3A")  # Màu nền xám tối cho tổng thể dịu mắt

        # Tạo khung đăng nhập với màu xám nhạt
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=20, fg_color="#4D4D4D")  # Màu xám nhạt cho khung
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")  # Căn giữa khung đăng nhập

        # Tiêu đề đăng nhập
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Login Page",
                                                  font=customtkinter.CTkFont(size=24, weight="bold"), 
                                                  text_color="#FFFFFF")  # Màu trắng để nổi bật trên nền tối
        self.login_label.grid(row=0, column=0, padx=35, pady=(20, 10))

        # Trường nhập tên người dùng
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="Username",
                                                     placeholder_text_color="#C4C4C4")
        self.username_entry.grid(row=1, column=0, padx=35, pady=(5, 10))

        # Trường nhập mật khẩu
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="Password",
                                                     placeholder_text_color="#C4C4C4")
        self.password_entry.grid(row=2, column=0, padx=35, pady=(5, 10))

        # Nút đăng nhập với hiệu ứng khi di chuột
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", width=200,
                                                    fg_color="#F9AA33", hover_color="#E6952D", 
                                                    text_color="#FFFFFF", font=customtkinter.CTkFont(weight="bold"), 
                                                    command=self.login)
        self.login_button.grid(row=3, column=0, padx=35, pady=(20, 10))

        # Label thông báo kết quả login (ban đầu ẩn)
        self.message_label = customtkinter.CTkLabel(self.login_frame, text="", 
                                                    font=customtkinter.CTkFont(size=14, weight="bold"))
        self.message_label.grid(row=4, column=0, padx=35, pady=(5, 20))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.controller.handle_login(username, password):
            self.show_success_popup()
            self.controller.switch_to_home()
        else:
            self.message_label.configure(text="Incorrect user or password!", text_color="#FF0000")  # Màu đỏ cho thông báo sai
        self.message_label.update()

    def show_success_popup(self):
        # Tạo một cửa sổ con (popup)
        popup = customtkinter.CTkToplevel(self)
        popup.geometry("300x150")  # Đặt kích thước cho popup
        popup.title("Success")

        # Thêm các tùy chỉnh đẹp cho popup
        popup.configure(fg_color="#2B2B2B")  # Màu nền tối cho pop-up
        popup.corner_radius = 20  # Bo góc cho pop-up

        # Đặt label cho popup với màu sắc và font đẹp hơn
        success_label = customtkinter.CTkLabel(popup, text="Login Successful!", 
                                               font=customtkinter.CTkFont(size=18, weight="bold"),
                                               text_color="#00FF7F")  # Màu xanh lá cây sáng hơn
        success_label.pack(pady=20)

        # Thêm hiệu ứng bo góc cho pop-up
        success_frame = customtkinter.CTkFrame(popup, fg_color="#333333", corner_radius=20)
        success_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Thêm label thông báo vào success_frame để tạo bố cục đẹp hơn
        message_label = customtkinter.CTkLabel(success_frame, text="Redirecting to Home...", 
                                               font=customtkinter.CTkFont(size=14), 
                                               text_color="#FFFFFF")
        message_label.pack(pady=10)

        # Tự động tắt popup sau 2 giây
        popup.after(2000, popup.destroy)

    def reset_fields(self):
        self.username_entry.delete(0, customtkinter.END)
        self.password_entry.delete(0, customtkinter.END)
        self.message_label.configure(text="")  # Xóa thông báo
        self.message_label.update()