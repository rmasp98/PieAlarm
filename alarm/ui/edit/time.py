
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from ui.widgets.spinner import Spinner

class TimeEdit(QWidget):

    def __init__(self, hour=0, minute=0, parent=None):
        super(TimeEdit, self).__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addStretch()
        self._hour = Spinner(0, 24, hour)
        layout.addWidget(self._hour)
        self._minute = Spinner(0, 60, minute)
        layout.addWidget(self._minute)
        layout.addStretch()

    def get_time(self):
        return self._hour.get_value(), self._minute.get_value()
