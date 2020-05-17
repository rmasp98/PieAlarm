import typing

import PyQt5.QtWidgets
import PyQt5.QtCore

import ui
from scheduler.observer import Observer


class LineEdit(PyQt5.QtWidgets.QLineEdit):
    def __init__(self, label="", parent=None):
        super(LineEdit, self).__init__(label, parent)
        self._keyboard = None

    def focusInEvent(self, e):
        super(LineEdit, self).focusInEvent(e)
        self._keyboard = ui.Ctrl().enable_keyboard()
        self._keyboard.connect(self._keyboard_edit)

    def focusOutEvent(self, e):
        super(LineEdit, self).focusOutEvent(e)
        if self._keyboard is not None:
            self._keyboard.close()

    def _keyboard_edit(self, key):
        if key != "Back":
            self.insert(key)
        else:
            self.backspace()


def edit(key, lineedit):
    if key != "Back":
        lineedit.insert(key)
    else:
        lineedit.backspace()


def _get_font_size(widget):
    font_size = widget.font().pixelSize()
    if font_size == -1:
        font_size = widget.font().pointSize() * 4 / 3
    return font_size


class Keyboard(PyQt5.QtWidgets.QDockWidget):
    _signal = Observer()

    def __init__(self, parent=None):
        super(Keyboard, self).__init__(parent)
        self.setFeatures(PyQt5.QtWidgets.QDockWidget.NoDockWidgetFeatures)

        self._key_values = [
            [
                CharKey("q", "0"),
                CharKey("w", "1"),
                CharKey("e", "2"),
                CharKey("r", "3"),
                CharKey("t", "4"),
                CharKey("y", "5"),
                CharKey("u", "6"),
                CharKey("i", "7"),
                CharKey("o", "8"),
                CharKey("p", "9"),
            ],
            [
                CharKey("a", "@"),
                CharKey("s", "#"),
                CharKey("e", "£"),
                CharKey("f", "_"),
                CharKey("g", "&"),
                CharKey("h", "-"),
                CharKey("j", "+"),
                CharKey("k", "("),
                CharKey("l", ")"),
            ],
            [
                ShiftKey(),
                CharKey("z", '"'),
                CharKey("x", ":"),
                CharKey("c", ";"),
                CharKey("v", "!"),
                CharKey("b", "?"),
                CharKey("n", "="),
                CharKey("m", "%"),
                DeleteKey(),
            ],
            [AltKey(), CharKey("/", "\\"), SpaceKey(), CharKey(".", ","), CloseKey()],
        ]
        v_widget = PyQt5.QtWidgets.QWidget()
        self.setWidget(v_widget)
        v_layout = PyQt5.QtWidgets.QVBoxLayout(v_widget)
        v_layout.addStretch()
        for row in self._key_values:
            row_widget = PyQt5.QtWidgets.QWidget()
            row_layout = PyQt5.QtWidgets.QHBoxLayout()
            row_widget.setLayout(row_layout)
            row_layout.addStretch()
            for key in row:
                row_layout.addWidget(key)
                if (
                    isinstance(key, CharKey)
                    or isinstance(key, DeleteKey)
                    or isinstance(key, SpaceKey)
                ):
                    key.connect(self._emit)
                elif isinstance(key, ShiftKey):
                    key.connect(self._shift_event)
                elif isinstance(key, AltKey):
                    key.connect(self._alt_event)
                elif isinstance(key, CloseKey):
                    key.connect(self.close)
            row_layout.addStretch()
            v_layout.addWidget(row_widget)
        v_layout.addStretch()

    def connect(self, function):
        self._signal.subscribe(function)

    def reset(self):
        self._signal.reset()

    def _emit(self, key):
        self.findChild(ShiftKey).unshift()
        self._shift_event()
        self._signal.notify(key)

    def _shift_event(self):
        caps = self.findChild(ShiftKey).is_capitalised()
        for key in self.findChildren(CharKey):
            key.capitalise(caps)

    def _alt_event(self):
        self.findChild(ShiftKey).unshift(True)
        for key in self.findChildren(CharKey):
            key.toggle_alt()


class Key(PyQt5.QtWidgets.QLabel):
    _signal = _signal = PyQt5.QtCore.pyqtSignal()

    def __init__(self, label="", parent=None):
        super(Key, self).__init__(label, parent)

    def connect(self, function):
        self._signal.connect(function)

    def mouseReleaseEvent(self, _):
        self._signal.emit()


class CharKey(Key):
    _signal = PyQt5.QtCore.pyqtSignal(str)

    def __init__(self, main, alt, parent=None):
        super(CharKey, self).__init__(parent)
        self._main = self._current = main
        self._alt = alt
        self._caps = False
        self._alt_active = False
        self.setText(self._current)

    def capitalise(self, caps):
        self._caps = caps
        if not self._alt_active:
            if self._caps:
                self._current = self._main.capitalize()
            else:
                self._current = self._main
        self.setText(self._current)

    def toggle_alt(self):
        self._alt_active = not self._alt_active
        if self._alt_active:
            self._current = self._alt
        else:
            self._current = self._main
        self.setText(self._current)

    def mouseReleaseEvent(self, _):
        self._signal.emit(self._current)

    def sizeHint(self):
        font_size = _get_font_size(self)
        return PyQt5.QtCore.QSize(font_size * 2, font_size * 1.5)


class ShiftKey(Key):
    def __init__(self, parent=None):
        super(ShiftKey, self).__init__(parent)
        self._shift_index = 0
        self._shift_pixmaps = [
            PyQt5.QtGui.QPixmap("ui/icons/unshift.png"),
            PyQt5.QtGui.QPixmap("ui/icons/shift.png"),
            PyQt5.QtGui.QPixmap("ui/icons/shift_lock.png"),
        ]

    def sizeHint(self):
        font_size = _get_font_size(self)
        return PyQt5.QtCore.QSize(font_size, font_size)

    def paintEvent(self, e):
        painter = PyQt5.QtGui.QPainter(self)
        size, x_offset, y_offset = (
            (self.width(), 0, (self.height() - self.width()) / 2)
            if self.width() < self.height()
            else (self.height(), (self.width() - self.height()) / 2, 0)
        )
        rect = PyQt5.QtCore.QRect(x_offset, y_offset, size, size)
        painter.drawPixmap(rect, self._shift_pixmaps[self._shift_index])
        painter.end()

    def unshift(self, reset=False):
        if reset or self._shift_index == 1:
            self._shift_index = 0
            self.update()

    def is_capitalised(self, unshift=False):
        if self._shift_index == 0:
            return False
        return True

    def mouseReleaseEvent(self, _):
        self._shift_index = (self._shift_index + 1) % len(self._shift_pixmaps)
        self.update()
        self._signal.emit()


class DeleteKey(Key):
    _signal = PyQt5.QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(DeleteKey, self).__init__(parent)
        self._pixmap = PyQt5.QtGui.QPixmap("ui/icons/delete_key.png")

    def sizeHint(self):
        font_size = _get_font_size(self)
        return PyQt5.QtCore.QSize(font_size, font_size)

    def paintEvent(self, e):
        painter = PyQt5.QtGui.QPainter(self)
        size, x_offset, y_offset = (
            (self.width(), 0, (self.height() - self.width()) / 2)
            if self.width() < self.height()
            else (self.height(), (self.width() - self.height()) / 2, 0)
        )
        rect = PyQt5.QtCore.QRect(x_offset, y_offset, size, size)
        painter.drawPixmap(rect, self._pixmap)
        painter.end()

    def mouseReleaseEvent(self, _):
        self._signal.emit("Back")


class AltKey(Key):
    _letters = "ABC"
    _symbols = "?123"

    def __init__(self, parent=None):
        super(AltKey, self).__init__(self._symbols, parent)

    def mouseReleaseEvent(self, _):
        if self.text() == self._symbols:
            self.setText(self._letters)
        else:
            self.setText(self._symbols)
        super(AltKey, self).mouseReleaseEvent(None)


class SpaceKey(Key):
    _signal = PyQt5.QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(SpaceKey, self).__init__("Space", parent)

    def mouseReleaseEvent(self, _):
        self._signal.emit(" ")

    def sizeHint(self):
        font_size = _get_font_size(self)
        return PyQt5.QtCore.QSize(font_size * 12, font_size)

    def paintEvent(self, _):
        painter = PyQt5.QtGui.QPainter(self)
        path = PyQt5.QtGui.QPainterPath()
        y_offset = self.height() * 0.25
        rect = PyQt5.QtCore.QRectF(0, y_offset, self.width(), self.height() / 2)
        path.addRoundedRect(rect, 10, 10)
        painter.fillPath(path, self.palette().color(self.foregroundRole()))
        painter.drawPath(path)
        painter.end()


class CloseKey(Key):
    def __init__(self, parent=None):
        super(CloseKey, self).__init__(parent)
        self._pixmap = PyQt5.QtGui.QPixmap("ui/icons/down.png")

    def sizeHint(self):
        font_size = _get_font_size(self)
        return PyQt5.QtCore.QSize(font_size, font_size)

    def paintEvent(self, e):
        painter = PyQt5.QtGui.QPainter(self)
        size, x_offset, y_offset = (
            (self.width(), 0, (self.height() - self.width()) / 2)
            if self.width() < self.height()
            else (self.height(), (self.width() - self.height()) / 2, 0)
        )
        rect = PyQt5.QtCore.QRect(x_offset, y_offset, size, size)
        painter.drawPixmap(rect, self._pixmap)
        painter.end()
