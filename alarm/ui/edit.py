
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTimeEdit

from alarm.alarm import Alarm
from alarm.ui.widget import *


class EditScreen(QWidget):

    def __init__(self, alarm, parent=None):
        super(EditScreen, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(create_time(alarm.get_time(), True))
        layout.addWidget(create_days(alarm))

        




#Need to display:
# - time
# - days
# - repeat
# - playback
# - name
# - active
