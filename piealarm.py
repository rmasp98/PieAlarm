import ui.controller

if __name__ == "__main__":
    # ui = UiController("alarm_view", theme="dark")
    ui = ui.controller.UiController(theme="dark")
    # ui = ui.controller.UiController()

    ui.exec()
    print("Finish")
