
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from ui.weather_widget import WeatherWidget


class WeatherGroup(QWidget):
    def __init__(self, parent=None):
        super(WeatherGroup, self).__init__(parent)
        self.weather_units = [WeatherWidget() for i in range(5)]
        self.UpdateGroup([(21, "sunny") for i in range(5)])


    def UpdateGroup(self, updates):
        layout = QHBoxLayout()
        for weather, update in zip(self.weather_units, updates):
            weather.Set(update[0], update[1])
            layout.addWidget(weather)

        self.setLayout(layout)
