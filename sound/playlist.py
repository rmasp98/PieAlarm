import os
import random

import sound.basic

playlist_path = "sound/playlists/"


class Playlist:
    """Playlist player plays songs from a playlist currently in a random order"""

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
        """Check to see if sound_data contains playlist and the playlist file exists"""
        if "playlist" in sound_data and os.path.exists(
            playlist_path + sound_data["playlist"]
        ):
            return True
        return False

    def play(self, chunk_size=100):
        """Start playing tracks in the playlist. chunk_size defines chunks in milliseconds
        that are written to stream. The is a balance of responsiveness to
        CPU consumption
        """
        self._exit_playback = False
        self._paused = False
        for self._track_index in range(self._track_index, len(self._tracks)):
            if sound.basic.Basic.verify_sound_data(
                {"type": "basic", "track": self._tracks[self._track_index]}
            ):
                if self._currently_playing is None:
                    self._currently_playing = sound.basic.Basic(
                        self._tracks[self._track_index]
                    )
                self._currently_playing.play(chunk_size)
                if not self._paused:
                    self.close()
                if self._exit_playback:
                    return

    def pause(self):
        """Pause track. Play will continue from where it stopped"""
        self._exit_playback = True
        self._paused = True
        if self._currently_playing is not None:
            self._currently_playing.pause()

    def stop(self):
        """Stop playback. Track will restart back to first in playlist"""
        self._exit_playback = True
        self._track_index = 0
        if self._currently_playing is not None:
            self._currently_playing.stop()

    def close(self):
        """Close track if one is still loaded"""
        if self._currently_playing is not None:
            self._currently_playing.close()
            self._currently_playing = None
