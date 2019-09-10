

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
import PyQt5.QtCore

import ui.window
import ui.main.screen as MainUI
import alarm.manager
import alarm.alarm
import alarm.ui.view as AlarmView
import alarm.ui.edit as AlarmEdit
import alarm.ui.snooze as AlarmSnooze


class Signal(PyQt5.QtCore.QObject):
    _signal = PyQt5.QtCore.pyqtSignal(str)
    def __init__(self, slot, parent=None):
        super(Signal, self).__init__(parent)
        self._signal.connect(slot)

    def emit(self, screen, alarm=None):
        self._signal.emit(screen)



class UiController():
    instance = None

    def __init__(self):
        if not UiController.instance:
            UiController.instance = UiController._UiController()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class _UiController():

        def __init__(self):
            self._app = QApplication([])
            self._window = ui.window.Window()
            QFontDatabase.addApplicationFont("fonts/square_sans_serif_7.ttf")
            self._alarm_manager = alarm.manager.Manager()
            create_alarms(self._alarm_manager)
            self._screen = "main"
            self.set_theme("default")
            self.screen_signal = Signal(self._set_screen)
        
        def test(self):
            pass

        def set_theme(self, theme):
            self._window.set_theme(theme)
            self._theme = theme
            self._set_screen(self._screen)

        def _set_screen(self, screen, edit_alarm=None):
            print("hello")
            if screen == "main":
                self._screen = screen
                self._window.setCentralWidget(\
                    MainUI.Screen(self._alarm_manager.get_next_alarm_time()))
                if self._theme == "default":
                    self._window.findChild(MainUI.Screen).show_weather(True)
                elif self._theme == "dark":
                    self._window.findChild(MainUI.Screen).show_weather(False)
            elif screen == "alarm_edit" and alarm is not None:
                self._screen = screen
                self._window.setCentralWidget(AlarmEdit.EditScreen(edit_alarm))
            elif screen == "alarm_view":
                self._screen = screen
                self._window.setCentralWidget(AlarmView.ViewScreen(self._alarm_manager))
            elif screen == "snooze":
                self._screen = screen
                self._window.setCentralWidget(AlarmSnooze.SnoozeScreen(self._alarm_manager))    

        def exec(self):
            self._window.show()
            self._app.exec_()
            self._alarm_manager._scheduler._remove_all_jobs()


# Temporary until we get everything working
def create_alarms(manager):
    alarms = [
        alarm.alarm.Alarm(19, 4, ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],\
             True, {"type":"basic", "track":"song.wav"}),\
        alarm.alarm.Alarm(7, 30, ["Saturday", "Sunday"], True, {"type":"basic",\
             "track":"song.wav"})
    ]

    i = 0
    for new_alarm in alarms:
        manager.create_alarm("test" + str(i), new_alarm)
        i = i + 1
