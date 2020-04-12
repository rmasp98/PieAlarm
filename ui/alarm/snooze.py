import PyQt5.QtWidgets
import PyQt5.QtCore

import utils.layout
import utils.qtext
import ui.widgets.slider


class SnoozeScreen(PyQt5.QtWidgets.QWidget):
    def __init__(self, alarm_manager, parent=None):
        super(SnoozeScreen, self).__init__(parent)
        self._alarm_manager = alarm_manager
        self._set_layout()

    def _set_layout(self):
        layout = utils.layout.create_vertical_layout(self)

        snooze = SnoozeWidget("Snooze")
        snooze.mouseReleaseEvent = self._snooze_event
        layout.addWidget(snooze)

        stop = ui.widgets.slider.Slider(self._alarm_manager)
        # stop.mouseReleaseEvent = self._stop_event
        layout.addWidget(
            stop, alignment=PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignVCenter
        )

    def _snooze_event(self, _):
        self._alarm_manager.snooze(10)


class SnoozeWidget(utils.qtext.QText):
    pass
