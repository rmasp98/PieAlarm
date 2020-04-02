import PyQt5.QtWidgets
import PyQt5.QtGui

import ui.controller
import utils.qtext
import light.light


class ToolBar(PyQt5.QtWidgets.QToolBar):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)
        self.setMaximumHeight(50)

        layout = PyQt5.QtWidgets.QHBoxLayout()
        tb_widget = PyQt5.QtWidgets.QWidget()
        tb_widget.setLayout(layout)

        layout.addWidget(BackButton())
        # layout.addWidget(LightButton())
        layout.addStretch()
        layout.addWidget(SaveButton())
        layout.addWidget(DeleteButton())
        layout.setContentsMargins(0, 0, 0, 0)

        self.setMovable(False)
        self.addWidget(tb_widget)

        self.enable_edit(False)

    def enable_edit(self, enable, save_event=None, delete_event=None):
        if enable:
            self.findChild(SaveButton).show()
            self.findChild(SaveButton).mouseReleaseEvent = save_event
            self.findChild(DeleteButton).show()
            self.findChild(DeleteButton).mouseReleaseEvent = delete_event
        else:
            self.findChild(SaveButton).hide()
            self.findChild(DeleteButton).hide()


class BackButton(PyQt5.QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(BackButton, self).__init__(parent)
        pixmap = PyQt5.QtGui.QPixmap("ui/icons/back.png")
        self.setPixmap(pixmap.scaledToWidth(50))
        self.mouseReleaseEvent = _back_event


def _back_event(_):
    ui.controller.UiController().set_screen("back")


class LightButton(PyQt5.QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(LightButton, self).__init__(parent)
        self._light_on = 0
        self._light = light.light.Light()
        pixmap = PyQt5.QtGui.QPixmap("ui/icons/light.png")
        self.setPixmap(pixmap.scaledToWidth(50))
        self.mouseReleaseEvent = self._light_event

    def _light_event(self, _):
        self._light_on = (self._light_on + 1) % 4
        self._light.set_warm(self._light_on / 3)


class SaveButton(PyQt5.QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(SaveButton, self).__init__(parent)
        pixmap = PyQt5.QtGui.QPixmap("ui/icons/save.png")
        self.setPixmap(pixmap.scaledToWidth(40))


class DeleteButton(PyQt5.QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(DeleteButton, self).__init__(parent)
        pixmap = PyQt5.QtGui.QPixmap("ui/icons/delete.png")
        self.setPixmap(pixmap.scaledToWidth(40))
