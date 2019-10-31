import ui.controller

if __name__ == "__main__":
    # ui = UiController("alarm_view", theme="dark")
    ui = ui.controller.UiController(theme="dark")
    # ui = UiController()
    # ui.window.update_weather((22, "sunny") for i in range(5))
    # ui.set_theme("default")

    ui.exec()
    print("Finish")
