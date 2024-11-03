from models.main import Model
from views.main import View
from controllers.main import Controller
import customtkinter


def main():
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()


if __name__ == "__main__":
    main()
