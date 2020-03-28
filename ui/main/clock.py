import PyQt5.QtCore
import PyQt5.QtWidgets

import utils.qtext
import utils.layout


class DigitalClock(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        timer = PyQt5.QtCore.QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)

        layout = utils.layout.create_horizontal_layout(self)
        layout.addSpacerItem(utils.layout.create_spacer())
        self._text = utils.qtext.QText()
        layout.addWidget(self._text)
        layout.addSpacerItem(utils.layout.create_spacer())

        self.show_time()

    # TODO: should probably convert this to datetime
    def show_time(self):
        time = PyQt5.QtCore.QTime.currentTime()
        self._text.setText(time.toString("hh:mm"))
