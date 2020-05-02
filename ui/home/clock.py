import PyQt5.QtCore
import PyQt5.QtWidgets
import PyQt5.QtGui

import ui.widgets.qtext
import ui.widgets.layout


class DigitalClock(ui.widgets.qtext.QText):
    def __init__(self, font_size, parent=None):
        super(DigitalClock, self).__init__(parent)
        font = self.font()
        font.setPixelSize(font_size)
        self.setFont(font)

        timer = PyQt5.QtCore.QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)

        self.show_time()

    # TODO: should probably convert this to datetime
    def show_time(self):
        time = PyQt5.QtCore.QTime.currentTime()
        self.setText(time.toString("hh:mm"))
