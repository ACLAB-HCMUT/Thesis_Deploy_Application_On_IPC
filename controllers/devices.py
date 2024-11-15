from models.main import Model
from views.main import View


class DevicesController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["devices"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.signout_btn.configure(command=self.logout)
        self.frame.dashboard_btn.configure(command=self.dashboard)
        self.frame.notification_btn.configure(command=self.notification)
        self.frame.settings_btn.configure(command=self.settings)
    def logout(self) -> None:
        self.model.auth.logout()

    def dashboard(self) -> None:
        self.view.switch("home")
        
    def notification(self) -> None:
        self.view.switch("notification")
        
    def settings(self) -> None:
        self.view.switch("settings")
    # def update_view(self) -> None:
    #     current_user = self.model.auth.current_user
    #     if current_user:
    #         username = current_user["username"]
    #         self.frame.greeting.configure(text=f"Welcome, {username}!")
    #     else:
    #         self.frame.greeting.configure(text=f"")
