
from PyQt5.QtWidgets import QMainWindow


class Window(QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setFixedSize(1024, 600)
        # self.showFullScreen()
        self.setProperty("darkTheme", False)
        self.setStyleSheet(open("ui/theme.qss").read())
        # self.setCursor(Qt.BlankCursor)

    def set_theme(self, theme):
        self.setProperty("theme", theme)
        self.setStyle(self.style())
