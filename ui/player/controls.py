import PyQt5.QtWidgets

from scheduler.observer import Observer


class Controls(PyQt5.QtWidgets.QWidget):
    def __init__(self, player, parent=None):
        super(Controls, self).__init__(parent)
        self._skip_time = 30
        v_layout = PyQt5.QtWidgets.QVBoxLayout(self)

        sub_controls = PyQt5.QtWidgets.QWidget()
        v_layout.addWidget(sub_controls)
        s_layout = PyQt5.QtWidgets.QHBoxLayout(sub_controls)

        s_layout.addWidget(
            ControlButton("ui/icons/player/repeat.png", 20, player.repeat)
        )
        s_layout.addWidget(
            ControlButton("ui/icons/player/shuffle.png", 20, player.shuffle)
        )
        s_layout.addWidget(
            ControlButton("ui/icons/player/add_playlist.png", 20, player.add_playlist)
        )

        main_controls = PyQt5.QtWidgets.QWidget()
        v_layout.addWidget(main_controls)
        m_layout = PyQt5.QtWidgets.QHBoxLayout(main_controls)
        m_layout.addWidget(
            ControlButton(
                "ui/icons/player/jump_back.png",
                30,
                lambda: player.previous(-self._skip_time),
            )
        )
        m_layout.addWidget(
            ControlButton("ui/icons/player/previous.png", 30, player.previous)
        )
        m_layout.addWidget(ControlButton("ui/icons/player/play.png", 30, player.play))
        m_layout.addWidget(ControlButton("ui/icons/player/next.png", 30, player.next))
        m_layout.addWidget(
            ControlButton(
                "ui/icons/player/jump.png",
                30,
                lambda: player.previous(self._skip_time),
            )
        )


class ControlButton(PyQt5.QtWidgets.QLabel):
    def __init__(self, image, height, callback, parent=None):
        super(ControlButton, self).__init__(parent)
        self._signal = Observer()
        self._signal.subscribe(callback)
        pixmap = PyQt5.QtGui.QPixmap(image)
        self.setPixmap(pixmap.scaledToHeight(height))

    def onMouseRelease(self, _):
        self._signal.notify()


class Play(PyQt5.QtWidgets.QLabel):
    pass
