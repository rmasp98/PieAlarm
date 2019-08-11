
from PyQt5.QtWidgets import QLabel

class NextAlarm(QLabel):
    def __init__(self, parent=None):
        super(NextAlarm, self).__init__(parent)
        self.setText("Next Alarm:\n06:30")