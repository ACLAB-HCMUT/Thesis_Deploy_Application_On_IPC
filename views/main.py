from typing import TypedDict

from .root import Root
from .home import HomeView
from .signin import SignInView
from .signup import SignUpView
from .devices import DevicesView
from .notification import NotificationView
from .settings import SettingsView

class Frames(TypedDict):
    signup: SignUpView
    signin: SignInView
    home: HomeView
    devices: DevicesView
    notification: NotificationView
    settings: SettingsView

class View:
    def __init__(self):
        self.root = Root()
        self.frames: Frames = {}  # type: ignore

        self._add_frame(SignUpView, "signup")
        self._add_frame(SignInView, "signin")
        self._add_frame(HomeView, "home")
        self._add_frame(DevicesView, "devices")
        self._add_frame(NotificationView, "notification")
        self._add_frame(SettingsView, "settings")

    def _add_frame(self, Frame, name: str) -> None:
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def switch(self, name: str) -> None:
        frame = self.frames[name]
        frame.tkraise()

    def start_mainloop(self) -> None:
        self.root.mainloop()
