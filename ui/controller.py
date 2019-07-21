

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
from ui.window import Window


class UiController():
    def __init__(self):
        self.app = QApplication([])
        self.window = Window()
        QFontDatabase.addApplicationFont("fonts/square_sans_serif_7.ttf")

    def exec(self):
        self.window.show()
        return self.app.exec_()
