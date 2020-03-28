import PyQt5.QtWidgets
import ui.main.clock

import weather.ui.main
import alarm.ui.nextalarm

import utils.layout


class Screen(PyQt5.QtWidgets.QWidget):
    def __init__(self, alarm_manager, parent=None):
        super(Screen, self).__init__(parent)
        self.setup_screen(alarm_manager.get_next_alarm_time())

    def setup_screen(self, next_alarm):
        vert_layout = utils.layout.create_vertical_layout(self)
        vert_layout.addWidget(weather.ui.main.Group())
        vert_layout.addWidget(ui.main.clock.DigitalClock())
        vert_layout.addWidget(alarm.ui.nextalarm.NextAlarm(next_alarm))

    def show_weather(self, show):
        self.findChild(weather.ui.main.Group).show_weather(show)

    def update_weather(self, updates):
        self.findChild(weather.ui.main.Group).update_all(updates)
