import PyQt5.QtWidgets
import PyQt5.QtGui
import PyQt5.QtCore

import ui.controller
import utils.qtext
import light.light
import ui.home.clock


class ToolBar(PyQt5.QtWidgets.QToolBar):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)
        self.setIconSize(PyQt5.QtCore.QSize(50, 50))
        self.setMovable(False)

        self.addAction(PyQt5.QtGui.QIcon("ui/icons/back.png"), "Back", _back_event)
        try:
            self._light_on = 0
            self._light = light.light.Light()
            self.addAction(
                PyQt5.QtGui.QIcon("ui/icons/light.png"), "Light", self._light_event
            )
        except:
            print("Could not create light button as no mote device found")

        self.addWidget(StretchWidget())
        self._clock = self.addWidget(ui.home.clock.DigitalClock(30))

        self.addWidget(StretchWidget())
        self._save = self.addAction(PyQt5.QtGui.QIcon("ui/icons/save.png"), "Save")
        self._delete = self.addAction(
            PyQt5.QtGui.QIcon("ui/icons/delete.png"), "Delete"
        )

    def enable_edit(self, enable, save_event=None, delete_event=None):
        self._save.setVisible(enable)
        if save_event is not None:
            self._save.triggered.connect(save_event)

        self._delete.setVisible(enable)
        if delete_event is not None:
            self._delete.triggered.connect(delete_event)

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
    ui.controller.UiController().back()
