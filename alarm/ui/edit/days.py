
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from alarm.alarm import Alarm

class DaysEdit(QWidget):

    def __init__(self, alarm, parent=None):
        super(DaysEdit, self).__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)

        self._days = {}
        for day in Alarm.Weekdays:
            day_widget = DayWidget(day[:3], True)
            day_widget.set_active(alarm.is_day_active(day))
            layout.addWidget(day_widget)
            self._days[day] = day_widget

    def get_active_days(self):
        return_days = set()
        for day, widget in self._days.items():
            if widget.is_active():
                return_days.add(day)
        return return_days


class DayWidget(QLabel):

    def __init__(self, text="", clickable=False, parent=None):
        super(DayWidget, self).__init__(text, parent)
        if clickable:
            self.mouseReleaseEvent = self._click_event

        self.setMinimumSize(50, 50)

    def set_active(self, active):
        self.setProperty("active", active)
        self.setStyle(self.style())

    def is_active(self):
        return self.property("active")

    def _click_event(self, _):
        self.set_active(not self.is_active())
