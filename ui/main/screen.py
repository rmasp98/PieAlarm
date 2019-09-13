
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ui.main.clock import DigitalClock
from ui.main.weather import WeatherGroup
from alarm.ui.nextalarm import NextAlarm


class Screen(QWidget):

    def __init__(self, alarm_manager, parent=None):
        super(Screen, self).__init__(parent)
        self.setup_screen(alarm_manager.get_next_alarm_time())

    def setup_screen(self, next_alarm):
        vert_layout = QVBoxLayout(self)
        vert_layout.addWidget(WeatherGroup())
        vert_layout.addWidget(DigitalClock())
        vert_layout.addWidget(NextAlarm(next_alarm))

    def show_weather(self, show):
        self.findChild(WeatherGroup).show_weather(show)

    def update_weather(self, updates):
        self.findChild(WeatherGroup).update_all(updates)
