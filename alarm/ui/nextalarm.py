import datetime
import PyQt5.QtWidgets

import ui.controller
import alarm.alarm
import utils.qtext


class NextAlarm(utils.qtext.QText):
    def __init__(self, time, parent=None):
        super(NextAlarm, self).__init__(parent)
        self.set_time(time)
        self.mouseReleaseEvent = _click_event

    def set_time(self, time):
        if time is not None:
            now = datetime.datetime.now()
            if time.weekday() == now.weekday() and time.time() > now.time():
                self.setText(
                    "Next Alarm:\n" + "{:0>2d}:{:0>2d}".format(time.hour, time.minute)
                )
            elif time.weekday() == (now + datetime.timedelta(days=1)).weekday():
                self.setText(
                    "Next Alarm:\n"
                    + "Tomorrow {:0>2d}:{:0>2d}".format(time.hour, time.minute)
                )
            else:
                self.setText(
                    "Next Alarm:\n"
                    + "{} {:0>2d}:{:0>2d}".format(
                        alarm.alarm.Alarm.Weekdays[time.weekday()],
                        time.hour,
                        time.minute,
                    )
                )
        else:
            self.setText("No Alarms")


def _click_event(_):
    ui.controller.UiController().set_screen("alarm_view")
