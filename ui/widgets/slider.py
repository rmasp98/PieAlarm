import PyQt5.QtWidgets
import PyQt5.QtCore


class Slider(PyQt5.QtWidgets.QSlider):
    def __init__(self, func, parent=None):
        super(Slider, self).__init__(PyQt5.QtCore.Qt.Horizontal, parent)
        self._func = func
        self.setPageStep(0)

    def mouseReleaseEvent(self, _):
        if self.value() != self.maximum():
            self.setValue(0)
        else:
            self._func()
