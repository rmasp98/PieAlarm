import os
import random

import sound.basic

playlist_path = "sound/playlists/"


class Playlist:
    def __init__(self, filename):
        with open(playlist_path + filename) as playlist:
            self._tracks = [line.rstrip() for line in playlist]
        random.shuffle(self._tracks)
        self._currently_playing = None
        self._track_index = 0
        self._paused = False
        self._exit_playback = False

    @classmethod
    def verify_sound_data(cls, sound_data):
        if "playlist" in sound_data and os.path.exists(
            playlist_path + sound_data["playlist"]
        ):
            return True
        return False

    def play(self, chunk_size=100):
        self._exit_playback = False
        self._paused = False
        for self._track_index in range(self._track_index, len(self._tracks)):
            if self._currently_playing is None:
                self._currently_playing = sound.basic.Basic(
                    self._tracks[self._track_index]
                )
            self._currently_playing.play(chunk_size)
            if not self._paused:
                self._currently_playing.close()
                self._currently_playing = None
            if self._exit_playback:
                return

    def pause(self):
        self._exit_playback = True
        self._paused = True
        if self._currently_playing is not None:
            self._currently_playing.pause()

    def stop(self):
        self._exit_playback = True
        self._track_index = 0
        if self._currently_playing is not None:
            self._currently_playing.stop()

    def close(self):
        pass
