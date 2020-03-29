import collections
import PyQt5.QtWidgets
import PyQt5.QtGui
import PyQt5.QtCore

import ui.window
import ui.home.home as Home
import alarm.manager
import alarm.alarm
import ui.alarm.view as AlarmView
import ui.alarm.edit as AlarmEdit
import ui.alarm.snooze as AlarmSnooze


class UiController:
    class _UiController:
        def __init__(self, screen, theme):
            self._app = PyQt5.QtWidgets.QApplication([])
            self._window = ui.window.Window()
            PyQt5.QtGui.QFontDatabase.addApplicationFont(
                "ui/fonts/square_sans_serif_7.ttf"
            )

            self._alarm_manager = alarm.manager.Manager()
            self._screen_signal = ScreenSignal(self._set_screen)
            self._screen = ""
            self._last_screen = collections.deque(maxlen=10)
            self._focus_alarm = None

            self.set_screen(screen, False)
            self.set_theme(theme)

        def set_theme(self, theme):
            self._window.set_theme(theme)

        def set_screen(self, screen, append_last_screen=True, edit_alarm=None):
            # if edit_alarm is not None:
            self._alarm_manager.set_focused_alarm(edit_alarm)
            self._screen_signal.emit(screen, append_last_screen)

        def enable_toolbar_edit(self, enable, save_event, delete_event):
            self._window.enable_toolbar_edit(enable, save_event, delete_event)

        def _set_screen(self, screen, append_back):
            if screen in screens:
                self.enable_toolbar_edit(False, None, None)
                if append_back:
                    self._last_screen.append(self._screen)
                self._screen = screen
                self._window.set_central_widget(screens[screen](self._alarm_manager))
            elif screen == "back":
                if self._last_screen:
                    self.set_screen(self._last_screen.pop(), False)

        def exec(self):
            self._window.show()
            self._app.exec_()
            self._alarm_manager.reset()

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
    "main": Home.HomeScreen,
    "alarm_edit": AlarmEdit.EditScreen,
    "alarm_view": AlarmView.ViewScreen,
    "snooze": AlarmSnooze.SnoozeScreen,
}
