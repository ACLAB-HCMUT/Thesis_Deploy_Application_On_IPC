from tkinter import Frame, Label, Button
import customtkinter as ctk
from PIL import Image
import requests

class HomeView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        # Set up sidebar
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#2A8C55", width=170, height=600, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        self.logo_img_data = Image.open("assets/img/logo.png")
        self.logo_img = ctk.CTkImage(dark_image=self.logo_img_data, light_image=self.logo_img_data, size=(77.68, 85.42))
        self.logo = ctk.CTkLabel(master=self.sidebar_frame, text="", image=self.logo_img)
        self.logo.grid(row=0, column=0, pady=(38,0), sticky="ew")

        # Dashboard button
        self.dashboard_img_data = Image.open("assets/img/home_icon.png")
        self.dashboard_img = ctk.CTkImage(dark_image=self.dashboard_img_data, light_image=self.dashboard_img_data)
        self.dashboard_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.dashboard_img, text="Dashboard", fg_color="#fff", font=("Arial Bold", 14), text_color="#2A8C55", hover_color="#eee", anchor="w")
        self.dashboard_btn.grid(row=1, column=0, padx=10, pady=(60,0), sticky="ew")

        # Devices button
        self.devices_img_data = Image.open("assets/img/devices_icon_transparent.png")
        self.devices_img = ctk.CTkImage(dark_image=self.devices_img_data, light_image=self.devices_img_data)
        self.devices_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.devices_img, text="Devices", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.devices_btn.grid(row=2, column=0, padx=10, pady=(16,0), sticky="ew")
        
        # Notification button
        self.notification_img_data = Image.open("assets/img/notification_icon_transparent.png")
        self.notification_img = ctk.CTkImage(dark_image=self.notification_img_data, light_image=self.notification_img_data)
        self.notification_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.notification_img, text="Notification", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.notification_btn.grid(row=3, column=0, padx=10, pady=(16,0), sticky="ew")

        # Settings button
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
        self.main_view.pack(fill="y", anchor="w", side="right")

        # self.greeting = ctk.CTkLabel(self.main_view, text="")
        # self.greeting.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.title_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        self.orders_label = ctk.CTkLabel(self.title_frame, text="Dashboard", font=("Arial Black", 25), text_color="#2A8C55")
        self.orders_label.pack(anchor="nw", side="left")

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
        self.humidity_label.grid(row=0, column=1,sticky="sw", padx=(50,0))

        self.humidity_number = ctk.CTkLabel(self.humidity_metric, text="40%", font=("Arial Bold", 25), text_color="#3b516e", justify="left")
        self.humidity_number.grid(row=1, column=1, sticky="nw", padx=(50,0), pady=(0,10))

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