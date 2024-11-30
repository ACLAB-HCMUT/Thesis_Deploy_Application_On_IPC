from models.main import Model
from models.auth import User
from views.main import View
import requests
from utils.constant import *
class SignInController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["signin"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.login_btn.configure(command=self.signin)
        # self.frame.signup_btn.configure(command=self.signup)
        self.frame.signup_label.bind("<Button-1>", lambda e: self.signup())

    def signup(self) -> None:
        self.view.switch("signup")
        self.frame.cred_status_label.configure(text="")

    def signin(self) -> None:
        email = self.frame.email_entry.get()
        password = self.frame.password_entry.get()
        url = f"{URL}/api/users/login"
        data = {
            "email": email,
            "password": password
        }
    
        try:
            response = requests.post(url, json=data)
        except requests.RequestException as e:
            print("An error occurred:", e)

        if response.status_code == 200:
            self.frame.cred_status_label.configure(text="")
            self.frame.password_entry.delete(0, last_index=len(password))
            user: User = {"username": data["email"]}
            self.model.auth.login(user)
        else:
            self.frame.cred_status_label.configure(text="Invalid email or password")
