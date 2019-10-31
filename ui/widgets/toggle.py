from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


class ToggleSwitch(QSlider):
    def __init__(self, active=True, parent=None):
        super(ToggleSwitch, self).__init__(Qt.Horizontal, parent)
        self.setMaximum(1)
        self._toggle(active)

    def _toggle(self, state):
        self.setProperty("active", state)
        self.setStyle(self.style())
        if state:
            self.setValue(1)
        else:
            self.setValue(0)

    def is_active(self):
        if self.value() == 1:
            return True
        else:
            return False

    def mouseReleaseEvent(self, _):
        if self.value() == 0:
            self._toggle(True)
        else:
            self._toggle(False)

    # These two are to prevent the slider from reacting on click
    def mouseMoveEvent(self, _):
        pass

    def mousePressEvent(self, _):
        pass
