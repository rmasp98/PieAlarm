
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFontDatabase, QFont

class DigitalClock(QLabel):
    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        QFontDatabase.addApplicationFont("fonts/square_sans_serif_7.ttf")
        font = QFont()
        font.setPointSize(75)
        font.setFamily("square_sans_serif_7")
        self.setFont(font)
        self.setAlignment(Qt.AlignCenter)
        # self.setStyleSheet("border: 1px inset grey")

        self.showTime()

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        self.setText(text)
