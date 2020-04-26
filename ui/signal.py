import PyQt5.QtCore


class ScreenSignal(PyQt5.QtCore.QObject):
    _signal = PyQt5.QtCore.pyqtSignal(object, object, bool)

    def __init__(self, slot, parent=None):
        super(ScreenSignal, self).__init__(parent)
        self._signal.connect(slot)

    def emit(self, screen, alarm, append_back):
        self._signal.emit(screen, alarm, append_back)
