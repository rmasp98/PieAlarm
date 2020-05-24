import time
import threading

import PyQt5.QtWidgets

from ui.home.homeweather import Group as WeatherGroup
from ui.home.nextalarm import NextAlarm
from ui.widgets.time import Time

from ui.widgets.layout import create_vertical_layout
from ui.widgets.text import FontSize
import ui


class HomeScreen(PyQt5.QtWidgets.QWidget):
    def __init__(self, alarm_manager, weather, parent=None):
        super(HomeScreen, self).__init__(parent)
        ui.Ctrl().enable_toolbar_action("back", False)
        self._sleep = threading.Event()

        vert_layout = create_vertical_layout(self)
        vert_layout.addWidget(WeatherGroup(weather))
        vert_layout.addStretch()
        vert_layout.addWidget(Time(FontSize.EXTRALARGE))
        vert_layout.addStretch()
        vert_layout.addWidget(NextAlarm(alarm_manager.get_next_alarm_time()))

    def mousePressEvent(self, _):
        threading.Thread(target=self._show_temp_toolbar).start()

    def _show_temp_toolbar(self):
        self._sleep.set()
        self._sleep.clear()
        ui.Ctrl().enable_toolbar_action("light", True)
        ui.Ctrl().enable_toolbar_action("settings", True)
        if not self._sleep.wait(3):
            ui.Ctrl().enable_toolbar_action("light", False)
            ui.Ctrl().enable_toolbar_action("settings", False)
