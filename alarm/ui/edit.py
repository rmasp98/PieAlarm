import PyQt5.QtWidgets

import alarm.alarm
import alarm.ui.time
import alarm.ui.days
import alarm.ui.playback
import ui.widgets.toggle
import ui.controller
import utils.layout


class EditScreen(PyQt5.QtWidgets.QWidget):
    def __init__(self, alarm_manager, parent=None):
        super(EditScreen, self).__init__(parent)

        self._alarm_manager = alarm_manager
        self._alarm = alarm_manager.get_focused_alarm()

        self._set_layout(utils.layout.create_vertical_layout(self))
        ui.controller.UiController().enable_toolbar_edit(True, self._save, self._delete)

    def _set_layout(self, layout):
        h_widget = PyQt5.QtWidgets.QWidget()
        # TODO: bodge to get size right but still looks a bit shit
        h_widget.setMinimumHeight(200)
        h_layout = utils.layout.create_horizontal_layout(h_widget, layout)
        self._time_widget = alarm.ui.time.TimeEdit(
            self._alarm.get_time().hour, self._alarm.get_time().minute
        )
        h_layout.addWidget(self._time_widget)

        self._active_switch = ui.widgets.toggle.ToggleSwitch(self._alarm.is_active())
        h_layout.addWidget(self._active_switch)

        self._days_widget = alarm.ui.days.DaysWidget(self._alarm, True)
        layout.addWidget(self._days_widget)

        self._playback = alarm.ui.playback.PlaybackWidget(self._alarm.get_playback())
        layout.addWidget(self._playback)

    def _save(self, _):
        if self._days_widget.get_active_days():
            hour, minute = self._time_widget.get_time()
            new_alarm = alarm.alarm.Alarm(
                hour,
                minute,
                self._days_widget.get_active_days(),
                self._playback.get_playback(),
                self._active_switch.is_active(),
            )
            self._alarm_manager.remove_alarm(self._alarm)
            self._alarm_manager.create_alarm(new_alarm)
            ui.controller.UiController().set_screen("back")
        else:
            _day_message()

    def _delete(self, _):
        self._alarm_manager.remove_alarm(self._alarm)
        ui.controller.UiController().set_screen("back")


def _day_message():
    msg = PyQt5.QtWidgets.QMessageBox()
    msg.setIcon(PyQt5.QtWidgets.QMessageBox.Warning)
    msg.setText("Must select at least one day")
    msg.setStandardButtons(PyQt5.QtWidgets.QMessageBox.Ok)
    msg.exec_()
