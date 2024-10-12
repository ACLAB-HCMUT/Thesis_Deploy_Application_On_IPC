import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY

def display_settings_content(content_frame, root):
    settings_label = ttk.Label(content_frame, text="Settings", font=("Arial", 18))
    settings_label.pack(pady=20)

    setting_option1 = ttk.Checkbutton(content_frame, text="Enable Notifications")
    setting_option1.pack(pady=5)

    # Light/Dark Mode Toggle
    current_theme = ttk.Style().theme_use()
    theme_label = ttk.Label(content_frame, text=f"Current Theme: {current_theme}", font=("Arial", 12))
    theme_label.pack(pady=10)

    def toggle_theme():
        # Toggle between 'flatly' (light) and 'darkly' (dark)
        if ttk.Style().theme_use() == "flatly":
            ttk.Style().theme_use("darkly")
            theme_label.config(text="Current Theme: darkly")
        else:
            ttk.Style().theme_use("flatly")
            theme_label.config(text="Current Theme: flatly")

    theme_toggle_button = ttk.Button(content_frame, text="Toggle Light/Dark Mode", bootstyle=PRIMARY, command=toggle_theme)
    theme_toggle_button.pack(pady=10)
