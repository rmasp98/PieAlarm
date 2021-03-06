import unittest
import unittest.mock as mock
import time
import threading

import sound.playlist


def threaded_play(playlist, basic_mock):
    basic_mock.return_value.play.side_effect = lambda _: time.sleep(0.01)
    t = threading.Thread(target=playlist.play)
    t.start()


@mock.patch("sound.basic.Basic")
class PlaylistTest(unittest.TestCase):
    def test_verify_passes_if_valid_playlist_sound_data(self, _):
        sound_data = {"type": "playlist", "playlist": "basic"}
        self.assertTrue(sound.playlist.Playlist.verify_sound_data(sound_data))

    def test_verify_fails_if_no_playlist_file(self, _):
        sound_data = {"type": "playlist"}
        self.assertFalse(sound.playlist.Playlist.verify_sound_data(sound_data))

    def test_verify_fails_if_playlist_file_does_not_exist(self, _):
        sound_data = {"type": "playlist", "playlist": "notexist"}
        self.assertFalse(sound.playlist.Playlist.verify_sound_data(sound_data))

    def test_play_plays_track_in_playlist_with_chunksize(self, basic_mock):
        playlist = sound.playlist.Playlist("basic")
        chunk_size = 10
        playlist.play(chunk_size)
        basic_mock.return_value.play.assert_called_with(chunk_size)

    # def test_play_plays_all_tracks_in_playlist(self, basic_mock):
    #     playlist = sound.playlist.Playlist("basic")
    #     playlist.play()
    #     basic_mock.assert_has_calls(
    #         [
    #             mock.call("waterfall.wav"),
    #             mock.call().play(100),
    #             mock.call().close(),
    #             mock.call("song.mp3"),
    #             mock.call().play(100),
    #             mock.call().close(),
    #         ],
    #     )

    def test_pause_calls_tracks_pause(self, basic_mock):
        playlist = sound.playlist.Playlist("basic")
        threaded_play(playlist, basic_mock)
        playlist.pause()
        time.sleep(0.01)  # Bodge to keep mock alive for thread
        basic_mock.return_value.pause.assert_called_once()

    def test_play_after_pause_resumes_same_track(self, basic_mock):
        playlist = sound.playlist.Playlist("../../test_data/playlist_single")
        threaded_play(playlist, basic_mock)
        playlist.pause()
        time.sleep(0.01)  # Bodge to make sure fully escaped last play
        playlist.play()
        basic_mock.assert_called_once()

    def test_pause_prevents_any_further_playback(self, basic_mock):
        playlist = sound.playlist.Playlist("basic")
        threaded_play(playlist, basic_mock)
        playlist.pause()
        time.sleep(0.01)  # Bodge to make sure fully escaped last play
        basic_mock.return_value.play.assert_called_once()

    def test_play_after_pause_plays_all_tracks(self, basic_mock):
        playlist = sound.playlist.Playlist("../../test_data/playlist_multiple")
        threaded_play(playlist, basic_mock)
        playlist.pause()
        time.sleep(0.01)  # Bodge to make sure fully escaped last play
        playlist.play()
        time.sleep(0.01)  # Bodge to make sure fully escaped last play
        self.assertEqual(basic_mock.call_count, 5)

    def test_stop_calls_tracks_stop(self, basic_mock):
        playlist = sound.playlist.Playlist("basic")
        threaded_play(playlist, basic_mock)
        playlist.stop()
        time.sleep(0.01)  # Bodge to keep mock alive for thread
        basic_mock.return_value.stop.assert_called_once()

    def test_stop_prevents_any_further_playback(self, basic_mock):
        playlist = sound.playlist.Playlist("basic")
        threaded_play(playlist, basic_mock)
        playlist.stop()
        time.sleep(0.01)  # Bodge to make sure fully escaped last play
        basic_mock.return_value.play.assert_called_once()

    def test_stop_resets_track_index(self, basic_mock):
        playlist = sound.playlist.Playlist("../../test_data/playlist_multiple")
        threaded_play(playlist, basic_mock)
        time.sleep(0.02)  # Bodge to make sure track_index gets off 0
        playlist.stop()
        time.sleep(0.01)  # Bodge to make sure fully escaped last play
        basic_mock.reset_mock()
        playlist.play()
        self.assertEqual(basic_mock.call_count, 5)

    def test_playlist_randomises_order_of_tracks(self, basic_mock):
        different = False
        for _ in range(5):
            playlist = sound.playlist.Playlist("../../test_data/playlist_multiple")
            playlist.play()
            first_calls = basic_mock.call_args
            basic_mock.reset_mock()
            playlist = sound.playlist.Playlist("../../test_data/playlist_multiple")
            playlist.play()
            different_iter = False
            for first, second in zip(first_calls, basic_mock.call_args):
                if first != second:
                    different_iter = True
            if different_iter:
                different = True
        self.assertTrue(different)

    def test_playlist_checks_to_see_if_track_is_valid(self, basic_mock):
        playlist = sound.playlist.Playlist("../../test_data/playlist_single")
        playlist.play()
        basic_mock.verify_sound_data.assert_called_with(
            {"type": "basic", "track": "sound/tracks/song.mp3"}
        )
