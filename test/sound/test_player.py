import unittest
import mock

from sound.player import Player

class PlayerTest(unittest.TestCase):

    def test_return_false_if_type_not_provided(self):
        self.assertFalse(self.player.play({}))

    def test_return_false_if_type_basic_but_no_track(self):
        sound_data = {"type":"basic"}
        self.assertFalse(self.player.play(sound_data))

    @mock.patch("sound.basic.Basic")
    def test_creates_basic_object_when_selected(self, basic):
        self.player.play(self.sound_data)
        basic.assert_called_once_with(self.sound_data["track"])

    @mock.patch("sound.basic.Basic")
    def test_plays_basic_player_when_selected(self, basic):
        self.player.play(self.sound_data)
        basic.return_value.play.assert_called_once()

    @mock.patch("sound.basic.Basic", mock.Mock())
    def test_returns_false_if_player_is_already_playing(self):
        self.player.play(self.sound_data)
        self.assertFalse(self.player.play(self.sound_data))

    @mock.patch("sound.basic.Basic")
    def test_stop_calls_player_stop(self, basic):
        self.player.play(self.sound_data)
        self.player.stop()
        basic.return_value.stop.assert_called_once()

    @mock.patch("sound.basic.Basic", mock.Mock())
    def test_another_track_can_be_played_after_first_stopped(self):
        self.player.play(self.sound_data)
        self.player.stop()
        self.assertTrue(self.player.play(self.sound_data))


    def __init__(self, *args, **kwargs):
        super(PlayerTest, self).__init__(*args, **kwargs)
        self.player = Player()
        self.sound_data = {"type":"basic", "track":"test"}
