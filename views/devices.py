import customtkinter as ctk
from PIL import Image
import requests
<<<<<<< HEAD
import os
from constant import *
from CTkTable import CTkTable
=======
>>>>>>> 3729710827dfcf61be214c7711f5aef27eb01601

class DevicesView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.switches = []
        self.relay_frames = []
        self.relay_img_labels = []
        self.relay_labels = []
        self.max_col = 3

        # Set up sidebar
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#2A8C55",  width=170, height=600, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

<<<<<<< HEAD
        self.logo_img_data = Image.open(os.path.join(base_path, "assets", "img", "logo.png"))
=======
        self.logo_img_data = Image.open("assets/img/logo.png")
>>>>>>> 3729710827dfcf61be214c7711f5aef27eb01601
        self.logo_img = ctk.CTkImage(dark_image=self.logo_img_data, light_image=self.logo_img_data, size=(77.68, 85.42))
        self.logo = ctk.CTkLabel(master=self.sidebar_frame, text="", image=self.logo_img)
        self.logo.grid(row=0, column=0, pady=(38,0), sticky="ew")

        # Dashboard button
<<<<<<< HEAD
        self.dashboard_img_data = Image.open(os.path.join(base_path, "assets", "img", "home_icon_transparent.png"))
=======
        self.dashboard_img_data = Image.open("assets/img/home_icon_transparent.png")
>>>>>>> 3729710827dfcf61be214c7711f5aef27eb01601
        self.dashboard_img = ctk.CTkImage(dark_image=self.dashboard_img_data, light_image=self.dashboard_img_data)
        self.dashboard_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.dashboard_img, text="Dashboard", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.dashboard_btn.grid(row=1, column=0, padx=10, pady=(60,0), sticky="ew")

        # Devices button
<<<<<<< HEAD
        self.devices_img_data = Image.open(os.path.join(base_path, "assets", "img", "devices_icon.png"))
=======
        self.devices_img_data = Image.open("assets/img/devices_icon.png")
>>>>>>> 3729710827dfcf61be214c7711f5aef27eb01601
        self.devices_img = ctk.CTkImage(dark_image=self.devices_img_data, light_image=self.devices_img_data)
        self.devices_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.devices_img, text="Devices", fg_color="#fff", font=("Arial Bold", 14), text_color="#2A8C55", hover_color="#eee", anchor="w")
        self.devices_btn.grid(row=2, column=0, padx=10, pady=(16,0), sticky="ew")

        # Notification button
<<<<<<< HEAD
        self.notification_img_data = Image.open(os.path.join(base_path, "assets", "img", "notification_icon_transparent.png"))
=======
        self.notification_img_data = Image.open("assets/img/notification_icon_transparent.png")
>>>>>>> 3729710827dfcf61be214c7711f5aef27eb01601
        self.notification_img = ctk.CTkImage(dark_image=self.notification_img_data, light_image=self.notification_img_data)
        self.notification_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.notification_img, text="Notification", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.notification_btn.grid(row=3, column=0, padx=10, pady=(16,0), sticky="ew")

        # Settings button
<<<<<<< HEAD
        self.settings_img_data = Image.open( os.path.join(base_path, "assets", "img", "settings_icon.png"))
=======
        self.settings_img_data = Image.open("assets/img/settings_icon.png")
>>>>>>> 3729710827dfcf61be214c7711f5aef27eb01601
        self.settings_img = ctk.CTkImage(dark_image=self.settings_img_data, light_image=self.settings_img_data)
        self.settings_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.settings_img, text="Settings", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.settings_btn.grid(row=4, column=0, padx=10, pady=(16,0), sticky="ew")

        # Sign out button
        self.signout_btn = ctk.CTkButton(self.sidebar_frame, text="Sign Out", font=("Arial Bold", 14), fg_color="#fff", text_color="#2A8C55", hover_color="#eee")
        self.signout_btn.pack(side="bottom", padx=10, pady=(0,10))

        # Set up main view
<<<<<<< HEAD
        self.main_view = ctk.CTkFrame(self, fg_color="#fff", width=640, height=600, corner_radius=0)
=======
        self.main_view = ctk.CTkFrame(self, fg_color="#fff",  width=640, height=600, corner_radius=0)
>>>>>>> 3729710827dfcf61be214c7711f5aef27eb01601
        self.main_view.pack_propagate(0)
        self.main_view.pack(fill="y", anchor="w", side="left")

        # self.greeting = ctk.CTkLabel(self.main_view, text="")
        # self.greeting.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.title_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        self.orders_label = ctk.CTkLabel(self.title_frame, text="Devices", font=("Arial Black", 25), text_color="#2A8C55")
        self.orders_label.pack(anchor="nw", side="left")

        self.new_orders = ctk.CTkButton(self.title_frame, text="+ New Device", font=("Arial Black", 15), text_color="#fff", fg_color="#2A8C55", hover_color="#207244")
        self.new_orders.pack(anchor="ne", side="right")

        # Relays Group
        self.relay_group_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.relay_group_frame.pack(anchor="n",fill="x", padx=27, pady=(36, 0))
<<<<<<< HEAD
        self.relay_img_data = Image.open(os.path.join(base_path, "assets", "img", "relay_icon.png"))
=======
        self.relay_img_data = Image.open("assets/img/relay_icon.png")
>>>>>>> 3729710827dfcf61be214c7711f5aef27eb01601
        self.relay_img = ctk.CTkImage(dark_image=self.relay_img_data, light_image=self.relay_img_data, size=(43, 43))
        
        # Create 6 relay switches
        self.create_switches(6)

<<<<<<< HEAD
        self.table_frame_container = ctk.CTkFrame(self.main_view, fg_color="#D3D3D3")
        self.table_frame_container.pack(expand=True, fill="both", padx=10, pady=10)

        self.table_frame = ctk.CTkScrollableFrame(self.table_frame_container, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Table Data
        self.table_data = [
            ["Relay ID", "Relay Name", "Status", "Time"],
            ['1', 'Máy bơm 1', 'On', '12:00 1/11/2024'],
            ['2', 'Máy bơm 2', 'Off', '12:00 1/11/2024'],
            ['3', 'Máy bơm 3', 'On', '12:00 2/11/2024'],
            ['4', 'Máy bơm 4', 'Off', '12:00 2/11/2024']
        ]

        # Create Table
        self.table = CTkTable(self.table_frame, values=self.table_data, colors=["#E6E6E6", "#EEEEEE"], 
                              header_color="#2A8C55", hover_color="#B4B4B4")
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        self.table.pack(expand=True, fill="both")

=======
>>>>>>> 3729710827dfcf61be214c7711f5aef27eb01601
        # Fetch relay data
        self.fetch_relay_data()

    # Function to create a specified number of switches
    def create_switches(self, num_switches):
        for i in range(num_switches):
            # Calculate row and column base on max column
            self.row = i // self.max_col
            self.col = i % self.max_col
            
            self.relay_frame = ctk.CTkFrame(self.relay_group_frame,border_color="#2A8C55", fg_color="transparent", border_width=2, width=178, height=60)
            self.relay_frame.grid_propagate(0)
            self.relay_frame.grid(row=self.row, column=self.col, padx=(15,0), pady=10)
            self.relay_frames.append(self.relay_frame)

            self.relay_img_label = ctk.CTkLabel(self.relay_frames[i], image=self.relay_img, text="")
            self.relay_img_label.grid(row=0, column=0, rowspan=2, padx=(12,0), pady=(10,10))
            self.relay_img_labels.append(self.relay_img_label)

            self.relay_label = ctk.CTkLabel(self.relay_frames[i], text=f"Relay {i + 1}", font=("Arial Black", 15), text_color="#2A8C55")
            self.relay_label.grid(row=0, column=1, pady=(2,0))
            self.relay_labels.append(self.relay_label)

            self.relay_switch = ctk.CTkSwitch(self.relay_frames[i], switch_width=60, switch_height=25, text="", command=lambda i=i: self.toggle_switch(i), onvalue="ON", offvalue="OFF")
            self.relay_switch.grid(row=1, column=1, padx=(20,5), pady=(0,10))
            self.switches.append(self.relay_switch)

    # Function to toggle relay switch
    def toggle_switch(self, switch):
        url = "https://do-an-ktmt-backend.onrender.com/api/data/relay/update"
        data = {
            "relayName": f"nutnhan{switch+1}",
            "status": self.switches[switch].get()
        } 
        try:
            response = requests.patch(url, json=data)
        except requests.RequestException as e:
            print("An error occurred:", e)

    # Function to fetch status of relay
    def fetch_relay_data(self):
        
        response = requests.get("https://do-an-ktmt-backend.onrender.com/api/data/relay/all").json()
        data = response["data"]

        for i in range(len(data)):
            if data[i].get("status") == "ON":
                self.switches[i].select()
            else:
                self.switches[i].deselect()
        
        # Schedule the next data fetch in 10 seconds
        self.after(10000, self.fetch_relay_data)