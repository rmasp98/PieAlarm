
from ui.controller import UiController


if __name__ == "__main__":
    ui = UiController(theme="dark")
    # ui = UiController()
    # ui.window.update_weather((22, "sunny") for i in range(5))
    # ui.set_theme("default")

    ui.exec()
    print("Finish")
