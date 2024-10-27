from models.main import Model
from views.main import View


class NotificationController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["notification"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.signout_btn.configure(command=self.logout)
        self.frame.dashboard_btn.configure(command=self.dashboard)
        self.frame.devices_btn.configure(command=self.devices)

    def logout(self) -> None:
        self.model.auth.logout()

    def dashboard(self) -> None:
        self.view.switch("home")

    def devices(self) -> None:
        self.view.switch("devices")
        
    # def update_view(self) -> None:
    #     current_user = self.model.auth.current_user
    #     if current_user:
    #         username = current_user["username"]
    #         self.frame.greeting.configure(text=f"Welcome, {username}!")
    #     else:
    #         self.frame.greeting.configure(text=f"")
