import collections
import PyQt5.QtCore

import ui
from ui.home import home
from ui.alarm import view
from ui.alarm import edit
from ui.alarm import snooze
from ui.settings import SettingsScreen
from ui.player import player


class UiController:
    class _UiController:
        def __init__(self):
            self._screen_signal = ScreenSignal(self._set_screen)
            self._screen = None
            self._last_screen = collections.deque(maxlen=10)

        def init(self, app, window, alarm_manager, weather, player, settings):
            self._app = app
            self._window = window
            self._alarm_manager = alarm_manager
            self._weather = weather
            self._player = player
            self._settings = settings
            self._settings.emit_all()

        def set_theme(self, theme):
            self._window.set_theme(theme)

        def set_screen(self, screen, alarm=None, append_back=True):
            self._screen_signal.emit(screen, alarm, append_back)

        def _set_screen(self, screen, alarm, append_back):
            self._set_default_toolbar()
            if screen == ui.Screen.HOME:
                self.enable_toolbar_clock(False)
                new_screen = home.HomeScreen(self._alarm_manager, self._weather)
            elif screen == ui.Screen.VIEW:
                new_screen = view.ViewScreen(self._alarm_manager)
            elif screen == ui.Screen.EDIT:
                new_screen = edit.EditScreen(alarm, self._alarm_manager)
            elif screen == ui.Screen.SNOOZE:
                new_screen = snooze.SnoozeScreen(self._alarm_manager)
            elif screen == ui.Screen.SETTINGS:
                new_screen = SettingsScreen(self._settings)
            elif screen == ui.Screen.PLAYER:
                new_screen = player.PlayerScreen(self._player)

            if append_back:
                self._last_screen.append(self._screen)
            self._screen = screen
            self._window.set_central_widget(new_screen)

        def back(self):
            if self._last_screen:
                self.set_screen(self._last_screen.pop(), append_back=False)

        def enable_toolbar_action(self, action, enable=True, event=None):
            self._window.enable_toolbar_action(action, enable, event)

        def enable_toolbar_clock(self, enable):
            self._window.enable_toolbar_clock(enable)

        def enable_keyboard(self, enable=True):
            return self._window.enable_keyboard(enable)

        def exec(self, screen=ui.Screen.HOME, theme="default"):
            self.set_screen(screen, append_back=False)
            self.set_theme(theme)

            self._window.show()
            self._app.exec_()
            self._alarm_manager.reset()
            self._weather.kill()

        def _set_default_toolbar(self):
            self.enable_toolbar_clock(True)
            self.enable_toolbar_action("save", False)
            self.enable_toolbar_action("delete", False)
            self.enable_toolbar_action("back")
            self.enable_toolbar_action("light", False)
            self.enable_toolbar_action("settings", False)
            self.enable_keyboard(False)

    _instance = None

    def __init__(self):
        if not UiController._instance:
            UiController._instance = UiController._UiController()

    def __getattr__(self, name):
        return getattr(self._instance, name)


class ScreenSignal(PyQt5.QtCore.QObject):
    _signal = PyQt5.QtCore.pyqtSignal(object, object, bool)

    def __init__(self, slot, parent=None):
        super(ScreenSignal, self).__init__(parent)
        self._signal.connect(slot)

    def emit(self, screen, alarm, append_back):
        self._signal.emit(screen, alarm, append_back)
