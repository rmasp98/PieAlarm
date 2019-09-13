
from PyQt5.QtWidgets import QMainWindow, QLabel, QToolBar
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt

import ui.main.screen as MainUI
import ui.controller

class Window(QMainWindow):

    def __init__(self, theme="default", parent=None):
        super(Window, self).__init__(parent)
        self.setFixedSize(1024, 600)
        # self.showFullScreen()
        self.setProperty("theme", "default")
        self.setStyleSheet(open("ui/theme.qss").read())
        # self.setCursor(Qt.BlankCursor)
        self._theme = theme

        toolbar = QToolBar()
        toolbar.addWidget(BackButton())
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

    def set_theme(self, theme):
        self.setProperty("theme", theme)
        self.setStyle(self.style())
        self._theme = theme
        self._disable_weather()

    def set_central_widget(self, widget):
        self.setCentralWidget(widget)
        self._disable_weather()

    def _disable_weather(self):
        main_screen = self.findChild(MainUI.Screen)
        if main_screen is not None:
            if self._theme == "dark":
                main_screen.show_weather(False)
            else:
                main_screen.show_weather(True)


class BackButton(QLabel):

    def __init__(self, parent=None):
        super(BackButton, self).__init__(parent)
        pixmap = QPixmap("ui/icons/back.png")
        self.setPixmap(pixmap.scaledToWidth(50))
        self.mouseReleaseEvent = _click_event

def _click_event(_):
    ui.controller.UiController().set_screen("back")
