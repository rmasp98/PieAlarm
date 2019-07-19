
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from ui.weather_widget import WeatherWidget


class WeatherGroup(QWidget):
    def __init__(self, parent=None):
        super(WeatherGroup, self).__init__(parent)

        layout = QHBoxLayout()
        for i in range(5):
            layout.addWidget(WeatherWidget())

        self.setLayout(layout)

    def update_group(self, updates):
        for weather, update in zip(self.findChildren(WeatherWidget), updates):
            weather.set(update[0], update[1])

    def hide_weather(self):
        for weather in self.findChildren(WeatherWidget):
            weather.hide()

    def show_weather(self):
        for weather in self.findChildren(WeatherWidget):
            weather.show()