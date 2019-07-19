

from PyQt5.QtWidgets import QApplication
from ui.window import Window


class UiController():
    def __init__(self):
        self.app = QApplication([])
        self.window = Window()

    def exec(self):
        self.window.show()
        return self.app.exec_()
