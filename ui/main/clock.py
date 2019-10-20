
import PyQt5.QtCore
import PyQt5.QtWidgets


class DigitalClock(PyQt5.QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        timer = PyQt5.QtCore.QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)

        self.show_time()

    # TODO: should probably convert this to datetime
    def show_time(self):
        time = PyQt5.QtCore.QTime.currentTime()
        text = time.toString('hh:mm')
        self.setText(text)
