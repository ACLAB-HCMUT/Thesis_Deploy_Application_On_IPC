import customtkinter as ctk
from PIL import Image
import requests
import os
from constant import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import mplcyberpunk
import matplotlib.dates as mdates


class TemperatureDataVisualizer(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Biểu đồ Nhiệt độ
        self.figure1, self.ax1 = plt.subplots(figsize=(6, 4), dpi=100)
        self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self)
        self.canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Biểu đồ Độ ẩm
        self.figure2, self.ax2 = plt.subplots(figsize=(6, 4), dpi=100)
        self.canvas2 = FigureCanvasTkAgg(self.figure2, master=self)
        self.canvas2.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.fetch_and_plot_data()

    # Hàm lấy dữ liệu từ API và tính nhiệt độ trung bình hàng ngày
    def fetch_data(self):
        response = requests.get("https://do-an-ktmt-backend.onrender.com/api/data")
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = pd.DataFrame(response.json()["data"])  # Chuyển đổi dữ liệu thành DataFrame

        # Chuyển đổi timestamp thành kiểu datetime
        data['timestamp'] = pd.to_datetime(data['timestamp'], format='%a, %d %b %Y %H:%M:%S %Z')

        # Tạo cột ngày từ timestamp
        data['date'] = data['timestamp'].dt.date

        # Tính toán nhiệt độ trung bình theo ngày
        daily_avg_temp = data.groupby('date')['temperature'].mean().reset_index()

        # Tính toán độ ẩm trung bình theo ngày
        daily_avg_humidity = data.groupby('date')['humidity'].mean().reset_index()

        # Trả về hai bảng dữ liệu (temperature và humidity) để sử dụng cho biểu đồ
        return daily_avg_temp, daily_avg_humidity

    # Hàm vẽ và cập nhật biểu đồ với các chấm và chú thích cho từng ngày
    def plot_temperature(self, daily_avg_temp, daily_avg_humidity):
        self.ax1.clear()
        self.ax2.clear()

        # Biểu đồ 1: Nhiệt độ
        self.ax1.plot(daily_avg_temp['date'], daily_avg_temp['temperature'], color='cyan', marker='o', linestyle='-', markersize=8)
        self.ax1.set_title('Temperature')
        self.ax1.set_xlabel('Date')
        self.ax1.set_ylabel('Average Temperature')
        self.ax1.set_ylim(0, 100)
        self.ax1.set_yticks(range(0, 101, 20))
        self.ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
        self.figure1.autofmt_xdate(rotation=45)

        # Biểu đồ 2: Độ ẩm
        self.ax2.plot(daily_avg_humidity['date'], daily_avg_humidity['humidity'], color='magenta', marker='s', linestyle='-', markersize=8)
        self.ax2.set_title('Humidity')
        self.ax2.set_xlabel('Date')
        self.ax2.set_ylabel('Average Humidity')
        self.ax2.set_ylim(0, 100)
        self.ax2.set_yticks(range(0, 101, 20))
        self.ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
        self.figure2.autofmt_xdate(rotation=45)

        # Hiển thị nhãn trên biểu đồ
        for ax in [self.ax1, self.ax2]:
            for x, y in zip(daily_avg_temp['date'], daily_avg_temp['temperature']):
                ax.annotate(f"{y:.1f}°C", 
                            (x, y), 
                            textcoords="offset points", 
                            xytext=(0, 10), 
                            ha='center', 
                            color="yellow", 
                            fontsize=8, 
                            bbox=dict(facecolor="black", edgecolor="yellow", boxstyle="round,pad=0.3"))
        
        # Thêm hiệu ứng phát sáng
        mplcyberpunk.add_glow_effects(self.ax1)
        mplcyberpunk.add_glow_effects(self.ax2)

        self.canvas1.draw()
        self.canvas2.draw()

    # Hàm lấy dữ liệu và cập nhật biểu đồ sau mỗi 10 giây
    def fetch_and_plot_data(self):
        # Lấy dữ liệu từ API (bao gồm nhiệt độ và độ ẩm)
        daily_avg_temp, daily_avg_humidity = self.fetch_data()

        # Vẽ biểu đồ nhiệt độ
        self.plot_temperature(daily_avg_temp, daily_avg_humidity)

        # Lên lịch cập nhật lại dữ liệu sau 1 ngày (86400 giây)
        self.after(86400, self.fetch_and_plot_data)

from CTkTable import CTkTable
import requests

class HomeView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_view = ctk.CTkFrame(self)
        self.main_view.grid_rowconfigure(0, weight=1)
        self.main_view.grid_rowconfigure(1, weight=2)
        self.main_view.grid_columnconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)

        # Set up sidebar
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#2A8C55", width=170, height=600, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        self.logo_img_data = Image.open(os.path.join(base_path, "assets", "img", "logo.png"))
        self.logo_img_data = Image.open("assets/img/logo.png")
        self.logo_img = ctk.CTkImage(dark_image=self.logo_img_data, light_image=self.logo_img_data, size=(77.68, 85.42))
        self.logo = ctk.CTkLabel(master=self.sidebar_frame, text="", image=self.logo_img)
        self.logo.grid(row=0, column=0, pady=(38,0), sticky="ew")

        # Dashboard button
        self.dashboard_img_data = Image.open(os.path.join(base_path, "assets", "img", "home_icon.png"))
        self.dashboard_img_data = Image.open("assets/img/home_icon.png")
        self.dashboard_img = ctk.CTkImage(dark_image=self.dashboard_img_data, light_image=self.dashboard_img_data)
        self.dashboard_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.dashboard_img, text="Dashboard", fg_color="#fff", font=("Arial Bold", 14), text_color="#2A8C55", hover_color="#eee", anchor="w")
        self.dashboard_btn.grid(row=1, column=0, padx=10, pady=(60,0), sticky="ew")

        # Devices button
        self.devices_img_data = Image.open(os.path.join(base_path, "assets", "img", "devices_icon_transparent.png"))
        self.devices_img_data = Image.open("assets/img/devices_icon_transparent.png")
        self.devices_img = ctk.CTkImage(dark_image=self.devices_img_data, light_image=self.devices_img_data)
        self.devices_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.devices_img, text="Devices", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.devices_btn.grid(row=2, column=0, padx=10, pady=(16,0), sticky="ew")
        
        # Notification button
        self.notification_img_data = Image.open(os.path.join(base_path, "assets", "img", "notification_icon_transparent.png"))
        self.notification_img_data = Image.open("assets/img/notification_icon_transparent.png")
        self.notification_img = ctk.CTkImage(dark_image=self.notification_img_data, light_image=self.notification_img_data)
        self.notification_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.notification_img, text="Notification", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.notification_btn.grid(row=3, column=0, padx=10, pady=(16,0), sticky="ew")

        # Settings button
        self.settings_img_data = Image.open(os.path.join(base_path, "assets", "img", "settings_icon.png"))
        self.settings_img_data = Image.open("assets/img/settings_icon.png")
        self.settings_img = ctk.CTkImage(dark_image=self.settings_img_data, light_image=self.settings_img_data)
        self.settings_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.settings_img, text="Settings", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.settings_btn.grid(row=4, column=0, padx=10, pady=(16,0), sticky="ew")

        # Sign out button
        self.signout_btn = ctk.CTkButton(self.sidebar_frame, text="Sign Out", font=("Arial Bold", 14), fg_color="#fff", text_color="#2A8C55", hover_color="#eee")
        self.signout_btn.pack(side="bottom", padx=10, pady=(0,10))

        # Set up main view
        self.main_view = ctk.CTkFrame(self, fg_color="#fff", width=640, height=600, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(fill="y", anchor="w", side="left")

        # self.greeting = ctk.CTkLabel(self.main_view, text="")
        # self.greeting.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.title_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=27, pady=(29, 0))
        self.title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        self.orders_label = ctk.CTkLabel(self.title_frame, text="Dashboard", font=("Arial Black", 25), text_color="#2A8C55")
        self.orders_label.pack(anchor="nw", side="left")
        # Khung chứa Temperature và Humidity
        self.metrics_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.metrics_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=27, pady=(36, 0))
        self.metrics_frame.grid_columnconfigure((0, 1, 2), weight=1)  # Đảm bảo ba cột được phân bổ đều

        # Temperature nằm ở column=0
        self.temperature_metric = ctk.CTkFrame(self.metrics_frame, fg_color="#d6fdd9", width=250, height=70)
        self.temperature_metric.grid_propagate(0)
        self.temperature_metric.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.temperature_img_data = Image.open(os.path.join(base_path, "assets", "img", "temperature_icon.png"))
        # self.new_orders = ctk.CTkButton(self.title_frame, text="+ New Order", font=("Arial Black", 15), text_color="#fff", fg_color="#2A8C55", hover_color="#207244")
        # self.new_orders.pack(anchor="ne", side="right")

        self.metrics_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.metrics_frame.pack(anchor="n",fill="x", padx=27, pady=(36, 0))

        # Temperature

        self.temperature_metric = ctk.CTkFrame(self.metrics_frame, fg_color="#d6fdd9", width=270, height=70)
        self.temperature_metric.grid_propagate(0)
        self.temperature_metric.pack(side="left", expand=True, anchor="center")

        self.temperature_img_data = Image.open("assets/img/temperature_icon.png")
        self.temperature_img = ctk.CTkImage(dark_image=self.temperature_img_data, light_image=self.temperature_img_data, size=(43, 43))

        self.temperature_img_label = ctk.CTkLabel(self.temperature_metric, image=self.temperature_img, text="")
        self.temperature_img_label.grid(row=0, column=0, rowspan=2, padx=(30, 5), pady=10)

        self.temperature_label = ctk.CTkLabel(self.temperature_metric, text="Temperature", font=("Arial", 16), text_color="#3b516e")
        self.temperature_label.grid(row=0, column=1, sticky="sw", padx=(50, 0))

        self.temperature_number = ctk.CTkLabel(self.temperature_metric, text="Loading...", font=("Arial Bold", 25), text_color="#3b516e", justify="left")
        self.temperature_number.grid(row=1, column=1, sticky="nw", padx=(50, 0), pady=(0, 10))

        # Humidity nằm ở column=2
        self.humidity_metric = ctk.CTkFrame(self.metrics_frame, fg_color="#d6f0fd", width=250, height=70)
        self.humidity_metric.grid_propagate(0)
        self.humidity_metric.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        self.humidity_img_data = Image.open(os.path.join(base_path, "assets", "img", "humidity_icon.png"))
        self.temperature_label.grid(row=0, column=1,sticky="sw", padx=(50,0))

        self.temperature_number = ctk.CTkLabel(self.temperature_metric, text="Loading...", font=("Arial Bold", 25), text_color="#3b516e", justify="left")
        self.temperature_number.grid(row=1, column=1, sticky="nw", padx=(50,0), pady=(0,10))

        # Humidity

        self.humidity_metric = ctk.CTkFrame(self.metrics_frame, fg_color="#d6f0fd", width=270, height=70)
        self.humidity_metric.grid_propagate(0)
        self.humidity_metric.pack(side="right", expand=True, anchor="center")

        self.humidity_img_data = Image.open("assets/img/humidity_icon.png")
        self.humidity_img = ctk.CTkImage(dark_image=self.humidity_img_data, light_image=self.humidity_img_data, size=(43, 43))

        self.humidity_img_label = ctk.CTkLabel(self.humidity_metric, image=self.humidity_img, text="")
        self.humidity_img_label.grid(row=0, column=0, rowspan=2, padx=(30, 5), pady=10)

        self.humidity_label = ctk.CTkLabel(self.humidity_metric, text="Humidity", font=("Arial", 16), text_color="#3b516e")
        self.humidity_label.grid(row=0, column=1, sticky="sw", padx=(50, 0))

        self.humidity_number = ctk.CTkLabel(self.humidity_metric, text="40%", font=("Arial Bold", 25), text_color="#3b516e", justify="left")
        self.humidity_number.grid(row=1, column=1, sticky="nw", padx=(50, 0), pady=(0, 10))

        # Biểu đồ 1 ở bên dưới, ở column=0
        self.chart_frame_1 = TemperatureDataVisualizer(self.main_view)
        self.chart_frame_1.grid(row=2, column=1, sticky="nsew", padx=10, pady=5)
        self.humidity_label.grid(row=0, column=1,sticky="sw", padx=(50,0))

        self.humidity_number = ctk.CTkLabel(self.humidity_metric, text="40%", font=("Arial Bold", 25), text_color="#3b516e", justify="left")
        self.humidity_number.grid(row=1, column=1, sticky="nw", padx=(50,0), pady=(0,10))

        table_data = [
            ["Relay ID", "Relay Name", "Status", "Time"],
            ['1', 'Máy bơm 1', 'On', '12:00 1/11/2024'],
            ['2', 'Máy bơm 2', 'Off', '12:00 1/11/2024'],
            ['3', 'Máy bơm 3', 'On', '12:00 1/11/2024'],
            ['4', 'Máy bơm 4', 'Off', '12:00 1/11/2024'],
            ['1', 'Máy bơm 1', 'Off', '12:00 1/11/2024'],
            ['2', 'Máy bơm 2', 'On', '12:00 1/11/2024'],
            ['3', 'Máy bơm 3', 'Off', '12:00 1/11/2024'],
            ['4', 'Máy bơm 4', 'On', '12:00 1/11/2024'],
            ['3', 'Máy bơm 3', 'On', '12:00 1/11/2024'],
            ['4', 'Máy bơm 4', 'Off', '12:00 1/11/2024']
        ]

        self.table_frame = ctk.CTkScrollableFrame(self.main_view, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=27, pady=21)
        self.table = CTkTable(self.table_frame, values=table_data, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4")
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        self.table.pack(expand=True)

        # Fetch temperature
        self.fetch_sensor_data()

    def fetch_sensor_data(self):
        try:
            response = requests.get("https://do-an-ktmt-backend.onrender.com/api/data/sensors/latest").json()
            data = response["data"]

            # Get the latest record
            latest_temperature = data["temperature"]
            latest_humidity = data["humidity"]
            
            # Update the label with the latest value
            self.temperature_number.configure(text=f"{latest_temperature}°C")
            self.humidity_number.configure(text=f"{latest_humidity}%")
        
        except requests.RequestException:
            self.temperature_number.configure(text="Error fetching data")
            self.humidity_number.configure(text="Error fetching data")
        except KeyError:
            self.temperature_number.configure(text="Invalid data format")
            self.humidity_number.configure(text="Invalid data format")
        
        # Schedule the next data fetch in 10 seconds
        self.after(10000, self.fetch_sensor_data)