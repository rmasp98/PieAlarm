import PyQt5.QtWidgets
import PyQt5.QtCore

from ui.player.controls import Controls


class PlayerScreen(PyQt5.QtWidgets.QWidget):
    def __init__(self, player, parent=None):
        super(PlayerScreen, self).__init__(parent)
        self._player = player

        v_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        self._image = PyQt5.QtWidgets.QLabel("Image")
        self._image.setFixedSize(200, 200)
        v_layout.addWidget(self._image)

        self._track = PyQt5.QtWidgets.QLabel("Track")
        v_layout.addWidget(self._track)
        self._artist = PyQt5.QtWidgets.QLabel("Artist")
        v_layout.addWidget(self._artist)

        self._track_pos = PyQt5.QtWidgets.QSlider(PyQt5.QtCore.Qt.Horizontal)
        v_layout.addWidget(self._track_pos)

        controls = Controls(player)
        v_layout.addWidget(controls)

    def _play_and_pause(self):
        pass
