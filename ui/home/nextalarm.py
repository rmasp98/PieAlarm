import datetime
import PyQt5.QtWidgets

import ui
import alarm.alarm
import ui.widgets.qtext
import ui.widgets.layout


class NextAlarm(PyQt5.QtWidgets.QWidget):
    def __init__(self, time, parent=None):
        super(NextAlarm, self).__init__(parent)

        layout = ui.widgets.layout.create_horizontal_layout(self)
        layout.addStretch()
        image = PyQt5.QtWidgets.QLabel()
        pixmap = PyQt5.QtGui.QPixmap("ui/icons/alarm.png")
        image.setPixmap(pixmap.scaledToWidth(35))
        layout.addWidget(image)

        self._text = ui.widgets.qtext.QText()
        layout.addWidget(self._text)
        layout.addStretch()

        self.set_time(time)
        self.mouseReleaseEvent = _click_event

    def set_time(self, time):
        if time is not None:
            now = datetime.datetime.now()
            if time.weekday() == now.weekday() and time.time() > now.time():
                self._text.setText(": {:0>2d}:{:0>2d}".format(time.hour, time.minute))
            elif time.weekday() == (now + datetime.timedelta(days=1)).weekday():
                self._text.setText(
                    ": Tomorrow {:0>2d}:{:0>2d}".format(time.hour, time.minute)
                )
            else:
                self._text.setText(
                    ": {} {:0>2d}:{:0>2d}".format(
                        alarm.alarm.Alarm.Weekdays[time.weekday()],
                        time.hour,
                        time.minute,
                    )
                )
        else:
            self._text.setText(": No Alarms")


def _click_event(_):
    ui.Ctrl().set_screen(ui.Screen.VIEW)
