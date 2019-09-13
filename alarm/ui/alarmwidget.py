
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from alarm.alarm import Alarm

class DayWidget(QLabel):
    pass

class TimeWidget(QLabel):
    pass

class AlarmWidget(QWidget):
    def __init__(self, name, alarm, active, parent=None):
        super(AlarmWidget, self).__init__(parent)
        self.setFixedHeight(250)
        self.setProperty("active", True)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel(name))
        layout.addWidget(create_time(alarm.get_time(), active))
        layout.addWidget(create_days(alarm))


def create_time(time, active):
    time_label = TimeWidget(str(time.hour) + ":" + str(time.minute))
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
