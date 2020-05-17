import PyQt5.QtWidgets
import PyQt5.QtGui
import PyQt5.QtCore

import ui.controller
import light.light
import ui.widgets.time


class ToolBar(PyQt5.QtWidgets.QToolBar):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)
        self.setIconSize(PyQt5.QtCore.QSize(50, 50))
        self.setMovable(False)
        self._actions = {}

        self._actions["back"] = self.addAction(
            PyQt5.QtGui.QIcon("ui/icons/back.png"), "Back", _back_event
        )
        try:
            self._light_on = 0
            self._light = light.light.Light()
            self._actions["light"] = self.addAction(
                PyQt5.QtGui.QIcon("ui/icons/light.png"), "Light", self._light_event
            )
        except:
            print("Could not create light button as no mote device found")

        self.addWidget(StretchWidget())
        self._clock = self.addWidget(
            ui.widgets.time.Time(ui.widgets.text.FontSize.MEDIUM)
        )

        self.addWidget(StretchWidget())
        self._actions["save"] = self.addAction(
            PyQt5.QtGui.QIcon("ui/icons/save.png"), "Save"
        )
        self._actions["delete"] = self.addAction(
            PyQt5.QtGui.QIcon("ui/icons/delete.png"), "Delete"
        )
        self._actions["settings"] = self.addAction(
            PyQt5.QtGui.QIcon("ui/icons/settings.png"), "Settings", _settings_event
        )

    def enable_action(self, action, enable=True, event=None):
        if action in self._actions:
            self._actions[action].setVisible(enable)
            if event is not None:
                self._actions[action].triggered.connect(event)
            elif action == "back":
                self._actions[action].triggered.connect(_back_event)
            elif action == "light":
                self._actions[action].triggered.connect(self._light_event)

    def enable_clock(self, enable):
        self._clock.setVisible(enable)

    def _light_event(self):
        self._light_on = (self._light_on + 1) % 4
        self._light.set_warm(self._light_on / 3)


class StretchWidget(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(StretchWidget, self).__init__(parent)
        self.setSizePolicy(
            PyQt5.QtWidgets.QSizePolicy.Expanding, PyQt5.QtWidgets.QSizePolicy.Expanding
        )


def _back_event():
    ui.Ctrl().back()


def _settings_event():
    ui.Ctrl().set_screen(ui.Screen.SETTINGS)
