import tkinter as tk
import requests

class APIClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.access_token = None

    def signin(self, username, password):
        url = f"{self.base_url}/signin"
        response = requests.post(url, json={"username": username, "password": password})
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
            return True
        else:
            print("Signin failed:", response.json())
            return False

    def refresh_token(self):
        url = f"{self.base_url}/refresh-token"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
            print("Token refreshed successfully")
        else:
            print("Failed to refresh token:", response.json())
            self.access_token = None  # Reset token if refresh fails

    def get_message(self):
        url = f"{self.base_url}/get-message"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json().get("message")
        elif response.status_code == 401 and response.json().get("detail") == "Token has expired. Please refresh.":
            # Token expired, attempt to refresh
            self.refresh_token()
            # Try again with the new token
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return response.json().get("message")
        else:
            print("Failed to retrieve message:", response.json())
            return None

class App:
    def __init__(self, root):
        self.api_client = APIClient()
        self.root = root
        self.root.title("JWT Authentication Example")

        # Signin form
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.signin_button = tk.Button(root, text="Sign In", command=self.handle_signin)
        self.signin_button.pack()

        # Message display
        self.message_label = tk.Label(root, text="", fg="green")
        self.message_label.pack()

        self.get_message_button = tk.Button(root, text="Get Message", command=self.handle_get_message)
        self.get_message_button.pack()

    def handle_signin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success = self.api_client.signin(username, password)
        if success:
            self.message_label.config(text="Sign in successful", fg="green")
        else:
            self.message_label.config(text="Sign in failed", fg="red")

    def handle_get_message(self):
        message = self.api_client.get_message()
        if message:
            self.message_label.config(text=message, fg="green")
        else:
            self.message_label.config(text="Failed to get message", fg="red")

# Run the application
root = tk.Tk()
app = App(root)
root.mainloop()
