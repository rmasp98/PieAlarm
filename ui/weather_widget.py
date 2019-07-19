
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

icons = {"sunny":"ui/icons/sun.png", "none":"ui/icons/no_weather.png"}


class WeatherWidget(QWidget):
    def __init__(self, parent=None):
        super(WeatherWidget, self).__init__(parent)
        # self.set(22, "sunny")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap(icons["none"])
        icon = QLabel()
        icon.setObjectName("icon")
        icon.setAlignment(Qt.AlignCenter)
        icon.setPixmap(pixmap.scaledToWidth(100))
        layout.addWidget(icon)

        temp = QLabel("0")
        temp.setObjectName("temperature")
        temp.setAlignment(Qt.AlignCenter)
        layout.addWidget(temp)

        self.setLayout(layout)

    def set(self, temp, weather):
        pixmap = QPixmap(icons[weather])
        self.findChild(QLabel, "icon").setPixmap(pixmap.scaledToWidth(100))
        self.findChild(QLabel, "temperature").setText(str(temp))
