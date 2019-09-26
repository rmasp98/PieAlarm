
from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QScroller
from PyQt5.QtCore import Qt

from alarm.ui.widgets import AlarmWidget, AddWidget

class ViewScreen(QWidget):
    def __init__(self, alarm_manager, parent=None):
        super(ViewScreen, self).__init__(parent)

        grid = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignTop)
        grid.setLayout(grid_layout)

        i = 0
        for alarm in alarm_manager.get_alarms():
            grid_layout.addWidget(AlarmWidget(alarm, True), i/2, i % 2)
            i = i + 1
        grid_layout.addWidget(AddWidget(), i/2, i % 2)

        scroll = QScrollArea(self)
        scroll.setWidget(grid)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(600)
        scroll.setFixedWidth(1024)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        QScroller.grabGesture(
            scroll.viewport(), QScroller.LeftMouseButtonGesture
        )
