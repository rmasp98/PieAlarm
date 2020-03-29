import PyQt5.QtWidgets

import ui.toolbar


class Window(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, theme="default", parent=None):
        super(Window, self).__init__(parent)
        self.setFixedSize(800, 480)
        # self.showFullScreen()
        # self.setCursor(Qt.BlankCursor)
        self.setProperty("theme", "default")
        self.setStyleSheet(open("ui/theme.qss").read())
        self._theme = theme

        self._toolbar = ui.toolbar.ToolBar()
        self.addToolBar(self._toolbar)

    def set_theme(self, theme):
        self.setProperty("theme", theme)
        self.setStyle(self.style())
        self._theme = theme

    def set_central_widget(self, widget):
        self.setCentralWidget(widget)

    def enable_toolbar_edit(self, enable, save_event, delete_event):
        self._toolbar.enable_edit(enable, save_event, delete_event)
