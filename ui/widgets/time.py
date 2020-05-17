import PyQt5.QtCore
import PyQt5.QtWidgets
import PyQt5.QtGui
import datetime

import ui.widgets.layout
import ui.widgets.text


class Time(ui.widgets.text.Text):
    def __init__(self, font_size, parent=None):
        super(Time, self).__init__(size=font_size, parent=parent)

        timer = PyQt5.QtCore.QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)

        self.show_time()

    def show_time(self):
        time = datetime.datetime.now()
        self.setText(time.strftime("%H:%M"))
