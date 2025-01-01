import customtkinter as ctk
from PIL import Image
from datetime import datetime
import random  # Temporary, simulates sensor data; replace with actual sensor data source
import os
from constant import *

class NotificationView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        # Set up sidebar
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#2A8C55", width=170, height=600, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        # Logo
        self.logo_img_data = Image.open(os.path.join(base_path, "assets", "img", "logo.png"))
        self.logo_img = ctk.CTkImage(dark_image=self.logo_img_data, light_image=self.logo_img_data, size=(77.68, 85.42))
        self.logo = ctk.CTkLabel(master=self.sidebar_frame, text="", image=self.logo_img)
        self.logo.grid(row=0, column=0, pady=(38, 0), sticky="ew")

        # Dashboard button
        self.dashboard_img_data = Image.open(os.path.join(base_path, "assets", "img", "home_icon_transparent.png"))
        self.dashboard_img = ctk.CTkImage(dark_image=self.dashboard_img_data, light_image=self.dashboard_img_data)
        self.dashboard_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.dashboard_img, text="Dashboard", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.dashboard_btn.grid(row=1, column=0, padx=10, pady=(60, 0), sticky="ew")

        # Devices button
        self.devices_img_data = Image.open(os.path.join(base_path, "assets", "img", "devices_icon_transparent.png"))
        self.devices_img = ctk.CTkImage(dark_image=self.devices_img_data, light_image=self.devices_img_data)
        self.devices_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.devices_img, text="Devices", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.devices_btn.grid(row=2, column=0, padx=10, pady=(16, 0), sticky="ew")

        # Notification button
        self.notification_img_data = Image.open(os.path.join(base_path, "assets", "img", "notification_icon.png"))
        self.notification_img = ctk.CTkImage(dark_image=self.notification_img_data, light_image=self.notification_img_data)
        self.notification_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.notification_img, text="Notification", fg_color="#fff", font=("Arial Bold", 14), text_color="#2A8C55", hover_color="#eee", anchor="w")
        self.notification_btn.grid(row=3, column=0, padx=10, pady=(16, 0), sticky="ew")

        # Settings button
        self.settings_img_data = Image.open(os.path.join(base_path, "assets", "img", "settings_icon.png"))
        self.settings_img = ctk.CTkImage(dark_image=self.settings_img_data, light_image=self.settings_img_data)
        self.settings_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.settings_img, text="Settings", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.settings_btn.grid(row=4, column=0, padx=10, pady=(16, 0), sticky="ew")

        # Sign out button
        self.signout_btn = ctk.CTkButton(self.sidebar_frame, text="Sign Out", font=("Arial Bold", 14), fg_color="#fff", text_color="#2A8C55", hover_color="#eee")
        self.signout_btn.pack(side="bottom", padx=10, pady=(0, 10))

        # Set up main view
        self.main_view = ctk.CTkFrame(self, fg_color="#fff", width=640, height=600, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(fill="y", anchor="w", side="left")

        # Title frame
        self.title_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        self.orders_label = ctk.CTkLabel(self.title_frame, text="Notification", font=("Arial Black", 25), text_color="#2A8C55")
        self.orders_label.pack(anchor="nw", side="left")

        # Scrollable notifications container with scrollbar on the right
        self.scrollable_notifications = ctk.CTkScrollableFrame(self.main_view, fg_color="transparent", width=600, height=480)
        self.scrollable_notifications.pack(anchor="n", fill="both", expand=True, padx=27, pady=(20, 0))

        # Add example notifications with placeholder sensor data
        self.add_notification(
            icon_path=os.path.join(base_path, "assets", "img", "temperature_icon.png"),
            title="Canh bao nhiet do",
            message="Nhiet do vuot nguong {temperature} do C",
            icon_color="#FF4444",
            temperature=self.get_sensor_data("temperature")
        )

        self.add_notification(
            icon_path=os.path.join(base_path, "assets", "img", "humidity_icon.png"),
            title="Canh bao do am khong khi",
            message="Do am khong khi vuot nguong {humidity}%",
            icon_color="#2196F3",
            humidity=self.get_sensor_data("humidity")
        )

        self.add_notification(
            icon_path=os.path.join(base_path, "assets", "img", "pump_icon.png"),
            title="Canh bao may bom so 1 bat",
            message="Do am dat vuot nguong {soil_moisture}%, may bom so 1 bat",
            icon_color="#673AB7",
            soil_moisture=self.get_sensor_data("soil_moisture")
        )

        self.add_notification(
            icon_path=os.path.join(base_path, "assets", "img", "soil_icon.png"),
            title="Canh bao do am dat",
            message="Do am am trung binh ngay hom nay la {average_soil_moisture}%",
            icon_color="#795548",
            average_soil_moisture=self.get_sensor_data("average_soil_moisture")
        )

    def add_notification(self, icon_path, title, message, date=None, icon_color="#000000", **sensor_data):
        # Get the current date if no date is provided
        if date is None:
            date = datetime.now().strftime("%d/%m/%Y")  # Format as "DD/MM/YYYY"

        # Format the message with sensor data
        formatted_message = message.format(**sensor_data)

        # Container for each notification
        notification_container = ctk.CTkFrame(
            self.scrollable_notifications,
            fg_color="transparent",
            height=80,
        )
        notification_container.pack(fill="x", pady=(0, 10))
        notification_container.pack_propagate(False)

        # Icon
        try:
            icon_data = Image.open(icon_path)
            icon = ctk.CTkImage(dark_image=icon_data, light_image=icon_data, size=(24, 24))
            icon_label = ctk.CTkLabel(
                notification_container,
                text="",
                image=icon,
                fg_color=icon_color,
                width=30,
                height=30,
                corner_radius=15
            )
            icon_label.pack(side="left", padx=(10, 15))
        except:
            print(f"Could not load icon: {icon_path}")

        # Text content container
        text_container = ctk.CTkFrame(notification_container, fg_color="transparent")
        text_container.pack(side="left", fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(
            text_container,
            text=title,
            font=("Arial Bold", 14),
            text_color="#000000",
            anchor="w"
        )
        title_label.pack(anchor="w")

        # Message
        message_label = ctk.CTkLabel(
            text_container,
            text=formatted_message,
            font=("Arial", 12),
            text_color="#666666",
            anchor="w"
        )
        message_label.pack(anchor="w")

        # Date
        date_label = ctk.CTkLabel(
            notification_container,
            text=date,
            font=("Arial", 12),
            text_color="#666666"
        )
        date_label.pack(side="right", padx=10)

    def get_sensor_data(self, sensor_type):
        """Simulate fetching sensor data. Replace with actual sensor reading logic."""
        simulated_data = {
            "temperature": random.uniform(30, 40),
            "humidity": random.uniform(50, 70),
            "soil_moisture": random.uniform(45, 55),
            "average_soil_moisture": random.uniform(48, 52)
        }
        return round(simulated_data.get(sensor_type, 0), 2)