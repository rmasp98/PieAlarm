
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

import ui.controller


class SnoozeScreen(QWidget):

    def __init__(self, alarm_manager, parent=None):
        super(SnoozeScreen, self).__init__(parent)
        self._alarm_manager = alarm_manager

        layout = QVBoxLayout()
        self.setLayout(layout)

        snooze = QLabel("Snooze")
        snooze.mouseReleaseEvent = self._snooze_event
        layout.addWidget(snooze)

        stop = QLabel("Stop")
        stop.mouseReleaseEvent = self._stop_event
        layout.addWidget(stop)

    def _snooze_event(self, _):
        self._alarm_manager.snooze()
        ui.controller.UiController().set_screen("main")

    def _stop_event(self, _):
        self._alarm_manager.stop()
        ui.controller.UiController().set_screen("main")





#Need to display:
# - time
# - days
# - repeat
# - playback
# - name
# - active
