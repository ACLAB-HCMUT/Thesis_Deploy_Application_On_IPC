import customtkinter as ctk
from PIL import Image
from CTkTable import CTkTable
from datetime import datetime
import os
from constant import *

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
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
         # Main container frame
        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        # Scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="white",
            corner_radius=0,
            scrollbar_fg_color="#E5E5E5",
            scrollbar_button_color="#999999",
            scrollbar_button_hover_color="#666666"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Title frame
        self.title_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.title_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        # Add leaf icon
        self.leaf_icon = Image.open(os.path.join(base_path, "assets", "img", "calendar_icon.png"))
        self.leaf_image = ctk.CTkImage(light_image=self.leaf_icon, dark_image=self.leaf_icon, size=(24, 24))
        self.leaf_label = ctk.CTkLabel(self.title_frame, image=self.leaf_image, text="")
        self.leaf_label.pack(side="left", padx=(0, 10))
        
        # Title text
        self.title_label = ctk.CTkLabel(
            self.title_frame, 
            text="Cai dat canh bao",
            font=("Arial Bold", 20),
            text_color="#2A8C55"
        )
        self.title_label.pack(side="left")
        # Sign out button
        self.signout_btn = ctk.CTkButton(self.sidebar_frame, text="Sign Out", font=("Arial Bold", 14), fg_color="#fff", text_color="#2A8C55", hover_color="#eee")
        self.signout_btn.pack(side="bottom", padx=10, pady=(0, 10))
        # Save button
        self.save_button = ctk.CTkButton(
            self.title_frame,
            text="Luu",
            font=("Arial Bold", 12),
            fg_color="#FF0000",
            hover_color="#CC0000",
            height=32,
            width=60,
            corner_radius=4
        )
        self.save_button.pack(side="right")
        
        # Create grid frame for 2x2 layout
        self.grid_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.grid_frame.pack(fill="x", padx=20, pady=5)
        
        # Create left and right columns
        self.left_column = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
        self.left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.right_column = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
        self.right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Create sections
        self._create_temperature_section()
        self._create_humidity_section()
        self._create_soil_temp_section()
        self._create_soil_humidity_section()
        self._create_switch_section()
        self._create_data_table()
        
    def _create_section_frame(self, parent, title):
        """Create a bordered section frame with title"""
        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            border_width=1,
            border_color="#E5E5E5",
            corner_radius=6
        )
        frame.pack(fill="x", pady=5)
        
        # Title
        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial Bold", 13),
            text_color="black",
            anchor="w"
        )
        title_label.pack(fill="x", padx=15, pady=(10, 5))
        
        return frame
        
    def _create_input_row(self, parent, label_text):
        """Create a row with label and entry"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=5)
        
        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=("Arial", 12),
            text_color="black",
            anchor="w"
        )
        label.pack(side="left")
        
        entry = ctk.CTkEntry(
            frame,
            height=30,
            width=150,
            border_color="#E5E5E5",
            fg_color="white"
        )
        entry.pack(side="right")
        
        return entry

    def _create_temperature_section(self):
        frame = self._create_section_frame(self.left_column, "Nhiet do khong khi")
        self.temp_upper = self._create_input_row(frame, "Nhiet do vuot nguong:")
        self.temp_lower = self._create_input_row(frame, "Nhiet do duoi nguong:")
        
    def _create_humidity_section(self):
        frame = self._create_section_frame(self.right_column, "Do am khong khi")
        self.humid_upper = self._create_input_row(frame, "Do am vuot nguong:")
        self.humid_lower = self._create_input_row(frame, "Do am duoi nguong:")
        
    def _create_soil_temp_section(self):
        frame = self._create_section_frame(self.left_column, "Nhiet do dat")
        self.soil_temp_upper = self._create_input_row(frame, "Nhiet do vuot nguong:")
        self.soil_temp_lower = self._create_input_row(frame, "Nhiet do duoi nguong:")
        
    def _create_soil_humidity_section(self):
        frame = self._create_section_frame(self.right_column, "Do am dat")
        self.soil_humid_upper = self._create_input_row(frame, "Do am vuot nguong:")
        self.soil_humid_lower = self._create_input_row(frame, "Do am duoi nguong:")
        
    def _create_switch_section(self):
        # Switch section container
        switch_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        switch_container.pack(fill="x", padx=20, pady=5)
        
        frame = self._create_section_frame(switch_container, "Cong tac")
        
        # Switch number
        switch_frame = ctk.CTkFrame(frame, fg_color="transparent")
        switch_frame.pack(fill="x", padx=15, pady=5)
        
        switch_label = ctk.CTkLabel(
            switch_frame,
            text="Cong tac so:",
            font=("Arial", 12),
            text_color="black"
        )
        switch_label.pack(side="left")
        
        switch_entry = ctk.CTkEntry(
            switch_frame,
            height=30,
            width=150,
            border_color="#E5E5E5",
            fg_color="white"
        )
        switch_entry.pack(side="left", padx=(10, 0))
        
        # Time selection frame
        time_frame = ctk.CTkFrame(frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=15, pady=(5, 10))
        
        # Start time
        start_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        start_frame.pack(side="left")
        
        start_label = ctk.CTkLabel(
            start_frame,
            text="Thoi gian bat dau",
            font=("Arial", 12),
            text_color="black"
        )
        start_label.pack(side="left")
        
        calendar_icon = Image.open(os.path.join(base_path, "assets", "img", "calendar_icon.png"))
        calendar_image = ctk.CTkImage(light_image=calendar_icon, dark_image=calendar_icon, size=(20, 20))
        
        start_calendar = ctk.CTkButton(
            start_frame,
            text="",
            image=calendar_image,
            fg_color="transparent",
            width=30,
            height=30,
            hover_color="#E5E5E5"
        )
        start_calendar.pack(side="left", padx=(10, 30))
        
        # End time
        end_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        end_frame.pack(side="left")
        
        end_label = ctk.CTkLabel(
            end_frame,
            text="Thoi gian ket thuc",
            font=("Arial", 12),
            text_color="black"
        )
        end_label.pack(side="left")
        
        end_calendar = ctk.CTkButton(
            end_frame,
            text="",
            image=calendar_image,
            fg_color="transparent",
            width=30,
            height=30,
            hover_color="#E5E5E5"
        )
        end_calendar.pack(side="left", padx=10)
        
    def _create_data_table(self):
        # Table data
        data = [
            ["Thiet bi", "Gia tri", "Gia tri", "Trang thai"],
            ["Nhiet do khong khi", "37 độ C", "15 độ C", "✓"],
            ["Do am khong khi", "70%", "0%", "✓"],
            ["Nhiet do dat", "37 độ C", "15 độ C", "✓"],
            ["Do am dat", "70%", "0%", "✓"],
            ["Cong tac 1", "20/11/2024 11:20:20", "20/11/2024 11:20:20", "✓"]
        ]
        
        # Table container
        table_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        table_frame.pack(fill="x", padx=20, pady=10)
        
        # Create table
        self.table = CTkTable(
            master=table_frame,
            values=data,
            colors=["#F5F5F5", "#FFFFFF"],
            header_color="#2A8C55",
            hover_color="#E5E5E5",
            border_width=1,
            border_color="#E5E5E5",
            pady=5,
            padx=10
        )
        self.table.pack(fill="x")
        
        # Style header row
        self.table.edit_row(0, text_color="white", hover_color="#2A8C55")
        
        # Add checkmarks in status column
        
def create_settings_window():
    window = ctk.CTk()
    window.title("Settings")
    window.geometry("800x600")
    
    # Create and pack the settings view
    settings_view = SettingsView(window)
    settings_view.pack(fill="both", expand=True)
    
    return window

