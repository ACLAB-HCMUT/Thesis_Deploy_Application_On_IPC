from tkinter import Frame, Label, Button
import customtkinter as ctk
from PIL import Image
import requests

class DevicesView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.switches = []
        self.relay_frames = []
        self.relay_img_labels = []
        self.relay_labels = []

        # Set up sidebar
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#2A8C55",  width=176, height=650, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        self.logo_img_data = Image.open("assets/img/logo.png")
        self.logo_img = ctk.CTkImage(dark_image=self.logo_img_data, light_image=self.logo_img_data, size=(77.68, 85.42))
        self.logo = ctk.CTkLabel(master=self.sidebar_frame, text="", image=self.logo_img)
        self.logo.grid(row=0, column=0, pady=(38,0), sticky="ew")

        # Dashboard button
        self.dashboard_img_data = Image.open("assets/img/home_icon_transparent.png")
        self.dashboard_img = ctk.CTkImage(dark_image=self.dashboard_img_data, light_image=self.dashboard_img_data)
        self.dashboard_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.dashboard_img, text="Dashboard", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w")
        self.dashboard_btn.grid(row=1, column=0, padx=10, pady=(60,0), sticky="ew")

        # Devices button
        self.devices_img_data = Image.open("assets/img/devices_icon.png")
        self.devices_img = ctk.CTkImage(dark_image=self.devices_img_data, light_image=self.devices_img_data)
        self.devices_btn = ctk.CTkButton(master=self.sidebar_frame, image=self.devices_img, text="Devices", fg_color="#fff", font=("Arial Bold", 14), text_color="#2A8C55", hover_color="#eee", anchor="w")
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
        self.signout_btn.grid(row=6, column=0, padx=10, pady=(250,0), sticky="ew")

        # Set up main view
        self.main_view = ctk.CTkFrame(self, fg_color="#fff",  width=680, height=650, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")

        # self.greeting = ctk.CTkLabel(self.main_view, text="")
        # self.greeting.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.title_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        self.orders_label = ctk.CTkLabel(self.title_frame, text="Devices", font=("Arial Black", 25), text_color="#2A8C55")
        self.orders_label.pack(anchor="nw", side="left")

        self.new_orders = ctk.CTkButton(self.title_frame, text="+ New Device", font=("Arial Black", 15), text_color="#fff", fg_color="#2A8C55", hover_color="#207244")
        self.new_orders.pack(anchor="ne", side="right")

        # Relays Group 1

        self.relay_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.relay_frame.pack(anchor="n",fill="x", padx=27, pady=(36, 0))

        # Relay1

        self.relay1_frame = ctk.CTkFrame(self.relay_frame,border_color="#2A8C55", fg_color="transparent", border_width=2, width=200, height=60)
        self.relay1_frame.grid_propagate(0)
        self.relay1_frame.pack(side="left")

        self.relay_img_data = Image.open("assets/img/relay_icon.png")
        self.relay_img = ctk.CTkImage(dark_image=self.relay_img_data, light_image=self.relay_img_data, size=(43, 43))
        self.relay1_img_label = ctk.CTkLabel(self.relay1_frame, image=self.relay_img, text="")
        self.relay1_img_label.grid(row=0, column=0, rowspan=2, padx=(12,5), pady=(10,10))

        self.relay1_label = ctk.CTkLabel(self.relay1_frame, text="Relay 1", font=("Arial Black", 15), text_color="#2A8C55")
        self.relay1_label.grid(row=0, column=1, pady=(2,0))

        self.switch1_var = ctk.StringVar(value="")
        self.relay1_switch = ctk.CTkSwitch(self.relay1_frame, switch_width=60, switch_height=25, variable=self.switch1_var, command=self.switcher, text="", onvalue="ON", offvalue="OFF")
        self.relay1_switch.grid(row=1, column=1, padx=(35,5), pady=(0,10))

        # Relay 2

        self.relay2_frame = ctk.CTkFrame(self.relay_frame,border_color="#2A8C55", fg_color="transparent", border_width=2, width=200, height=60)
        self.relay2_frame.grid_propagate(0)
        self.relay2_frame.pack(side="left", expand=True, anchor="center")

        self.relay2_img_label = ctk.CTkLabel(self.relay2_frame, image=self.relay_img, text="")
        self.relay2_img_label.grid(row=0, column=0, rowspan=2, padx=(12,5), pady=(10,10))

        self.relay2_label = ctk.CTkLabel(self.relay2_frame, text="Relay 2", font=("Arial Black", 15), text_color="#2A8C55")
        self.relay2_label.grid(row=0, column=1, pady=(2,0))
        
        
        self.relay2_switch = ctk.CTkSwitch(self.relay2_frame, switch_width=60, switch_height=25, text="", onvalue="ON", offvalue="OFF")
        self.relay2_switch.grid(row=1, column=1, padx=(35,5), pady=(0,10))

        # Relay 3

        self.relay3_frame = ctk.CTkFrame(self.relay_frame,border_color="#2A8C55", fg_color="transparent", border_width=2, width=200, height=60)
        self.relay3_frame.grid_propagate(0)
        self.relay3_frame.pack(side="right")

        self.relay3_img_label = ctk.CTkLabel(self.relay3_frame, image=self.relay_img, text="")
        self.relay3_img_label.grid(row=0, column=0, rowspan=2, padx=(12,5), pady=(10,10))

        self.relay3_label = ctk.CTkLabel(self.relay3_frame, text="Relay 3", font=("Arial Black", 15), text_color="#2A8C55")
        self.relay3_label.grid(row=0, column=1, pady=(2,0))
        
        self.relay3_switch = ctk.CTkSwitch(self.relay3_frame, switch_width=60, switch_height=25, text="", onvalue="ON", offvalue="OFF")
        self.relay3_switch.grid(row=1, column=1, padx=(35,5), pady=(0,10))

        # Relays Group 2

        self.relay_group2_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.relay_group2_frame.pack(anchor="n",fill="x", padx=27, pady=(36, 0))

        # Relay 4

        self.relay4_frame = ctk.CTkFrame(self.relay_group2_frame,border_color="#2A8C55", fg_color="transparent", border_width=2, width=200, height=60)
        self.relay4_frame.grid_propagate(0)
        self.relay4_frame.pack(side="left")

        self.relay4_img_label = ctk.CTkLabel(self.relay4_frame, image=self.relay_img, text="")
        self.relay4_img_label.grid(row=0, column=0, rowspan=2, padx=(12,5), pady=(10,10))

        self.relay4_label = ctk.CTkLabel(self.relay4_frame, text="Relay 4", font=("Arial Black", 15), text_color="#2A8C55")
        self.relay4_label.grid(row=0, column=1, pady=(2,0))
        
        self.relay4_switch = ctk.CTkSwitch(self.relay4_frame, switch_width=60, switch_height=25, text="", onvalue="ON", offvalue="OFF")
        self.relay4_switch.grid(row=1, column=1, padx=(35,5), pady=(0,10))

        # Relay 5

        self.relay5_frame = ctk.CTkFrame(self.relay_group2_frame,border_color="#2A8C55", fg_color="transparent", border_width=2, width=200, height=60)
        self.relay5_frame.grid_propagate(0)
        self.relay5_frame.pack(side="left", expand=True, anchor="center")

        self.relay5_img_label = ctk.CTkLabel(self.relay5_frame, image=self.relay_img, text="")
        self.relay5_img_label.grid(row=0, column=0, rowspan=2, padx=(12,5), pady=(10,10))

        self.relay5_label = ctk.CTkLabel(self.relay5_frame, text="Relay 5", font=("Arial Black", 15), text_color="#2A8C55")
        self.relay5_label.grid(row=0, column=1, pady=(2,0))
        
        self.relay5_switch = ctk.CTkSwitch(self.relay5_frame, switch_width=60, switch_height=25, text="", onvalue="ON", offvalue="OFF")
        self.relay5_switch.grid(row=1, column=1, padx=(35,5), pady=(0,10))

        # Relay 6

        self.relay6_frame = ctk.CTkFrame(self.relay_group2_frame,border_color="#2A8C55", fg_color="transparent", border_width=2, width=200, height=60)
        self.relay6_frame.grid_propagate(0)
        self.relay6_frame.pack(side="right")

        self.relay6_img_label = ctk.CTkLabel(self.relay6_frame, image=self.relay_img, text="")
        self.relay6_img_label.grid(row=0, column=0, rowspan=2, padx=(12,5), pady=(10,10))

        self.relay6_label = ctk.CTkLabel(self.relay6_frame, text="Relay 6", font=("Arial Black", 15), text_color="#2A8C55")
        self.relay6_label.grid(row=0, column=1, pady=(2,0))
    
        self.relay6_switch = ctk.CTkSwitch(self.relay6_frame, switch_width=60, switch_height=25, text="", onvalue="ON", offvalue="OFF")
        self.relay6_switch.grid(row=1, column=1, padx=(35,5), pady=(0,10))

        # # Relays Group 3
        # self.relay_group3_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        # self.relay_group3_frame.pack(anchor="n",fill="x", padx=27, pady=(36, 0))
        # self.create_switches(3)

        # Fetch relay data
        self.fetch_relay_data()

    # Function to create a specified number of switches
    # def create_switches(self, num_switches):
    #     for i in range(num_switches):
    #         self.relay_frame = ctk.CTkFrame(self.relay_group3_frame,border_color="#2A8C55", fg_color="transparent", border_width=2, width=200, height=60)
    #         self.relay_frame.grid_propagate(0)
    #         self.relay_frame.pack(side="left", expand=True, anchor="center")
    #         self.relay_frames.append(self.relay_frame)

    #         self.relay_img_label = ctk.CTkLabel(self.relay_frames[i], image=self.relay_img, text="")
    #         self.relay_img_label.grid(row=0, column=0, rowspan=2, padx=(12,5), pady=(10,10))
    #         self.relay_img_labels.append(self.relay_img_label)

    #         self.relay_label = ctk.CTkLabel(self.relay_frames[i], text="Relay 6", font=("Arial Black", 15), text_color="#2A8C55")
    #         self.relay_label.grid(row=0, column=1, pady=(2,0))
    #         self.relay_labels.append(self.relay_label)

    #         self.relay_switch = ctk.CTkSwitch(self.relay_frames[i], switch_width=60, switch_height=25, text="", onvalue="ON", offvalue="OFF")
    #         self.relay_switch.grid(row=1, column=1, padx=(35,5), pady=(0,10))
    #         self.switches.append(self.relay_switch)

    def switcher(self):
        url = "https://do-an-ktmt-backend.onrender.com/api/data/relay/update"
        data = {
            "relayName": "nutnhan1",
            "status": self.switch1_var.get()
        }

        try:
            # Send a PATCH request
            response = requests.patch(url, json=data)

            # Check if the request was successful
            if response.status_code == 200:
                print("Update successful")
            else:
                print("Failed to update. Status code:", response.status_code)
        except requests.RequestException as e:
            print("An error occurred:", e)
        
    def fetch_relay_data(self):
        
        response = requests.get("https://do-an-ktmt-backend.onrender.com/api/data/relay/all").json()
        data = response["data"]

        if data[0].get("status") == "ON":
            self.relay1_switch.select()
        else:
            self.relay1_switch.deselect()
        
        # Schedule the next data fetch in 10 seconds
        self.after(10000, self.fetch_relay_data)