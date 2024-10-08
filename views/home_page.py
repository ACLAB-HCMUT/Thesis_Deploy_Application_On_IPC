import ttkbootstrap as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

def display_home_content(content_frame):
    # Simulate sensor data
    temperature_data = [random.uniform(20, 35) for _ in range(10)]
    light_data = [random.uniform(100, 1000) for _ in range(10)]
    time_data = list(range(10))

    # Create a figure for the temperature chart
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
    
    # Plot temperature data
    ax1.plot(time_data, temperature_data, marker='o', linestyle='-', color='red')
    ax1.set_title("Temperature Sensor Data")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Temperature (°C)")

    # Plot light sensor data
    ax2.plot(time_data, light_data, marker='o', linestyle='-', color='blue')
    ax2.set_title("Light Sensor Data")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Light Intensity (Lux)")

    # Create a canvas to display the figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=content_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)
