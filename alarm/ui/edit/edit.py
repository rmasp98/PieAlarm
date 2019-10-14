
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QMessageBox

from alarm.alarm import Alarm
from alarm.ui.edit.time import TimeEdit
from alarm.ui.edit.days import DaysEdit
from alarm.ui.edit.playback import PlaybackWidget
from ui.widgets.toggle import ToggleSwitch
import ui.controller

class EditScreen(QWidget):

    def __init__(self, alarm_manager, parent=None):
        super(EditScreen, self).__init__(parent)

        self._alarm_manager = alarm_manager
        self._alarm = alarm_manager.get_focused_alarm()

        layout = QVBoxLayout()
        self.setLayout(layout)

        h_widget = QWidget()
        h_layout = QHBoxLayout()
        h_widget.setLayout(h_layout)
        self._time_widget = TimeEdit(self._alarm.get_time().hour, self._alarm.get_time().minute)
        h_layout.addWidget(self._time_widget)

        self._active_switch = ToggleSwitch()
        h_layout.addWidget(self._active_switch)

        layout.addWidget(h_widget)

        h_widget2 = QWidget()
        h_layout2 = QHBoxLayout()
        h_widget2.setLayout(h_layout2)

        self._days_widget = DaysEdit(self._alarm)
        h_layout2.addWidget(self._days_widget, 2)

        self._repeat = QCheckBox("Repeat")
        self._repeat.setChecked(self._alarm.is_repeating())
        h_layout2.addWidget(self._repeat)
        layout.addWidget(h_widget2)

        self._playback = PlaybackWidget(self._alarm.get_playback())
        layout.addWidget(self._playback)

        ui.controller.UiController().enable_toolbar_edit(True, self._save, self._delete)

    def _save(self, _):
        if self._days_widget.get_active_days():
            hour, minute = self._time_widget.get_time()
            new_alarm = Alarm(
                hour, minute, self._days_widget.get_active_days(), self._repeat.isChecked(),\
                self._playback.get_playback()
            )
            self._alarm_manager.remove_alarm(self._alarm)
            self._alarm_manager.create_alarm(new_alarm)
            ui.controller.UiController().set_screen("back")
        else:
            _day_message()

    def _cancel(self):
        ui.controller.UiController().set_screen("back")

    def _delete(self, _):
        self._alarm_manager.remove_alarm(self._alarm)
        ui.controller.UiController().set_screen("back")


def _day_message():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Must select at least one day")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
