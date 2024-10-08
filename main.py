import tkinter as tk
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from controller.user_controller import UserController
from models.user_model import UserModel
from views.user_view import UserView

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("My Application")

    # Thay đổi biểu tượng bằng PhotoImage
    icon = ImageTk.PhotoImage(Image.open('/home/anhkhoa01010902/iot_desktop_app/assets/farm_image.png'))
    root.iconphoto(True, icon)

    # Create instances of Model, View, and Controller
    user_model = UserModel()
    user_view = UserView(root)
    user_controller = UserController(user_model, user_view, root)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
