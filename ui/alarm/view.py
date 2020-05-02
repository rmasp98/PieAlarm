import PyQt5.QtWidgets
import PyQt5.QtCore
import PyQt5.QtGui


import alarm.alarm
import ui
import ui.alarm.days
import ui.widgets.layout
import ui.widgets.qtext


class ViewScreen(PyQt5.QtWidgets.QWidget):
    def __init__(self, alarm_manager, parent=None):
        super(ViewScreen, self).__init__(parent)
        self._set_grid(alarm_manager)
        self._set_scrollarea()

    def _set_scrollarea(self):
        scroll = PyQt5.QtWidgets.QScrollArea(self)
        scroll.setWidget(self._grid)
        scroll.setWidgetResizable(True)
        # TODO: figure out how to fill window
        scroll.setFixedHeight(480)
        scroll.setFixedWidth(800)
        scroll.setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAlwaysOff)
        PyQt5.QtWidgets.QScroller.grabGesture(
            scroll.viewport(), PyQt5.QtWidgets.QScroller.LeftMouseButtonGesture
        )

    def _set_grid(self, alarm_manager):
        self._grid = PyQt5.QtWidgets.QWidget()
        grid_layout = ui.widgets.layout.create_grid_layout(self._grid)
        grid_layout.setAlignment(PyQt5.QtCore.Qt.AlignTop)

        i = 0
        for view_alarm in alarm_manager.get_alarms():
            grid_layout.addWidget(
                AlarmWidget(view_alarm, view_alarm.is_active()), i / 2, i % 2
            )
            i = i + 1
        grid_layout.addWidget(AddWidget(), i / 2, i % 2)


class AlarmWidget(PyQt5.QtWidgets.QWidget):
    def __init__(self, view_alarm, active, parent=None):
        super(AlarmWidget, self).__init__(parent)
        self.setFixedHeight(250)
        self.setProperty("active", True)
        self._alarm = view_alarm
        self.mouseReleaseEvent = self._click_event

        layout = ui.widgets.layout.create_vertical_layout(self)
        layout.addWidget(create_time(view_alarm.time(), active))
        layout.addWidget(ui.alarm.days.DaysWidget(view_alarm.active_days()))

    def _click_event(self, _):
        ui.Ctrl().set_screen(ui.Screen.EDIT, alarm=self._alarm)


def create_time(time, active):
    time_label = TimeWidget("{:0>2d}:{:0>2d}".format(time.hour, time.minute))
    time_label.setProperty("alarm_active", active)
    return time_label


class AddWidget(ui.widgets.qtext.QText):
    def __init__(self, parent=None):
        super(AddWidget, self).__init__(parent)
        pixmap = PyQt5.QtGui.QPixmap("ui/icons/add.png")
        self.setPixmap(pixmap.scaledToWidth(100))
        self.mouseReleaseEvent = _click_event


def _click_event(_):
    ui.Ctrl().set_screen(ui.Screen.EDIT, alarm=None)


class TimeWidget(ui.widgets.qtext.QText):
    pass
