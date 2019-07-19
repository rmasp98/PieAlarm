
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from ui.digital_clock import DigitalClock
from ui.weather_group import WeatherGroup


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.resize(1024, 600)
        self.setStyleSheet("""
        QMainWindow {
            border-image: url(ui/icons/landscape.jpg),
        }  
        """)
        self.setup_screen()

    def setup_screen(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        vert_layout = QVBoxLayout(main_widget)

        weather_group = WeatherGroup()
        vert_layout.addWidget(weather_group)

        clock = DigitalClock()
        vert_layout.addWidget(clock)

        placeholder = QLabel("Next Alarm:\n06:30")
        placeholder.setAlignment(Qt.AlignCenter)
        vert_layout.addWidget(placeholder)

    def set_weather(self, updates):
        self.findChild(WeatherGroup).update_group(updates)

    def set_dark(self):
        self.setStyleSheet("""
            background-color: black
        """)
        self.findChild(WeatherGroup).hide_weather()

    def unset_dark(self):
        self.setStyleSheet("""
        QMainWindow {
            border-image: url(ui/icons/landscape.jpg),
        }  
        """)
        self.findChild(WeatherGroup).show_weather()