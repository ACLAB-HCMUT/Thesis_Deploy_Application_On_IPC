import customtkinter as ctk
from PIL import Image
import requests
import os
from constant import *
from CTkTable import CTkTable
from utils.constant import *
class DevicesView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.switches = []
        self.relay_frames = []
        self.relay_img_labels = []
        self.relay_labels = []
        self.max_col = 3
        self.num_switches = 0

        # Set up sidebar
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#2A8C55",  width=170, height=600, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        self.logo_img_data = Image.open(os.path.join(base_path, "assets", "img", "logo.png"))
        self.logo_img = ctk.CTkImage(dark_image=self.logo_img_data, light_image=self.logo_img_data, size=(77.68, 85.42))
        self.logo = ctk.CTkLabel(master=self.sidebar_frame, text="", image=self.logo_img)
        self.logo.grid(row=0, column=0, pady=(38,0), sticky="ew")

        # Dashboard button
        self.dashboard_img_data = Image.open(os.path.join(base_path, "assets", "img", "home_icon_transparent.png"))
        self.dashboard_img = ctk.CTkImage(dark_image=self.dashboard_img_data, light_image=self.dashboard_img_data)
        self.dashboard_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.dashboard_img, text="Dashboard", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.dashboard_btn.grid(row=1, column=0, padx=10, pady=(60,0), sticky="ew")

        # Devices button
        self.devices_img_data = Image.open(os.path.join(base_path, "assets", "img", "devices_icon.png"))
        self.devices_img = ctk.CTkImage(dark_image=self.devices_img_data, light_image=self.devices_img_data)
        self.devices_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.devices_img, text="Devices", fg_color="#fff", font=("Arial Bold", 14), text_color="#2A8C55", hover_color="#eee", anchor="w")
        self.devices_btn.grid(row=2, column=0, padx=10, pady=(16,0), sticky="ew")

        # Notification button
        self.notification_img_data = Image.open(os.path.join(base_path, "assets", "img", "notification_icon_transparent.png"))
        self.notification_img = ctk.CTkImage(dark_image=self.notification_img_data, light_image=self.notification_img_data)
        self.notification_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.notification_img, text="Notification", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.notification_btn.grid(row=3, column=0, padx=10, pady=(16,0), sticky="ew")

        # Settings button
        self.settings_img_data = Image.open( os.path.join(base_path, "assets", "img", "settings_icon.png"))
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

        self.title_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        self.orders_label = ctk.CTkLabel(self.title_frame, text="Devices", font=("Arial Black", 25), text_color="#2A8C55")
        self.orders_label.pack(anchor="nw", side="left")

        self.new_orders = ctk.CTkButton(self.title_frame, text="+ New Device", font=("Arial Black", 15), text_color="#fff", fg_color="#2A8C55", hover_color="#207244", command=self.add_new_relay_dynamically)
        self.new_orders.pack(anchor="ne", side="right")

        # Relays Group
        self.relay_group_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.relay_group_frame.pack(anchor="nw",fill="x", padx=27, pady=(36, 0))
        self.relay_img_data = Image.open(os.path.join(base_path, "assets", "img", "relay_icon.png"))
        self.relay_img = ctk.CTkImage(dark_image=self.relay_img_data, light_image=self.relay_img_data, size=(43, 43))
        
        # Create 6 relay switches
        self.create_switches(3)

        # self.table_frame_container = ctk.CTkFrame(self.main_view, fg_color="#D3D3D3")
        # self.table_frame_container.pack(expand=True, fill="both", padx=10, pady=10)

        self.table_frame = ctk.CTkScrollableFrame(self.main_view, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Table Data
        self.table_data = [
            ["Relay Name", "Status", "Time"]
        ]

        # Create Table
        self.table = CTkTable(self.table_frame, values=self.table_data, colors=["#E6E6E6", "#EEEEEE"], 
                              header_color="#2A8C55", hover_color="#B4B4B4")
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        self.table.pack(expand=True, fill="both")

        # Fetch relay data
        self.fetch_relay_data()

        # Fetch relay history
        self.get_relay_history()

    # Function to create a specified number of switches
    def create_switches(self, num_switches):
        self.num_switches = num_switches
        for i in range(num_switches):
            self.add_relay(i)

    def add_relay(self, index=None):
        if index is None:
            index = self.num_switches
            self.num_switches += 1

        # Calculate row and column based on max_col
        row = index // self.max_col
        col = index % self.max_col

        # Create frame, label, and switch for the relay
        relay_frame = ctk.CTkFrame(self.relay_group_frame, border_color="#2A8C55", fg_color="transparent", border_width=2, width=178, height=60)
        relay_frame.grid_propagate(0)
        relay_frame.grid(row=row, column=col, padx=(15,0), pady=10)
        self.relay_frames.append(relay_frame)

        relay_img_label = ctk.CTkLabel(relay_frame, image=self.relay_img, text="")
        relay_img_label.grid(row=0, column=0, rowspan=2, padx=(12,0), pady=(10,10))
        self.relay_img_labels.append(relay_img_label)

        relay_label = ctk.CTkLabel(relay_frame, text=f"Relay {index + 1}", font=("Arial Black", 15), text_color="#2A8C55")
        relay_label.grid(row=0, column=1, pady=(2,0))
        self.relay_labels.append(relay_label)

        relay_switch = ctk.CTkSwitch(relay_frame, switch_width=60, switch_height=25, text="", command=lambda i=index: self.toggle_switch(i), onvalue="ON", offvalue="OFF")
        relay_switch.grid(row=1, column=1, padx=(20,5), pady=(0,10))
        self.switches.append(relay_switch)

    def add_new_relay_dynamically(self):
        # Call add_relay to add one more relay at runtime
        self.add_relay()
        # url = "https://do-an-ktmt-backend.onrender.com/api/data/relay/create"
        url = f"{URL}/api/data/relay/create"
        data = {
            "relayName": f"nutnhan{self.num_switches}",
            "status": "OFF"
        }
        try:
            response = requests.post(url, json=data)
        except requests.RequestException as e:
            print("An error occurred:", e)

    # Function to toggle relay switch
    def toggle_switch(self, switch):
        # url = "http://10.28.128.126:8080/api/data/relay/update"
        url = f"{URL}/api/data/relay/update"
        data = {
            "relayName": f"nutnhan{switch+1}",
            "status": self.switches[switch].get()
        } 
        try:
            response = requests.patch(url, json=data)
        except requests.RequestException as e:
            print("An error occurred:", e)
        
        self.get_relay_history()

    # Function to fetch status of relay
    def fetch_relay_data(self):
        url = f"{URL}/api/data/relay/all"
        response = requests.get(url).json()
        data = response["data"]

        for i in range(self.num_switches):
            if data[i].get("status") == "ON":
                self.switches[i].select()
            else:
                self.switches[i].deselect()
        
        # Schedule the next data fetch in 10 seconds
        self.after(10000, self.fetch_relay_data)

    # Function to fetch data from a URL and update the table
    def get_relay_history(self):
        url = f"{URL}/api/data/relay_history"
        response = requests.get(url).json()
        data = response["data"]

        # Clear the table once
        self.all_indices = list(range(len(self.table.values)))[1:]
        self.table.delete_rows(self.all_indices)

        # Add each row from the data
        for item in data:
            row = list(item.values())[1:]
            self.table.add_row(row)
              