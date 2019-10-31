import PyQt5.QtWidgets
import PyQt5.QtGui

import utils.layout

icons = {"sunny": "ui/icons/sun.png", "none": "ui/icons/no_weather.png"}


class WeatherWidget(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WeatherWidget, self).__init__(parent)
        layout = utils.layout.create_vertical_layout(self)

        pixmap = PyQt5.QtGui.QPixmap(icons["none"])
        icon = PyQt5.QtWidgets.QLabel()
        icon.setObjectName("icon")
        icon.setPixmap(pixmap.scaledToWidth(100))
        layout.addWidget(icon)

        temp = PyQt5.QtWidgets.QLabel("0")
        temp.setObjectName("temperature")
        layout.addWidget(temp)

    def update(self, temperature, weather):
        pixmap = PyQt5.QtGui.QPixmap(icons[weather])
        self.findChild(PyQt5.QtWidgets.QLabel, "icon").setPixmap(
            pixmap.scaledToWidth(100)
        )
        self.findChild(PyQt5.QtWidgets.QLabel, "temperature").setText(str(temperature))


class WeatherGroup(PyQt5.QtWidgets.QWidget):
    def __init__(self, num_widgets=5, parent=None):
        super(WeatherGroup, self).__init__(parent)

        layout = utils.layout.create_horizontal_layout(self)
        for _ in range(num_widgets):
            layout.addWidget(WeatherWidget())

    def update_all(self, updates):
        for weather, update in zip(self.findChildren(WeatherWidget), updates):
            weather.update(update[0], update[1])

    def show_weather(self, is_show):
        for weather in self.findChildren(WeatherWidget):
            if is_show:
                weather.show()
            else:
                weather.hide()
