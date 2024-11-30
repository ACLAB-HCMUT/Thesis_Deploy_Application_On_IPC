from models.main import Model
from models.auth import User
from views.main import View
import re
import requests
from utils.constant import *
class SignUpController:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.frame = self.view.frames["signup"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.signup_btn.configure(command=self.signup)
        self.frame.login_btn.configure(command=self.signin)

    def signin(self) -> None:
        self.view.switch("signin")
        self.clear_validation_msg()

    def signup(self) -> None:
        url = f"{URL}/api/users/register"

        data = {
            "name": self.frame.fullname_input.get(),
            "password": self.frame.password_input.get(),
            "email": self.frame.email_input.get(),
            "phoneNumber": self.frame.phone_input.get(),
            "address": self.frame.address_input.get()
        }

        if not self.is_valid_email(data["email"]):
            self.frame.email_status_label.configure(text="Invalid email")
            return
        
        try:
            response = requests.post(url, json=data)
        except requests.RequestException as e:
            print("An error occurred:", e)

        if response.status_code == 409:
            self.frame.email_status_label.configure(text="Email already exists")
            return
        else:
            self.clear_validation_msg()
            self.clear_form()
            self.view.switch("signin")
        
    def is_valid_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def clear_validation_msg(self) -> None:
        self.frame.email_status_label.configure(text="")

    def clear_form(self) -> None:
        fullname = self.frame.fullname_input.get()
        email = self.frame.email_input.get()
        password = self.frame.password_input.get()
        phone = self.frame.phone_input.get()
        address = self.frame.address_input.get()
        self.frame.fullname_input.delete(0, last_index=len(fullname))
        self.frame.fullname_input.focus()
        self.frame.email_input.delete(0, last_index=len(email))
        self.frame.password_input.delete(0, last_index=len(password))
        self.frame.phone_input.delete(0, last_index=len(phone))
        self.frame.address_input.delete(0, last_index=len(address))
