from PyQt5.QtWidgets import QMainWindow

import ui.main.screen as MainUI
import ui.toolbar


class Window(QMainWindow):
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
        self._disable_weather()

    def set_central_widget(self, widget):
        self.setCentralWidget(widget)
        self._disable_weather()

    def enable_toolbar_edit(self, enable, save_event, delete_event):
        self._toolbar.enable_edit(enable, save_event, delete_event)

    def _disable_weather(self):
        main_screen = self.findChild(MainUI.Screen)
        if main_screen is not None:
            if self._theme == "dark":
                main_screen.show_weather(False)
            else:
                main_screen.show_weather(True)
