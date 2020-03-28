import sound.basic


# Playlist
# media player Single
# media player playlist
# Random

# Other media controls


class Player:
    """Player

    Interface to all sound classes. Responsible for creating and closing down 
    sound classes and passing on media controls. Sound class and config defined
    by sound_data, which is a json containing type, and any metadata that
    type requires.
    """

    def __init__(self):
        self._player = None

    @classmethod
    def verify_sound_data(cls, sound_data):
        """Makes sure that sound_data is valid"""
        if "type" in sound_data:
            if sound_data["type"] == "basic":
                return sound.basic.Basic.verify_sound_data(sound_data)
        return False

    def play(self, sound_data):
        """Creates sound object, plays it (blocking), closes it down and
        returns true if played successfully. Only one track can be played on
        a player at a time"""
        if self._player is None:
            self._player = self._get_player(sound_data)
            if self._player is not None:
                self._player.play()
                self._player.close()
                self._player = None
                return True
        return False

    def stop(self):
        """This will break the play loop of the sound object. It will result
        in play closing down and returning"""
        if self._player is not None:
            self._player.stop()

    def _get_player(self, sound_data):
        if self.verify_sound_data(sound_data):
            if sound_data["type"] == "basic":
                return sound.basic.Basic(sound_data["track"])
