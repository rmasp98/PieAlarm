
import collections
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

class UiController():
    
    class _UiController():

        def __init__(self, screen="main", theme="default"):
            self._app = QApplication([])
            self._window = ui.window.Window()
            QFontDatabase.addApplicationFont("fonts/square_sans_serif_7.ttf")
            self._alarm_manager = alarm.manager.Manager()
            self._screen_signal = ScreenSignal(self._set_screen)
            self._screen = ""
            self._last_screen = collections.deque(maxlen=10)

            # TODO: Remove when edit screen/database complete
            create_alarms(self._alarm_manager)

            self.set_screen(screen, False)
            self.set_theme(theme)


        def set_theme(self, theme):
            self._window.set_theme(theme)

        def set_screen(self, screen, append_last_screen=True):
            self._screen_signal.emit(screen, append_last_screen)

        def _set_screen(self, screen, append_back):
            if screen in screens:
                if append_back:
                    self._last_screen.append(self._screen)
                self._screen = screen
                self._window.set_central_widget(screens[screen](self._alarm_manager))
            elif screen == "back":
                if self._last_screen:
                    self.set_screen(self._last_screen.pop(), False)
            # elif screen == "alarm_edit" and edit_alarm in self._alarm_manager.get_alarms():
            #     self._screen = screen
            #     self._window.setCentralWidget(AlarmEdit.EditScreen(\
            #         self._alarm_manager.get_alarms()[edit_alarm]))

        def exec(self):
            self._window.show()
            self._app.exec_()
            self._alarm_manager._scheduler._remove_all_jobs()


    instance = None

    def __init__(self, screen="main", theme="default"):
        if not UiController.instance:
            UiController.instance = UiController._UiController(screen, theme)

    def __getattr__(self, name):
        return getattr(self.instance, name)


class ScreenSignal(PyQt5.QtCore.QObject):
    _signal = PyQt5.QtCore.pyqtSignal(str, bool)
    def __init__(self, slot, parent=None):
        super(ScreenSignal, self).__init__(parent)
        self._signal.connect(slot)

    def emit(self, screen, append_back):
        self._signal.emit(screen, append_back)

screens = {
    "main": MainUI.Screen,
    "alarm_edit": AlarmEdit.EditScreen,
    "alarm_view": AlarmView.ViewScreen,
    "snooze": AlarmSnooze.SnoozeScreen
}


# Temporary until we get everything working
def create_alarms(manager):
    # pass
    manager.create_alarm("Work", alarm.alarm.Alarm(21, 10, ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],\
             True, {"type":"basic", "track":"song.wav"}))
    manager.create_alarm("Weekend", alarm.alarm.Alarm(7, 30, ["Saturday", "Sunday"],\
             True, {"type":"basic", "track":"song.wav"}))
