import PyQt5.QtWidgets

import ui.home.homeweather
import ui.home.nextalarm
import ui.home.clock

import utils.layout


class HomeScreen(PyQt5.QtWidgets.QWidget):
    def __init__(self, alarm_manager, parent=None):
        super(HomeScreen, self).__init__(parent)
        self.setup_screen(alarm_manager.get_next_alarm_time())

    def setup_screen(self, next_alarm):
        vert_layout = utils.layout.create_vertical_layout(self)
        vert_layout.addWidget(ui.home.homeweather.Group())
        vert_layout.addWidget(ui.home.clock.DigitalClock())
        vert_layout.addWidget(ui.home.nextalarm.NextAlarm(next_alarm))

    def show_weather(self, show):
        self.findChild(ui.home.homeweather.Group).show_weather(show)

    def update_weather(self, updates):
        self.findChild(ui.home.homeweather.Group).update_all(updates)
