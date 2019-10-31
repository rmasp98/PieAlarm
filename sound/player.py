import sound.basic


class Player:
    def __init__(self):
        self._playing = False
        self._player = None

    def play(self, sound_data):
        if not self._playing and "type" in sound_data:
            if sound_data["type"] == "basic" and "track" in sound_data:
                print(self._playing)
                self._playing = True
                self._player = sound.basic.Basic("sound/tracks/" + sound_data["track"])
                self._player.play()
                self._playing = False
                return True
        return False

    def stop(self):
        if self._player is not None:
            self._player.stop()
