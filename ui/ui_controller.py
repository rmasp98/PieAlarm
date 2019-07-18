

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from ui.digital_clock import DigitalClock
from ui.weather_group import WeatherGroup

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
        main_widget = QWidget()
        self.window.setCentralWidget(main_widget)

        vert_layout = QVBoxLayout(main_widget)

        weather_group = WeatherGroup()
        vert_layout.addWidget(weather_group)

        clock = DigitalClock()
        vert_layout.addWidget(clock)

        placeholder = QLabel("Next Alarm:\n06:30")
        placeholder.setAlignment(Qt.AlignCenter)
        vert_layout.addWidget(placeholder)
