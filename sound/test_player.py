import threading
import time
import unittest
import unittest.mock as mock

import sound.player


class PlayerTest(unittest.TestCase):
    def test_verify_returns_false_if_no_type(self):
        sound_data = {}
        self.assertFalse(sound.player.Player.verify_sound_data(sound_data))

    @mock.patch("sound.basic.Basic")
    def test_verify_call_basic_verify_if_type_basic(self, basic):
        sound_data = {"type": "basic"}
        sound.player.Player.verify_sound_data(sound_data)
        basic.verify_sound_data.assert_called_once()

    def test_playback_fails_if_type_not_provided(self):
        self.assertFalse(self.player.play({}))

    @mock.patch("sound.basic.Basic")
    def test_creates_basic_object_when_selected(self, basic):
        self.player.play(self.sound_data)
        basic.assert_called_once_with(self.sound_data["track"])

    @mock.patch("sound.basic.Basic")
    def test_plays_basic_player_when_selected(self, basic):
        self.player.play(self.sound_data)
        basic.return_value.play.assert_called_once()

    @mock.patch("sound.basic.Basic")
    def test_returns_false_if_player_is_already_playing(self, basic):
        basic.return_value.play.side_effect = lambda: time.sleep(0.02)
        threading.Thread(target=self.player.play, args=(self.sound_data,)).start()
        time.sleep(0.01)
        self.assertFalse(self.player.play(self.sound_data))

    @mock.patch("sound.basic.Basic")
    def test_stop_calls_player_stop(self, basic):
        basic.return_value.play.side_effect = lambda: time.sleep(0.01)
        threading.Thread(target=self.player.play, args=(self.sound_data,)).start()
        self.player.stop()
        basic.return_value.stop.assert_called_once()

    @mock.patch("sound.basic.Basic", mock.Mock())
    def test_another_track_can_be_played_after_first_stopped(self):
        self.player.play(self.sound_data)
        self.player.stop()
        self.assertTrue(self.player.play(self.sound_data))

    def __init__(self, *args, **kwargs):
        super(PlayerTest, self).__init__(*args, **kwargs)
        self.player = sound.player.Player()
        self.sound_data = {"type": "basic", "track": "sound/tracks/song-short.wav"}
