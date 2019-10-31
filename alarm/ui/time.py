import PyQt5.QtWidgets

import ui.widgets.spinner
import utils.layout


class TimeEdit(PyQt5.QtWidgets.QWidget):
    def __init__(self, hour=0, minute=0, parent=None):
        super(TimeEdit, self).__init__(parent)
        layout = utils.layout.create_horizontal_layout(self)

        layout.addStretch()
        self._hour = ui.widgets.spinner.Spinner(0, 24, hour)
        layout.addWidget(self._hour)
        self._minute = ui.widgets.spinner.Spinner(0, 60, minute)
        layout.addWidget(self._minute)
        layout.addStretch()

    def get_time(self):
        return self._hour.get_value(), self._minute.get_value()
