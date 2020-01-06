import sound.basic


# Basic
# Playlist
# media player Single
# media player playlist
# Random


class Player:
    def __init__(self):
        self._player = None

    @classmethod
    def verify_sound_data(cls, sound_data):
        if "type" in sound_data:
            if sound_data["type"] == "basic" and "track" in sound_data:
                return True
        return False

    def play(self, sound_data):
        if self._player is None:
            self._player = self._get_player(sound_data)
            if self._player is not None:
                self._player.play()
                self._player.close()
                self._player = None
                return True
        return False

    def stop(self):
        if self._player is not None:
            self._player.stop()

    def _get_player(self, sound_data):
        if self.verify_sound_data(sound_data):
            if sound_data["type"] == "basic":
                return sound.basic.Basic(sound_data["track"])
