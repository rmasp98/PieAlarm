
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFontDatabase, QFont, QColor




class DigitalClock(QLabel):
    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)

        QFontDatabase.addApplicationFont("fonts/square_sans_serif_7.ttf")
        font = QFont()
        font.setPointSize(100)
        font.setFamily("square_sans_serif_7")
        self.setFont(font)
        self.setAlignment(Qt.AlignCenter)
        # self.setStyleSheet("border: 1px inset grey")

        self.show_time()

    def show_time(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        self.setText(text)
