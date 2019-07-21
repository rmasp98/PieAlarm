
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap


icons = {"sunny":"ui/icons/sun.png", "none":"ui/icons/no_weather.png"}


class WeatherWidget(QWidget):
    def __init__(self, parent=None):
        super(WeatherWidget, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        pixmap = QPixmap(icons["none"])
        icon = QLabel()
        icon.setObjectName("icon")
        icon.setPixmap(pixmap.scaledToWidth(100))
        layout.addWidget(icon)

        temp = QLabel("0")
        temp.setObjectName("temperature")
        layout.addWidget(temp)

    def update(self, temperature, weather):
        pixmap = QPixmap(icons[weather])
        self.findChild(QLabel, "icon").setPixmap(pixmap.scaledToWidth(100))
        self.findChild(QLabel, "temperature").setText(str(temperature))


class WeatherGroup(QWidget):
    def __init__(self, parent=None):
        super(WeatherGroup, self).__init__(parent)

        layout = QHBoxLayout()
        for _ in range(5):
            layout.addWidget(WeatherWidget())
        self.setLayout(layout)

    def update_all(self, updates):
        for weather, update in zip(self.findChildren(WeatherWidget), updates):
            weather.update(update[0], update[1])

    def show_weather(self, is_show):
        for weather in self.findChildren(WeatherWidget):
            if is_show:
                weather.show()
            else:
                weather.hide()
