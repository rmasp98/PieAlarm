import os
import pathlib
import glob
import PyQt5.QtWidgets

from ui.widgets.layout import create_vertical_layout
from ui.widgets.layout import create_horizontal_layout
from ui.widgets.spinner import Spinner
from ui.widgets.text import Text
from ui.widgets.text import FontSize


class PlaybackWidget(PyQt5.QtWidgets.QWidget):
    types = ["basic", "playlist"]

    def __init__(self, playback, parent=None):
        super(PlaybackWidget, self).__init__(parent)
        layout = create_vertical_layout(self)

        # self._playback = playback
        # if self._playback is None:
        #     self._playback = {"type": "basic"}

        self._type = PlaybackSpinner("type", self.types, 0)
        self._type.connect(self._update_playback_options)
        layout.addWidget(self._type)

        self._playback_data = PlaybackSpinner("TEMP", [], 0)
        layout.addWidget(self._playback_data)

        self._update_playback_options("basic")

    def get_playback(self):
        return {**self._type.get_playback(), **self._playback_data.get_playback()}

    def _update_playback_options(self, playback_type):
        if playback_type == "basic":
            self._playback_data.update("track", _get_tracks())
        elif playback_type == "playlist":
            self._playback_data.update("playlist", _get_playlists())


class PlaybackSpinner(PyQt5.QtWidgets.QWidget):
    def __init__(self, label, options, start_index, parent=None):
        super(PlaybackSpinner, self).__init__(parent)
        self._layout = create_horizontal_layout(self)

        self._label = Text(label, FontSize.SMALL)
        self._label.setMinimumWidth(50)
        self._layout.addWidget(self._label)
        self._layout.addSpacing(100)

        self._spinner = Spinner(options, start_index=start_index, loop=False)
        self._layout.addWidget(self._spinner)
        self._layout.addStretch()

    def update(self, label, options):
        self._label.setText(label)
        new_spinner = Spinner(options, start_index=0, loop=False)
        self._layout.replaceWidget(self._spinner, new_spinner)
        self._spinner.deleteLater()
        self._spinner = new_spinner

    def get_playback(self):
        return {self._label.text(): self._spinner.get_value()}

    def connect(self, callback):
        self._spinner.change_value.connect(callback)


# TODO: I want to eventually just display file name
# which can be done keeping as PosixPath and calling name()
def _get_tracks():
    files = list(pathlib.Path("sound/tracks").rglob("*.wav"))
    files.extend(pathlib.Path("sound/tracks").rglob("*.mp3"))
    return [i.as_posix()[13:] for i in files]


def _get_playlists():
    return os.listdir("sound/playlists")
