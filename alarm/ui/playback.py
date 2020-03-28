import os
import pathlib
import glob
import PyQt5.QtWidgets

import utils.layout


class PlaybackWidget(PyQt5.QtWidgets.QWidget):
    types = ["basic", "playlist"]

    def __init__(self, playback, parent=None):
        super(PlaybackWidget, self).__init__(parent)
        layout = utils.layout.create_horizontal_layout(self)

        self._playback = playback
        if self._playback is None:
            self._playback = {"type": "basic"}

        self._type_combo = _PlaybackCombo("type", self.types, self._playback["type"])
        layout.addWidget(self._type_combo)
        self._type_combo.connect(self._get_type_data_widget)

        self._playback_data = _PlaybackCombo("", [], "")
        layout.addWidget(self._playback_data)
        self._get_type_data_widget()

    def get_playback(self):
        return {
            self._type_combo.get_name(): self._type_combo.get_value(),
            self._playback_data.get_name(): self._playback_data.get_value(),
        }

    def _get_type_data_widget(self):
        playback_type = self._type_combo.get_value()
        if playback_type == "basic":
            self._playback_data.update("track", _get_tracks())
            if "track" in self._playback:
                self._playback_data.set_value(self._playback["track"])
        elif playback_type == "playlist":
            self._playback_data.update("playlist", _get_playlists())
            if "playlist" in self._playback:
                self._playback_data.set_value(self._playback["track"])
        else:
            raise ValueError("You have broken everything!")


class _PlaybackCombo(PyQt5.QtWidgets.QWidget):
    def __init__(self, label, combo_items, start_item, parent=None):
        super(_PlaybackCombo, self).__init__(parent)

        layout = utils.layout.create_horizontal_layout(self)

        self._label = PyQt5.QtWidgets.QLabel()
        layout.addWidget(self._label)

        self._combo = PyQt5.QtWidgets.QComboBox()
        layout.addWidget(self._combo)

        self.update(label, combo_items)
        if start_item in combo_items:
            self._combo.setCurrentText(start_item)

    def update(self, label, combo_items):
        self._label.setText(label)
        self._combo.clear()
        self._combo.addItems(combo_items)

    def get_name(self):
        return self._label.text()

    def get_value(self):
        return self._combo.currentText()

    def set_value(self, value):
        index = self._combo.findText(value)
        if index != -1:
            self._combo.setCurrentIndex(index)

    def connect(self, callback):
        self._combo.activated[str].connect(callback)


# TODO: I want to eventually just display file name
# which can be done keeping as PosixPath and calling name()
def _get_tracks():
    files = list(pathlib.Path("sound/tracks").rglob("*.wav"))
    files.extend(pathlib.Path("sound/tracks").rglob("*.mp3"))
    return [i.as_posix() for i in files]


def _get_playlists():
    return os.listdir("sound/playlists")
