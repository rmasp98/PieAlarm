import PyQt5.QtWidgets
import PyQt5.QtCore


class Slider(PyQt5.QtWidgets.QSlider):
    def __init__(self, alarm_manager, parent=None):
        super(Slider, self).__init__(PyQt5.QtCore.Qt.Horizontal, parent)
        self._alarm_manager = alarm_manager

    def mouseReleaseEvent(self, _):
        if self.value() != self.maximum():
            self.setValue(0)
        else:
            self._alarm_manager.stop()
