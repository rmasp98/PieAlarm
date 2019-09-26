
import time
import threading

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QSize, QRect, Qt

#TODO: make movement based on acceleration

class Spinner(QWidget):
    def __init__(self, minimum=0, maximum=100, start=0, parent=None):
        if minimum > maximum or not minimum <= start < maximum:
            raise ValueError("Minimum lager than maximum or start not beteen minimum and maximum")

        super(Spinner, self).__init__(parent)
        self._offset = 0
        self._spacing = 150
        self._drag_start = 0

        self._value = self._start_value = start
        self._mod = maximum - minimum
        self._min = minimum

        self.setMinimumSize(200, 100)

    def get_value(self):
        return self._value

    def sizeHint(self):
        return QSize(200, 200)

    def mousePressEvent(self, e):
        self._drag_start = e.localPos().y()
        self._start_value = self._value

    def mouseMoveEvent(self, e):
        offset = e.localPos().y() - self._drag_start
        if abs(offset) > self._spacing/2:
            half_point = 0.5 if offset > 0 else -0.5
            self._value = self._get_bounded_value(\
                self._value - int(offset/self._spacing + half_point))
            self._drag_start = self._drag_start +\
                int(offset/self._spacing + half_point) * self._spacing
            offset = e.localPos().y() - self._drag_start
        self._update_offset(offset)

    def mouseReleaseEvent(self, _):
        # Need to be threaded otherwise hogs main thread
        threading.Thread(target=self._center_scroll).start()

    def paintEvent(self, _):
        painter = QPainter(self)

        num_values = self._get_num_rendered_values()

        font_size = self.font().pixelSize()
        centre = int(self.height()/2)-font_size/2
        start_pos = centre - self._spacing * int(num_values/2)

        for i in range(num_values):
            rect = QRect(int(painter.device().width()/2)-50,\
                start_pos + i*self._spacing + self._offset, 150, 100)
            # TODO: format should be based on size of maximum and minimum
            painter.drawText(rect, Qt.AlignCenter,\
                "{:0>2d}".format(self._get_bounded_value(self._value - int(num_values/2) + i)))
        painter.end()

    def _get_bounded_value(self, value):
        return (value - self._min) % self._mod + self._min

    def _update_offset(self, offset):
        self._offset = offset
        self.update()

    def _center_scroll(self):
        while abs(self._offset) > 1:
            time.sleep(0.01)
            self._update_offset(int(self._offset/1.05))
        self._update_offset(0)

    def _get_num_rendered_values(self):
        num_values = int(self.height()/self._spacing)
        if num_values % 2 == 0: # Always force odd number
            num_values = num_values + 1
        if num_values == 1: # Always render at least a number both sides of value
            num_values = 3
        return num_values
