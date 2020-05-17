import time
import threading

import PyQt5.QtWidgets
import PyQt5.QtGui
import PyQt5.QtCore


class Spinner(PyQt5.QtWidgets.QWidget):
    change_value = PyQt5.QtCore.pyqtSignal(str)

    def __init__(self, options, start_index=0, loop=True, underhang=True, parent=None):
        super(Spinner, self).__init__(parent)
        self._options = options
        self._loop = loop
        self._underhang = underhang
        self._focus_index = start_index
        self._offset = 0
        self._spacing = -1
        self._alignment = PyQt5.QtCore.Qt.AlignCenter

    def get_value(self):
        return self._options[self._focus_index]

    def sizeHint(self):
        font_size = self._get_font_height()
        return PyQt5.QtCore.QSize(self._get_min_option_width(), font_size * 1.5)

    def minimumSizeHint(self):
        return PyQt5.QtCore.QSize(self._get_min_option_width(), self._get_font_height())

    def mousePressEvent(self, e):
        self._timer = time.time()
        self._drag_start = self._true_drag_start = e.localPos().y()

    def mouseMoveEvent(self, e):
        self._update_offset(e.localPos().y() - self._drag_start)

    def mouseReleaseEvent(self, e):
        dt = time.time() - self._timer
        self._speed = (
            0.001 * (e.localPos().y() - self._true_drag_start) / (dt * dt * dt)
        )
        # Need to be threaded otherwise hogs main thread
        threading.Thread(target=self._decelerate).start()

    def paintEvent(self, _):
        painter = PyQt5.QtGui.QPainter(self)

        # border_rect = PyQt5.QtCore.QRect(0, 0, self.width(), self.height())
        # painter.drawRect(border_rect)

        if self._spacing == -1:
            self._spacing = self._get_font_height()

        underhang = 0
        if not self._underhang:
            underhang = self._get_font_height() * 0.12

        indices, center_index = self._get_focussed_indices()
        spinner_center = self.height() / 2
        for index in range(len(indices)):
            if indices[index] >= 0 and indices[index] < len(self._options):
                center = (
                    spinner_center
                    + (self._spacing * (index - center_index))
                    + self._offset
                    + underhang
                )
                text_rect = PyQt5.QtCore.QRect(
                    0, center - (self._spacing / 2), self.width(), self._spacing,
                )
                painter.drawText(
                    text_rect, self._alignment, self._options[indices[index]],
                )
        painter.end()

    @PyQt5.QtCore.pyqtProperty(int)
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, value):
        self._spacing = value

    @PyQt5.QtCore.pyqtProperty(str)
    def textalign(self):
        return str(self._alignment)

    @textalign.setter
    def textalign(self, value):
        if value == "left":
            self._alignment = PyQt5.QtCore.Qt.AlignLeft
        elif value == "right":
            self._alignment = PyQt5.QtCore.Qt.AlignRight
        else:
            self._alignment = PyQt5.QtCore.Qt.AlignCenter
        self._alignment += PyQt5.QtCore.Qt.AlignVCenter

    def _update_offset(self, offset):
        if abs(offset) > self._spacing / 2:
            half_point = 0.5 if offset > 0 else -0.5
            new_index = self._focus_index - int(offset / self._spacing + half_point)
            if self._loop or (new_index >= 0 and new_index < len(self._options)):
                self._focus_index = new_index % len(self._options)
                new_offset = int(offset / self._spacing + half_point) * self._spacing
                self._drag_start = self._drag_start + new_offset
                offset = offset - new_offset
                self.change_value.emit(self._options[self._focus_index])
            else:
                offset = self._offset
                self._speed = 0
        self._offset = offset
        self.update()

    def _decelerate(self):
        while abs(self._speed) > 0.5:
            time.sleep(0.01)
            self._update_offset(int(self._offset + self._speed))
            self._speed = self._speed / 1.1
        self._center_scroll()

    def _center_scroll(self):
        while abs(self._offset) > 1:
            time.sleep(0.01)
            self._update_offset(int(self._offset / 1.05))
        self._update_offset(0)

    def _get_focussed_indices(self):
        num_values = int(self.height() / self._spacing) + 2
        if num_values % 2 == 0:
            num_values += 1
        center_index = int((num_values - 1) / 2)
        focussed_indices = []
        for i in range(num_values):
            index = self._focus_index + i - center_index
            if self._loop:
                focussed_indices.append(index % len(self._options))
            else:
                focussed_indices.append(index)
        return focussed_indices, center_index

    def _get_font_height(self):
        pixel = self.font().pixelSize()
        if pixel == -1:
            return self.font().pointSize() * 4 / 3
        return pixel

    def _get_min_option_width(self):
        width = 0
        for option in self._options:
            if len(option) > width:
                width = len(option)
        return width * self._get_font_height() * 0.75
