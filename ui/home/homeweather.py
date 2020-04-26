import datetime
import PyQt5.QtWidgets
import PyQt5.QtGui

import weather.darksky
import utils.layout
import utils.qtext

icons = [
    "ui/icons/weather/no_weather.png",
    "ui/icons/weather/sun.png",
    "ui/icons/weather/night.png",
    "ui/icons/weather/rainy.png",
    "ui/icons/weather/snowy.png",
    "ui/icons/weather/sleet.png",
    "ui/icons/weather/windy.png",
    "ui/icons/weather/fog.png",
    "ui/icons/weather/cloudy.png",
    "ui/icons/weather/partly-cloudy.png",
    "ui/icons/weather/night-cloudy.png",
]


class Icon(PyQt5.QtWidgets.QWidget):
    def __init__(self, image, temp, time, size=50, parent=None):
        super(Icon, self).__init__(parent)
        self._image = icons[image]
        self._temp = int(temp)
        self._time = time.strftime("%-I%p")
        self._size = size

    def sizeHint(self):
        return PyQt5.QtCore.QSize(self._size, self._size + 25)

    def change(self, image, temp, time):
        self._image = icons[image]
        self._temp = int(temp)
        self._time = time.strftime("%-I%p")
        self.update()

    def paintEvent(self, _):
        painter = PyQt5.QtGui.QPainter(self)

        image_rect = PyQt5.QtCore.QRect(0, 0, self._size, self._size)
        image = PyQt5.QtGui.QImage()
        image.load(self._image)
        painter.drawImage(image_rect, image)
        painter.drawText(image_rect, PyQt5.QtCore.Qt.AlignCenter, str(self._temp))

        time_rect = PyQt5.QtCore.QRect(0, self._size, self._size, 25)
        painter.drawText(time_rect, PyQt5.QtCore.Qt.AlignCenter, self._time)

        painter.end()


class Widget(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        layout = utils.layout.create_vertical_layout(self)

        icon = Icon(10, 99, datetime.datetime.now(), 100)
        icon.setObjectName("icon")
        layout.addWidget(icon)

    def update(self, weather, temperature, time):
        self.findChild(Icon, "icon").change(weather, temperature, time)


class Group(PyQt5.QtWidgets.QWidget):
    def __init__(self, weather, num_widgets=5, parent=None):
        super(Group, self).__init__(parent)
        self._weather = weather

        layout = utils.layout.create_horizontal_layout(self)
        for _ in range(num_widgets):
            layout.addSpacerItem(utils.layout.create_spacer())
            layout.addWidget(Widget())
        layout.addSpacerItem(utils.layout.create_spacer())

        timer = PyQt5.QtCore.QTimer(self)
        timer.timeout.connect(self.update_all)
        timer.start(900000)
        self.update_all()

    def update_all(self):
        try:
            # updates = weather.darksky.Darksky().get_weather("Guildford").data
            # for widget, key in zip(self.findChildren(Widget), sorted(updates)[0::3]):
            #     widget.update(updates[key].w_type, updates[key].feel_temp, key)
            for widget, updates in zip(
                self.findChildren(Widget), self._weather.get_short_weather()
            ):
                widget.update(updates.w_type, updates.temp, updates.time)
        except:
            for widget in self.findChildren(Widget):
                widget.update(0, 99, datetime.datetime.now())

    def show_weather(self, is_show):
        for weather in self.findChildren(Widget):
            if is_show:
                weather.show()
            else:
                weather.hide()
