import PyQt5.QtWidgets

from ui.widgets.spinner import Spinner
from ui.widgets.layout import create_horizontal_layout
from ui.widgets.text import FontSize


class TimeEdit(PyQt5.QtWidgets.QWidget):
    def __init__(self, hour=0, minute=0, parent=None):
        super(TimeEdit, self).__init__(parent)
        layout = create_horizontal_layout(self)

        layout.addStretch()
        self._hour = Spinner(
            ["{:0>2d}".format(i) for i in range(24)], start_index=hour, underhang=False
        )
        layout.addWidget(self._hour)
        self._minute = Spinner(
            ["{:0>2d}".format(i) for i in range(60)],
            start_index=minute,
            underhang=False,
        )
        layout.addWidget(self._minute)
        layout.addStretch()

    def get_time(self):
        return int(self._hour.get_value()), int(self._minute.get_value())
