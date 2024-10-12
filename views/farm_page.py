import ttkbootstrap as ttk

def display_farm_content(content_frame):
    farm_label = ttk.Label(content_frame, text="Farm Information", font=("Arial", 18))
    farm_label.pack(pady=20)

    farm_detail = ttk.Label(content_frame, text="Here is some information about the farm...")
    farm_detail.pack(pady=10)
