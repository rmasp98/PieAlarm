from enum import Enum

import PyQt5.QtWidgets
import PyQt5.QtGui
import PyQt5.QtCore


class FontSize(Enum):
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"
    EXTRALARGE = "XL"


class Text(PyQt5.QtWidgets.QLabel):
    def __init__(self, text="", size=FontSize.MEDIUM, underhang=True, parent=None):
        super(Text, self).__init__(text, parent)
        self.setProperty("fontsize", size.value)
        self._underhang = underhang

    def sizeHint(self):
        if self._underhang:
            return super(Text, self).sizeHint()
        else:
            return PyQt5.QtCore.QSize(
                super(Text, self).sizeHint().width(), self.font().pixelSize() * 0.80
            )

    def paintEvent(self, e):
        if self._underhang:
            super(Text, self).paintEvent(e)
        else:
            painter = PyQt5.QtGui.QPainter(self)
            font = self.font()
            offset = font.pixelSize() * 0.2
            text_rect = PyQt5.QtCore.QRect(0, 0, self.width(), self.height() + offset)
            painter.drawText(text_rect, PyQt5.QtCore.Qt.AlignCenter, self.text())
            painter.end()
