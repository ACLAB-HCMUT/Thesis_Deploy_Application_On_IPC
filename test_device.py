import customtkinter as ctk
from PIL import Image
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import mplcyberpunk
from constant import *

class TemperatureDataVisualizer(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure_grid()

        # Biểu đồ Nhiệt độ
        self.figure1, self.ax1 = plt.subplots()
        self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self)
        self.canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Biểu đồ Độ ẩm
        self.figure2, self.ax2 = plt.subplots()
        self.canvas2 = FigureCanvasTkAgg(self.figure2, master=self)
        self.canvas2.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.fetch_and_plot_data()

    def configure_grid(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

    def fetch_data(self):
        response = requests.get("https://do-an-ktmt-backend.onrender.com/api/data")
        response.raise_for_status()
        data = pd.DataFrame(response.json()["data"])
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data['date'] = data['timestamp'].dt.date

        daily_avg_temp = data.groupby('date')['temperature'].mean().reset_index()
        daily_avg_humidity = data.groupby('date')['humidity'].mean().reset_index()

        return daily_avg_temp, daily_avg_humidity

    def plot_temperature(self, daily_avg_temp, daily_avg_humidity):
        self.ax1.clear()
        self.ax2.clear()

        # Biểu đồ Nhiệt độ
        self.ax1.plot(daily_avg_temp['date'], daily_avg_temp['temperature'], color='cyan', marker='o', linestyle='-')
        self.ax1.set(title='Temperature', xlabel='Date', ylabel='Avg Temperature (°C)', ylim=(0, 100))
        self.ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
        self.figure1.autofmt_xdate(rotation=45)

        # Biểu đồ Độ ẩm
        self.ax2.plot(daily_avg_humidity['date'], daily_avg_humidity['humidity'], color='magenta', marker='s', linestyle='-')
        self.ax2.set(title='Humidity', xlabel='Date', ylabel='Avg Humidity (%)', ylim=(0, 100))
        self.ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
        self.figure2.autofmt_xdate(rotation=45)

        mplcyberpunk.add_glow_effects(self.ax1)
        mplcyberpunk.add_glow_effects(self.ax2)

        self.canvas1.draw()
        self.canvas2.draw()

    def fetch_and_plot_data(self):
        daily_avg_temp, daily_avg_humidity = self.fetch_data()
        self.plot_temperature(daily_avg_temp, daily_avg_humidity)
        self.after(86400, self.fetch_and_plot_data)  # Cập nhật mỗi ngày

class HomeView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = self.create_sidebar()
        self.main_view = self.create_main_view()

    def create_sidebar(self):
        sidebar_frame = ctk.CTkFrame(self, fg_color="#2A8C55", width=170, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, sticky="ns")

        # Logo
        logo_img = ctk.CTkImage(dark_image=Image.open(os.path.join("assets", "img", "logo.png")), size=(78, 85))
        ctk.CTkLabel(sidebar_frame, text="", image=logo_img).pack(pady=(38, 0))

        # Các nút trong sidebar
        buttons_info = [
            ("Dashboard", "home_icon.png", "#2A8C55"),
            ("Devices", "devices_icon_transparent.png", "#207244"),
            ("Notification", "notification_icon_transparent.png", "#207244"),
            ("Settings", "settings_icon.png", "#207244")
        ]
        for text, img_name, hover_color in buttons_info:
            img = ctk.CTkImage(dark_image=Image.open(os.path.join("assets", "img", img_name)))
            ctk.CTkButton(sidebar_frame, image=img, text=text, fg_color="transparent", font=("Arial Bold", 14), hover_color=hover_color, anchor="w").pack(pady=16, fill="x")

        # Nút Sign out
        ctk.CTkButton(sidebar_frame, text="Sign Out", font=("Arial Bold", 14), fg_color="#fff", text_color="#2A8C55", hover_color="#eee").pack(side="bottom", padx=10, pady=(0, 10))
        return sidebar_frame

    def create_main_view(self):
        main_view = ctk.CTkFrame(self, fg_color="#fff", corner_radius=0)
        main_view.grid(row=0, column=1, sticky="nsew")
        main_view.grid_rowconfigure(1, weight=1)
        main_view.grid_columnconfigure(0, weight=1)

        self.create_metrics_frame(main_view)

        self.create_dashboard_title(main_view)

        # Khung biểu đồ
        chart_frame = TemperatureDataVisualizer(main_view)
        chart_frame.grid(row=1, column=0, sticky="nsew", padx=27, pady=20)

        return main_view

    def create_dashboard_title(self, parent):
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=27, pady=(29, 0))
        ctk.CTkLabel(title_frame, text="Dashboard", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw")

    def create_metrics_frame(self, parent):
        metrics_frame = ctk.CTkFrame(parent, fg_color="transparent")
        metrics_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=27, pady=(36, 0))
        metrics_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Temperature Metric
        self.create_metric(metrics_frame, 0, "Temperature", "#d6fdd9", "temperature_icon.png", "Loading...", "#3b516e")

        # Humidity Metric
        self.create_metric(metrics_frame, 2, "Humidity", "#d6f0fd", "humidity_icon.png", "40%", "#3b516e")

    def create_metric(self, parent, column, label, bg_color, icon_path, value_text, text_color):
        metric_frame = ctk.CTkFrame(parent, fg_color=bg_color, width=250, height=70)
        metric_frame.grid_propagate(0)
        metric_frame.grid(row=0, column=column, sticky="nsew", padx=(0, 10) if column == 0 else (10, 0))

        icon_img = ctk.CTkImage(dark_image=Image.open(os.path.join(base_path, "assets", "img", icon_path)), size=(43, 43))
        ctk.CTkLabel(metric_frame, image=icon_img, text="").grid(row=0, column=0, rowspan=2, padx=(30, 5), pady=10)

        ctk.CTkLabel(metric_frame, text=label, font=("Arial", 16), text_color=text_color).grid(row=0, column=1, sticky="sw", padx=(50, 0))
        ctk.CTkLabel(metric_frame, text=value_text, font=("Arial Bold", 25), text_color=text_color).grid(row=1, column=1, sticky="nw", padx=(50, 0), pady=(0, 10))

app = ctk.CTk()
app.title("Dashboard")
HomeView(app).pack(fill="both", expand=True)
app.mainloop()
