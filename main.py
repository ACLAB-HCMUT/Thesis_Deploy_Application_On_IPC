import customtkinter
from controllers.main_controller import MainController


if __name__ == "__main__":
    root = customtkinter.CTk()  # Tạo cửa sổ chính
    root.geometry("800x600")  # Kích thước cửa sổ chính

    controller = MainController(root)

    root.mainloop()
