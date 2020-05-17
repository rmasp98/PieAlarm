import datetime
import PyQt5.QtWidgets
import PyQt5.QtGui

import weather.darksky
import ui.widgets.layout
import ui.widgets.text

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
    def __init__(
        self, image=0, temp=99, time=datetime.datetime.now(), width=100, parent=None
    ):
        super(Icon, self).__init__(parent)
        self._image = icons[image]
        self._temp = int(temp)
        self._time = time.strftime("%-I%p")
        self._width = width
        self._hide = False

    def sizeHint(self):
        return PyQt5.QtCore.QSize(self._width, self._width + 25)

    def change(self, image, temp, time):
        self._image = icons[image]
        self._temp = int(temp)
        self._time = time.strftime("%-I%p")
        self.update()

    def hide(self, hide):
        self._hide = hide

    def paintEvent(self, _):
        painter = PyQt5.QtGui.QPainter(self)

        if not self._hide:
            image_rect = PyQt5.QtCore.QRect(0, 0, self._width, self._width)
            image = PyQt5.QtGui.QImage()
            image.load(self._image)
            painter.drawImage(image_rect, image)
            painter.drawText(image_rect, PyQt5.QtCore.Qt.AlignCenter, str(self._temp))

            time_rect = PyQt5.QtCore.QRect(0, self._width, self._width, 25)
            painter.drawText(time_rect, PyQt5.QtCore.Qt.AlignCenter, self._time)

        painter.end()


class Group(PyQt5.QtWidgets.QWidget):
    def __init__(self, weather, num_widgets=5, update_period_sec=900, parent=None):
        super(Group, self).__init__(parent)
        self._weather = weather

        layout = ui.widgets.layout.create_horizontal_layout(self)
        for _ in range(num_widgets):
            layout.addSpacerItem(ui.widgets.layout.create_spacer())
            layout.addWidget(Icon())
        layout.addSpacerItem(ui.widgets.layout.create_spacer())

        timer = PyQt5.QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(update_period_sec * 1000)
        self.update()

    def update(self):
        try:
            for icon, updates in zip(
                self.findChildren(Icon), self._weather.get_short_weather()
            ):
                icon.hide(False)
                icon.change(updates.w_type, updates.temp, updates.time)
        except:
            for icon in self.findChildren(Icon):
                icon.hide(True)
