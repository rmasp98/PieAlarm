import datetime

import PyQt5.QtWidgets

import alarm.alarm
import ui
import ui.alarm.time
import ui.alarm.days
import ui.alarm.playback
import ui.widgets.toggle
import ui.widgets.layout


class EditScreen(PyQt5.QtWidgets.QWidget):
    def __init__(self, alarm, alarm_manager, parent=None):
        super(EditScreen, self).__init__(parent)
        self._alarm_manager = alarm_manager
        self._edit_alarm = alarm

        if self._edit_alarm is not None:
            self._set_layout(
                ui.widgets.layout.create_vertical_layout(self),
                self._edit_alarm.time(),
                self._edit_alarm.active_days(),
                self._edit_alarm.is_active(),
                self._edit_alarm.playback(),
            )
        else:
            self._set_layout(
                ui.widgets.layout.create_vertical_layout(self),
                datetime.time(0, 0),
                {},
                True,
                None,
            )
        ui.controller.UiController().enable_toolbar_action("save", event=self._save)
        ui.controller.UiController().enable_toolbar_action("delete", event=self._delete)

    def _set_layout(self, layout, time, days, active, playback):
        h_widget = PyQt5.QtWidgets.QWidget()
        h_layout = ui.widgets.layout.create_horizontal_layout(h_widget, layout)
        self._time_widget = ui.alarm.time.TimeEdit(time.hour, time.minute)
        h_layout.addWidget(self._time_widget)

        self._active_switch = ui.widgets.toggle.ToggleSwitch(active)
        h_layout.addWidget(self._active_switch)

        self._days_widget = ui.alarm.days.DaysWidget(days, True)
        self._days_widget.setMaximumHeight(75)
        layout.addWidget(self._days_widget)

        self._playback = ui.alarm.playback.PlaybackWidget(playback)
        layout.addWidget(self._playback)

    def _save(self, _):
        try:
            hour, minute = self._time_widget.get_time()
            new_alarm = alarm.alarm.Alarm(
                hour,
                minute,
                self._days_widget.get_active_days(),
                self._playback.get_playback(),
                self._active_switch.is_active(),
            )
            self._alarm_manager.remove_alarm(self._edit_alarm)
            self._alarm_manager.create_alarm(new_alarm)
            ui.Ctrl().back()
        except Exception as err:
            _error_message(str(err))

    def _delete(self, _):
        self._alarm_manager.remove_alarm(self._edit_alarm)
        ui.Ctrl().back()


def _error_message(message):
    msg = PyQt5.QtWidgets.QMessageBox()
    msg.setIcon(PyQt5.QtWidgets.QMessageBox.Warning)
    msg.setText(message)
    msg.setStandardButtons(PyQt5.QtWidgets.QMessageBox.Ok)
    msg.exec_()
