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


try:
    plt.style.use('cyberpunk')
except ImportError:
    print("mplcyberpunk chưa được cài đặt. Vui lòng chạy `pip install mplcyberpunk`.")

# Class TemperatureDataVisualizer
class TemperatureDataVisualizer(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Tạo một khung cuộn
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Cấu hình biểu đồ 1
        self.figure1, self.ax1 = plt.subplots(figsize=(4.7, 4.7), dpi=100)
        self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self.scrollable_frame)
        self.canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Cấu hình biểu đồ 2
        self.figure2, self.ax2 = plt.subplots(figsize=(4.7, 4.7), dpi=100)
        self.canvas2 = FigureCanvasTkAgg(self.figure2, master=self.scrollable_frame)
        self.canvas2.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Khởi tạo lần đầu và thiết lập cập nhật tự động
        self.fetch_and_plot_data()

    def fetch_data(self):
        # Gửi yêu cầu GET đến API
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

    def plot_temperature(self, daily_avg_temp, daily_avg_humidity):
        self.ax1.clear()
        self.ax2.clear()

        # Biểu đồ 1: Nhiệt độ
        self.ax1.plot(daily_avg_temp['date'], daily_avg_temp['temperature'], color='cyan', marker='o', linestyle='-', markersize=8)
        self.ax1.set_title('Daily Average Temperature Over Time (Chart 1)')
        self.ax1.set_xlabel('Date')
        self.ax1.set_ylabel('Average Temperature')
        self.ax1.set_ylim(0, 100)
        self.ax1.set_yticks(range(0, 101, 20))
        self.ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.figure1.autofmt_xdate(rotation=45)

        # Biểu đồ 2: Độ ẩm
        self.ax2.plot(daily_avg_humidity['date'], daily_avg_humidity['humidity'], color='magenta', marker='s', linestyle='-', markersize=8)
        self.ax2.set_title('Daily Average Humidity Over Time (Chart 2)')
        self.ax2.set_xlabel('Date')
        self.ax2.set_ylabel('Average Humidity')
        self.ax2.set_ylim(0, 100)
        self.ax2.set_yticks(range(0, 101, 20))
        self.ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
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

    def fetch_and_plot_data(self):
        # Lấy dữ liệu từ API (bao gồm nhiệt độ và độ ẩm)
        daily_avg_temp, daily_avg_humidity = self.fetch_data()

        # Vẽ biểu đồ nhiệt độ
        self.plot_temperature(daily_avg_temp, daily_avg_humidity)

        # Lên lịch cập nhật lại dữ liệu sau 1 ngày (86400 giây)
        self.after(86400, self.fetch_and_plot_data)


class HomeView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.main_view = ctk.CTkFrame(self)
        self.grid_rowconfigure(0, weight=1)
        # self.main_view.grid_rowconfigure(1, weight=2)
        # self.main_view.grid_columnconfigure(1, weight=1)


        # Set up sidebar
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#2A8C55", width=170, height=600, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        self.logo_img_data = Image.open(os.path.join(base_path, "assets", "img", "logo.png"))
        self.logo_img = ctk.CTkImage(dark_image=self.logo_img_data, light_image=self.logo_img_data, size=(77.68, 85.42))
        self.logo = ctk.CTkLabel(master=self.sidebar_frame, text="", image=self.logo_img)
        self.logo.grid(row=0, column=0, pady=(38,0), sticky="ew")

        # Dashboard button
        self.dashboard_img_data = Image.open(os.path.join(base_path, "assets", "img", "home_icon.png"))
        self.dashboard_img = ctk.CTkImage(dark_image=self.dashboard_img_data, light_image=self.dashboard_img_data)
        self.dashboard_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.dashboard_img, text="Dashboard", fg_color="#fff", font=("Arial Bold", 14), text_color="#2A8C55", hover_color="#eee", anchor="w")
        self.dashboard_btn.grid(row=1, column=0, padx=10, pady=(60,0), sticky="ew")

        # Devices button
        self.devices_img_data = Image.open(os.path.join(base_path, "assets", "img", "devices_icon_transparent.png"))
        self.devices_img = ctk.CTkImage(dark_image=self.devices_img_data, light_image=self.devices_img_data)
        self.devices_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.devices_img, text="Devices", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.devices_btn.grid(row=2, column=0, padx=10, pady=(16,0), sticky="ew")
        
        # Notification button
        self.notification_img_data = Image.open(os.path.join(base_path, "assets", "img", "notification_icon_transparent.png"))
        self.notification_img = ctk.CTkImage(dark_image=self.notification_img_data, light_image=self.notification_img_data)
        self.notification_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.notification_img, text="Notification", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.notification_btn.grid(row=3, column=0, padx=10, pady=(16,0), sticky="ew")

        # Settings button
        self.settings_img_data = Image.open(os.path.join(base_path, "assets", "img", "settings_icon.png"))
        self.settings_img = ctk.CTkImage(dark_image=self.settings_img_data, light_image=self.settings_img_data)
        self.settings_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.settings_img, text="Settings", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.settings_btn.grid(row=4, column=0, padx=10, pady=(16,0), sticky="ew")

        # Sign out button
        self.signout_btn = ctk.CTkButton(self.sidebar_frame, text="Sign Out", font=("Arial Bold", 14), fg_color="#fff", text_color="#2A8C55", hover_color="#eee")
        self.signout_btn.pack(side="bottom", padx=10, pady=(0,10))

        # Set up main view
        self.main_view = ctk.CTkFrame(self, fg_color="#fff", width=1000, height=600, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(fill="both", expand=True, anchor="w", side="left")

        # self.greeting = ctk.CTkLabel(self.main_view, text="")
        # self.greeting.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.title_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        self.orders_label = ctk.CTkLabel(self.title_frame, text="Dashboard", font=("Arial Black", 25), text_color="#2A8C55")
        self.orders_label.pack(anchor="nw", side="left")

        # Khung chứa Temperature và Humidity
        self.metrics_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.metrics_frame.pack(fill="both", padx=27, pady=(36, 0))

        
        self.temperature_metric = ctk.CTkFrame(self.metrics_frame, fg_color="#d6fdd9", width=300, height=70)
        self.temperature_metric.pack(side="left", padx=(0, 10))

        # Tải ảnh và tạo image
        self.temperature_img_data = Image.open(os.path.join(base_path, "assets", "img", "temperature_icon.png"))
        self.temperature_img = ctk.CTkImage(dark_image=self.temperature_img_data, light_image=self.temperature_img_data, size=(43, 43))

        # Label cho hình ảnh
        self.temperature_img_label = ctk.CTkLabel(self.temperature_metric, image=self.temperature_img, text="")
        self.temperature_img_label.pack(side="left", padx=(30, 5), pady=10)

        # Label cho tên "Temperature"
        self.temperature_label = ctk.CTkLabel(self.temperature_metric, text="Temperature", font=("Arial", 16), text_color="#3b516e")
        self.temperature_label.pack(side="top", padx=(30, 30))  # Chuyển side thành "top"

        self.temperature_number = ctk.CTkLabel(self.temperature_metric, text="Loading...", font=("Arial Bold", 25), text_color="#3b516e", justify="left")
        self.temperature_number.pack(side="top", padx=(30, 30), pady=(0, 10))  # Chuyển side thành "top"  # Đảm bảo ba cột được phân bổ đều


        #/////////////////////////////////////////


        self.humidity_metric = ctk.CTkFrame(self.metrics_frame, fg_color="#d6f0fd", width=300, height=70)
        self.humidity_metric.pack(side="left", padx=(0, 10))

        # Tải ảnh và tạo image
        self.humidity_img_data = Image.open(os.path.join(base_path, "assets", "img", "humidity_icon.png"))
        self.humidity_img = ctk.CTkImage(dark_image=self.humidity_img_data, light_image=self.humidity_img_data, size=(43, 43))

        # Label cho hình ảnh
        self.humidity_img_label = ctk.CTkLabel(self.humidity_metric, image=self.humidity_img, text="")
        self.humidity_img_label.pack(side="left", padx=(30, 5), pady=10)

        # Label cho tên "humidity"
        self.humidity_label = ctk.CTkLabel(self.humidity_metric, text="humidity", font=("Arial", 16), text_color="#3b516e")
        self.humidity_label.pack(side="top", padx=(30, 30))  # Chuyển side thành "top"

        self.humidity_number = ctk.CTkLabel(self.humidity_metric, text="Loading...", font=("Arial Bold", 25), text_color="#3b516e", justify="left")
        self.humidity_number.pack(side="top", padx=(30, 30), pady=(0, 10))  # Chuyển side thành "top"  # Đảm bảo ba cột được phân bổ đều

        # Biểu đồ 1 ở bên dưới, ở column=0
        self.chart_frame_1 = TemperatureDataVisualizer(self.main_view)
        self.chart_frame_1.pack(expand=True, fill="both", padx=10, pady=10)

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