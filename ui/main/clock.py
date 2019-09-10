
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QLabel


class DigitalClock(QLabel):
    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)

        self.show_time()

    def show_time(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        self.setText(text)
