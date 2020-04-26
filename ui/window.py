import PyQt5.QtWidgets
import PyQt5.QtCore
import PyQt5.QtGui

import ui.toolbar


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

        self._toolbar = ui.toolbar.ToolBar()
        self.addToolBar(PyQt5.QtCore.Qt.BottomToolBarArea, self._toolbar)

    def set_theme(self, theme):
        self.setProperty("theme", theme)
        self.setStyle(self.style())
        self._theme = theme

    def set_central_widget(self, widget):
        self.setCentralWidget(widget)

    def enable_toolbar_edit(self, enable, save_event, delete_event):
        self._toolbar.enable_edit(enable, save_event, delete_event)

    def enable_toolbar_clock(self, enable):
        self._toolbar.enable_clock(enable)
