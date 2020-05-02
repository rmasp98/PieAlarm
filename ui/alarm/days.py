import PyQt5.QtWidgets
import PyQt5.QtCore

import ui.widgets.layout
import ui.widgets.qtext
import alarm.alarm


class DaysWidget(PyQt5.QtWidgets.QWidget):
    def __init__(self, days, clickable=False, parent=None):
        super(DaysWidget, self).__init__(parent)
        layout = ui.widgets.layout.create_horizontal_layout(self)

        self._days = {}
        for day in alarm.alarm.Alarm.Weekdays:
            day_widget = DayLabel(day[:3], clickable)
            if day in days:
                day_widget.set_active(True)
            layout.addWidget(day_widget)
            self._days[day] = day_widget

    def get_active_days(self):
        return_days = set()
        for day, widget in self._days.items():
            if widget.is_active():
                return_days.add(day)
        return return_days


class DayLabel(ui.widgets.qtext.QText):
    def __init__(self, text, clickable=False, parent=None):
        super(DayLabel, self).__init__(text, parent)
        self.setSizePolicy(
            PyQt5.QtWidgets.QSizePolicy.Preferred, PyQt5.QtWidgets.QSizePolicy.Preferred
        )
        self.setProperty("highlight", clickable)
        if clickable:
            self.mouseReleaseEvent = self._click_event

    def sizeHint(self):
        return PyQt5.QtCore.QSize(50, 50)

    def minimumSizeHint(self):
        return PyQt5.QtCore.QSize(25, 50)

    def set_active(self, active):
        self.setProperty("active", active)
        self.setStyle(self.style())

    def is_active(self):
        return self.property("active")

    def _click_event(self, _):
        self.set_active(not self.is_active())
