# controllers/main_controller.py

from views.login_view import LoginView
from views.home_view import HomeView
from logic.login_logic import check_login

class MainController:
    def __init__(self, root):
        self.root = root
        self.login_view = LoginView(root, self)
        self.home_view = HomeView(root, self)

        self.login_view.pack(fill="both", expand=True)
        self.home_view.pack_forget()

    def handle_login(self, username, password):
        if check_login(username, password):
            # self.switch_to_home()
            return True
        else:
            return False

    def switch_to_home(self):
        self.login_view.pack_forget()
        self.home_view.pack(fill="both", expand=True)

    def switch_to_login(self):
        self.login_view.reset_fields()
        self.home_view.pack_forget()
        self.login_view.pack(fill="both", expand=True)
