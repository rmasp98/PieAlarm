
from os import listdir
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel

class PlaybackWidget(QWidget):
    types = ["basic", "playlist"]

    def __init__(self, playback, parent=None):
        super(PlaybackWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)

        if playback is None:
            playback = {"type":"basic"}

        self._type_combo = _PlaybackCombo("type", self.types, playback["type"])
        layout.addWidget(self._type_combo)
        self._type_combo.connect(self._get_type_data_widget)

        self._playback_data = _PlaybackCombo("track", self.types, playback["type"])
        layout.addWidget(self._playback_data)
        self._get_type_data_widget()

    def get_playback(self):
        return {self._type_combo.get_name():self._type_combo.get_value(),\
                self._playback_data.get_name():self._playback_data.get_value()}

    def _get_type_data_widget(self):
        playback_type = self._type_combo.get_value()
        if playback_type == "basic":
            self._playback_data.update("track", _get_tracks())
        elif playback_type == "playlist":
            self._playback_data.update("playlist", _get_playlists())
        else:
            raise ValueError("You have broken everything!")

class _PlaybackCombo(QWidget):
    def __init__(self, label, combo_items, start_item, parent=None):
        super(_PlaybackCombo, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self._label = QLabel()
        layout.addWidget(self._label)

        self._combo = QComboBox()
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

    def connect(self, callback):
        self._combo.activated[str].connect(callback)


def _get_tracks():
    return listdir("sound/tracks")

def _get_playlists():
    return listdir("sound/playlists")
