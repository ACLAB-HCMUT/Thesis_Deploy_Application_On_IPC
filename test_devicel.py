import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
import requests
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

# Kiểm tra và thiết lập style cyberpunk
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
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Cấu hình biểu đồ 1
        self.figure1, self.ax1 = plt.subplots(figsize=(6, 6), dpi=100)
        self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self.scrollable_frame)
        self.canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Cấu hình biểu đồ 2
        self.figure2, self.ax2 = plt.subplots(figsize=(8, 8), dpi=100)
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


# Khởi tạo giao diện chính và khởi chạy ứng dụng
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Temperature Dashboard")

    # Tạo và đóng gói visualizer vào trong giao diện chính
    visualizer = TemperatureDataVisualizer(root)
    visualizer.pack(fill="both", expand=True, padx=20, pady=20)

    root.mainloop()
