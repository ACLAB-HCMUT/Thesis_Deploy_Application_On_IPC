import customtkinter
<<<<<<< HEAD
=======
from connect_to_mongodb import *
>>>>>>> e9bab437f0db0820a6b15607368a26f3c80b1bee
from connect_to_rs485_relay import *
import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.patches as patches
from get_data_from_adafruit import *

<<<<<<< HEAD
=======
def get_data_from_database():
    data = connect_database("test")
    return data

print(get_data_from_database())

>>>>>>> e9bab437f0db0820a6b15607368a26f3c80b1bee

# Class định nghĩa TabView
class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Chọn màu nền trùng nhau cho cả frame và biểu đồ
        self.bg_color = "#222831"  # Màu nền bạn muốn cho frame và biểu đồ

        # Tạo các tab
        self.add("Biểu đồ độ ẩm")
        self.add("Biểu đồ nhiệt độ")

        # Tạo frame bo tròn cho biểu đồ độ ẩm
        humidity_frame = customtkinter.CTkFrame(self.tab("Biểu đồ độ ẩm"), corner_radius=20)
        humidity_frame.grid(row=0, column=0, padx=20, pady=20)

        # Gọi hàm vẽ biểu đồ độ ẩm và chèn vào frame
        self.plot_graph_humidity(humidity_frame)

        # Tạo frame bo tròn cho biểu đồ nhiệt độ
        temperature_frame = customtkinter.CTkFrame(self.tab("Biểu đồ nhiệt độ"), corner_radius=20)
        temperature_frame.grid(row=0, column=0, padx=20, pady=20)

        # Gọi hàm vẽ biểu đồ và chèn vào frame
        self.plot_graph_temperature(temperature_frame)

    def plot_graph_temperature(self, frame):
        # Tạo dữ liệu từ MongoDB
        data = pd.DataFrame(get_data_from_adafruit("cambien1"))

        x = data['created_at']
        y1 = data['value']

        # Áp dụng style cyberpunk
        plt.style.use('cyberpunk')

        # Tạo figure cho biểu đồ
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, y1, marker='o')

        # Làm cho đường sáng lên
        mplcyberpunk.make_lines_glow()

        # Gán nhãn trục và chú thích
        ax.set_xlabel('Time')
        ax.set_ylabel('Temperature')
        ax.legend()

        # Tạo lớp nền với góc bo tròn có màu trùng với frame
        round_background = patches.FancyBboxPatch(
            (0, 0), 1, 1, boxstyle="round,pad=0.05", facecolor=self.bg_color, edgecolor="none",
            transform=ax.transAxes, zorder=-1)

        ax.add_patch(round_background)  # Thêm nền bo tròn

        # Chèn biểu đồ vào giao diện Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)

    def plot_graph_humidity(self, frame):
        # Tạo dữ liệu từ MongoDB
        data = pd.DataFrame(get_data_from_adafruit("cambien2"))

        x = data['created_at']
        y1 = data['value']

        # Áp dụng style cyberpunk
        plt.style.use('cyberpunk')

        # Tạo figure cho biểu đồ
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, y1, marker='o')

        # Làm cho đường sáng lên
        mplcyberpunk.make_lines_glow()

        # Gán nhãn trục và chú thích
        ax.set_xlabel('Time')
        ax.set_ylabel('Humidity')
        ax.legend()

        # Tạo lớp nền với góc bo tròn có màu trùng với frame
        round_background = patches.FancyBboxPatch(
            (0, 0), 1, 1, boxstyle="round,pad=0.05", facecolor=self.bg_color, edgecolor="none",
            transform=ax.transAxes, zorder=-1)

        ax.add_patch(round_background)  # Thêm nền bo tròn

        # Chèn biểu đồ vào giao diện Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)


# Class định nghĩa ứng dụng chính
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter App with Background")
        self.geometry("600x400")

        # Tạo background giữa màn hình (frame ở giữa)
        self.bg_color = "#222831"  # Chọn màu nền bạn muốn
        self.background_frame = customtkinter.CTkFrame(self, width=400, height=300, corner_radius=15)
        self.background_frame.place(relx=0.5, rely=0.5, anchor="center")  # Đặt frame ở giữa màn hình

        # Thêm TabView vào background frame
        self.tab_view = MyTabView(master=self.background_frame)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)

        # Tạo công tắc (switch) và gán sự kiện vào background frame
        self.switch_var = customtkinter.StringVar(value="on")
        self.switch = customtkinter.CTkSwitch(self.background_frame, text="Relay Pump", command=self.switch_event,
                                              variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.grid(row=1, column=0, pady=20)

        # Tạo nút bấm và gán sự kiện vào background frame
        self.button = customtkinter.CTkButton(self.background_frame, text="Press Me", command=self.button_event)
        self.button.grid(row=2, column=0, pady=20)

    # Sự kiện khi công tắc thay đổi trạng thái
    def switch_event(self):
        if self.switch_var.get() == "off":
            print("Turn off relay")
        elif self.switch_var.get() == "on":
            print("Turn on relay")

    # Sự kiện khi nút bấm được nhấn
    def button_event(self):
        print("button pressed")


# Khởi tạo và chạy ứng dụng
if __name__ == "__main__":
    app = App()
    app.mainloop()
