import PyQt5.QtWidgets
import PyQt5.QtCore

from ui.widgets.layout import create_vertical_layout
from ui.widgets.text import Text
from ui.widgets.text import FontSize
import ui.widgets.slider


class SnoozeScreen(PyQt5.QtWidgets.QWidget):
    def __init__(self, alarm_manager, parent=None):
        super(SnoozeScreen, self).__init__(parent)
        self._alarm_manager = alarm_manager
        ui.Ctrl().enable_toolbar_action("back", False)
        self._set_layout()

    def _set_layout(self):
        layout = create_vertical_layout(self)

        snooze = Text("Snooze", FontSize.EXTRALARGE)
        snooze.mouseReleaseEvent = self._snooze_event
        layout.addWidget(snooze)

        stop = ui.widgets.slider.Slider(self._alarm_manager.stop)
        layout.addWidget(
            stop, alignment=PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignVCenter
        )

    def _snooze_event(self, _):
        self._alarm_manager.snooze()
