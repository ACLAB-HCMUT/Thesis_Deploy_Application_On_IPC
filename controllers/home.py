from models.main import Model
from views.main import View


class HomeController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["home"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.signout_btn.configure(command=self.logout)
        self.frame.devices_btn.configure(command=self.devices)
        self.frame.notification_btn.configure(command=self.notification)

    def logout(self) -> None:
        self.model.auth.logout()

    def devices(self) -> None:
        self.view.switch("devices")

    def notification(self) -> None:
        self.view.switch("notification")
                    
    # def update_view(self) -> None:
    #     current_user = self.model.auth.current_user
    #     if current_user:
    #         username = current_user["username"]
    #         self.frame.greeting.configure(text=f"Welcome, {username}!")
    #     else:
    #         self.frame.greeting.configure(text=f"")
