from ui.ui_controller import UiController

if __name__ == "__main__":
    ui = UiController()
    ui.window.set_weather((22, "sunny") for i in range(5))
    # ui.window.set_dark()
    ui.exec()
