
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap

from alarm.alarm import Alarm
import ui.controller

class DayWidget(QLabel):
    pass

class TimeWidget(QLabel):
    pass

class AlarmWidget(QWidget):
    def __init__(self, alarm, active, parent=None):
        super(AlarmWidget, self).__init__(parent)
        self.setFixedHeight(250)
        self.setProperty("active", True)
        self._alarm = alarm
        self.mouseReleaseEvent = self._click_event

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(create_time(alarm.get_time(), active))
        layout.addWidget(create_days(alarm))

    def _click_event(self, _):
        ui.controller.UiController().set_screen("alarm_edit", edit_alarm=self._alarm)


def create_time(time, active):
    time_label = TimeWidget("{:0>2d}:{:0>2d}".format(time.hour, time.minute))
    time_label.setProperty("alarm_active", active)
    return time_label

def create_days(alarm):
    days = QWidget()
    day_layout = QHBoxLayout()
    days.setLayout(day_layout)
    for day in Alarm.Weekdays:
        day_widget = DayWidget(day[:3])
        day_widget.setProperty("active", alarm.is_day_active(day))
        day_layout.addWidget(day_widget)
    return days

class AddWidget(QLabel):
    def __init__(self, parent=None):
        super(AddWidget, self).__init__(parent)
        pixmap = QPixmap("ui/icons/add.png")
        self.setPixmap(pixmap.scaledToWidth(100))
        self.mouseReleaseEvent = _click_event

def _click_event(_):
    new_alarm = Alarm(0, 0, [], False, None, True)
    ui.controller.UiController().set_screen("alarm_edit", edit_alarm=new_alarm)
