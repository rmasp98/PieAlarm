import PyQt5.QtWidgets
import PyQt5.QtCore
import PyQt5.QtGui

import ui.toolbar
from ui.keyboard import Keyboard


class Window(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, theme="default", parent=None):
        super(Window, self).__init__(parent)
        PyQt5.QtGui.QFontDatabase.addApplicationFont("ui/fonts/square_sans_serif_7.ttf")
        self.setFixedSize(800, 480)
        # self.showFullScreen()
        self.setCursor(PyQt5.QtCore.Qt.BlankCursor)
        self.setProperty("theme", "default")
        self.setStyleSheet(open("ui/theme.qss").read())
        self._theme = theme

        self._keyboard = Keyboard()
        self.addDockWidget(
            PyQt5.QtCore.Qt.BottomDockWidgetArea, self._keyboard,
        )
        self._keyboard.hide()

        self._toolbar = ui.toolbar.ToolBar()
        self.addToolBar(PyQt5.QtCore.Qt.BottomToolBarArea, self._toolbar)

    def set_theme(self, theme):
        self.setProperty("theme", theme)
        self.setStyle(self.style())
        self._theme = theme

    def set_central_widget(self, widget):
        self.setCentralWidget(widget)

    def enable_toolbar_action(self, action, enable=True, event=None):
        self._toolbar.enable_action(action, enable, event)

    def enable_toolbar_clock(self, enable):
        self._toolbar.enable_clock(enable)

    def enable_keyboard(self, enable=True):
        if enable:
            self._keyboard.reset()
            self._keyboard.show()
            return self._keyboard
        else:
            self._keyboard.hide()
