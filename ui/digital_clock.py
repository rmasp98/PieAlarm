
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFontDatabase, QFont

class DigitalClock(QLabel):
    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        # self.setSegmentStyle(QLCDNumber.Filled)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.showTime()
        QFontDatabase.addApplicationFont("fonts/square_sans_serif_7.ttf")
        font = QFont()
        font.setPointSize(75)
        font.setFamily("square_sans_serif_7")
        self.setFont(font)

        self.resize(15, 6)

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        # if (time.second() % 2) == 0:
        #     text = text[:2] + ' ' + text[3:]

        self.setText(text)