
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore    import Qt
from ui.clock import DigitalClock
from ui.weather import WeatherGroup


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.resize(1024, 600)
        # self.showFullScreen()
        self.setup_screen()
        self.setProperty("darkTheme", False)
        self.setStyleSheet(open("ui/theme.qss").read())
        self.setCursor(Qt.BlankCursor)

    def setup_screen(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        vert_layout = QVBoxLayout(main_widget)
        vert_layout.addWidget(WeatherGroup())
        vert_layout.addWidget(DigitalClock())
        vert_layout.addWidget(QLabel("Next Alarm:\n06:30"))

    def update_weather(self, updates):
        self.findChild(WeatherGroup).update_all(updates)

    def set_theme(self, theme):
        if theme == "Default":
            self.setProperty("darkTheme", False)
            self.findChild(WeatherGroup).show_weather(True)
        elif theme == "Dark":
            self.setProperty("darkTheme", True)
            self.findChild(WeatherGroup).show_weather(False)

        self.setStyle(self.style())
