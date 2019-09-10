
from PyQt5.QtWidgets import QLabel

import ui.controller

class NextAlarm(QLabel):

    def __init__(self, time, parent=None):
        super(NextAlarm, self).__init__(parent)
        self.set_time(time)
        self.mouseReleaseEvent = _click_event

    def set_time(self, time):
        self.setText("Next Alarm:\n" + "{:0>2d}:{:0>2d}".format(time.hour, time.minute))

def _click_event(_):
    ui.controller.UiController().screen_signal.emit("alarm_view")
