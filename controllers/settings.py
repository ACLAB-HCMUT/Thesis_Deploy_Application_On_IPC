# controller/settings.py

from models.main import Model
from views.main import View


class SettingsController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["settings"]
        self._bind()

    def _bind(self) -> None:
        """Liên kết các hàm của controller với các nút trong view"""
        self.frame.signout_btn.configure(command=self.logout)
        self.frame.dashboard_btn.configure(command=self.dashboard)
        self.frame.devices_btn.configure(command=self.devices)
        self.frame.notification_btn.configure(command=self.notifications)
    
    def logout(self) -> None:
        """Xử lý đăng xuất"""
        self.model.auth.logout()

    def dashboard(self) -> None:
        """Chuyển sang màn hình chính"""
        self.view.switch("home")

    def devices(self) -> None:
        """Chuyển sang màn hình quản lý thiết bị"""
        self.view.switch("devices")

    def notifications(self) -> None:
        """Chuyển sang màn hình thông báo"""
        self.view.switch("notification")
