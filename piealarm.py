from ui.controller import UiController
from alarm.alarm import Alarm

if __name__ == "__main__":
    ui = UiController()
    # ui.window.update_weather((22, "sunny") for i in range(5))
    ui.window.set_theme("Default")

    alarm = Alarm()



    ui.exec()
