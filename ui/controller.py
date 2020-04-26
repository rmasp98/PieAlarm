import collections

import ui
from ui import signal
from ui.home import home
from ui.alarm import view
from ui.alarm import edit
from ui.alarm import snooze


class UiController:
    class _UiController:
        def __init__(self):
            self._screen_signal = signal.ScreenSignal(self._set_screen)
            self._screen = None
            self._last_screen = collections.deque(maxlen=10)

        def init(self, app, window, alarm_manager, weather):
            self._app = app
            self._window = window
            self._alarm_manager = alarm_manager
            self._weather = weather

        def set_theme(self, theme):
            self._window.set_theme(theme)

        def set_screen(self, screen, alarm=None, append_back=True):
            self._screen_signal.emit(screen, alarm, append_back)

        def _set_screen(self, screen, alarm, append_back):
            self.enable_toolbar_clock(True)
            self.enable_toolbar_edit(False, None, None)
            if screen == ui.Screen.HOME:
                self.enable_toolbar_clock(False)
                new_screen = home.HomeScreen(self._alarm_manager, self._weather)
            elif screen == ui.Screen.VIEW:
                new_screen = view.ViewScreen(self._alarm_manager)
            elif screen == ui.Screen.EDIT:
                new_screen = edit.EditScreen(alarm, self._alarm_manager)
            elif screen == ui.Screen.SNOOZE:
                new_screen = snooze.SnoozeScreen(self._alarm_manager)

            if append_back:
                self._last_screen.append(self._screen)
            self._screen = screen
            self._window.set_central_widget(new_screen)

        def back(self):
            if self._last_screen:
                self.set_screen(self._last_screen.pop(), append_back=False)

        def enable_toolbar_edit(self, enable, save_event, delete_event):
            self._window.enable_toolbar_edit(enable, save_event, delete_event)

        def enable_toolbar_clock(self, enable):
            self._window.enable_toolbar_clock(enable)

        def exec(self, screen=ui.Screen.HOME, theme="default"):
            self.set_screen(screen, append_back=False)
            self.set_theme(theme)

            self._window.show()
            self._app.exec_()
            self._alarm_manager.reset()
            self._weather.kill()

    instance = None

    def __init__(self):
        if not UiController.instance:
            UiController.instance = UiController._UiController()

    def __getattr__(self, name):
        return getattr(self.instance, name)
