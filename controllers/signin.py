from models.main import Model
from models.auth import User
from views.main import View
import requests

class SignInController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["signin"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.login_btn.configure(command=self.signin)
        self.frame.signup_btn.configure(command=self.signup)

    def signup(self) -> None:
        self.view.switch("signup")

    def signin(self) -> None:
        email = self.frame.email_entry.get()
        password = self.frame.password_entry.get()
        url = "https://do-an-ktmt-backend.onrender.com/api/users/login"
        data = {
            "email": email,
            "password": password
        }
    
        try:
            response = requests.post(url, json=data)
        except requests.RequestException as e:
            print("An error occurred:", e)

        if response.status_code == 200:
            self.frame.password_entry.delete(0, last_index=len(password))
            user: User = {"username": data["email"]}
            self.model.auth.login(user)
        else:
            print("Invalid credentials")
