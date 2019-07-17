

from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.digital_clock import DigitalClock


class UiController():
    def __init__(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.window.resize(1024, 600)
        #window.showFullScreen()
        self.SetupScreen()


    def exec(self):
        self.window.show()
        return self.app.exec_()

    def SetupScreen(self):
        self.window.setCentralWidget(DigitalClock())
