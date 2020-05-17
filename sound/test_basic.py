import threading
import unittest
import unittest.mock as mock

import sound.basic


# Variales for tests
_width = 1
_channels = 2
_frame_rate = 44100
_format = 32
_length = 100
_small_chunks = 1
_wav_file = "waterfall.wav"
_mp3_file = "song.mp3"


def create_audio_mock(
    sample_width=_width, channels=_channels, frame_rate=_frame_rate, length=_length
):
    audio_mock = mock.MagicMock()
    audio_mock.return_value.sample_width = sample_width
    audio_mock.return_value.channels = channels
    audio_mock.return_value.frame_rate = frame_rate
    audio_mock.return_value.__len__.return_value = length
    return audio_mock


def async_play(pydub_mock, length=_length, track=_wav_file):
    pydub_mock.from_wav = create_audio_mock(length=length)
    basic = sound.basic.Basic(_wav_file)
    sound_thread = threading.Thread(target=basic.play, args=[_small_chunks])
    sound_thread.start()
    return basic, sound_thread


# @mock.patch("pyaudio.PyAudio")
@mock.patch("sound.basic.Basic._pa")
@mock.patch("pydub.AudioSegment")
class BasicTest(unittest.TestCase):
    def test_loading_file_fails_on_unrecognised_format(self, _, __):
        self.assertRaisesRegex(
            ValueError,
            "File format not recognised",
            sound.basic.Basic,
            "../../README.md",
        )

    def test_can_load_a_wav_file(self, pydub_mock, _):
        sound.basic.Basic(_wav_file)
        pydub_mock.from_wav.assert_called_once()

    def test_can_open_stream_with_file_parameters(self, pydub_mock, pyaudio_mock):
        pydub_mock.from_wav = create_audio_mock(_width, _channels, _frame_rate)
        sound.basic.Basic(_wav_file)
        pyaudio_mock.open.assert_called_with(
            format=pyaudio_mock.get_format_from_width(_width),
            channels=_channels,
            rate=_frame_rate,
            output=True,
        )

    def test_full_buffer_written_to_stream(self, pydub_mock, _):
        pydub_mock.from_wav = create_audio_mock(length=_length)
        basic = sound.basic.Basic(_wav_file)
        basic.play(_small_chunks)
        for i in range(_length):
            self.assertEquals(
                pydub_mock.from_wav.return_value.__getitem__.call_args_list[i][0][0],
                slice(i, i + _small_chunks),
            )

    def test_can_pause_playback(self, pydub_mock, pyaudio_mock):
        basic, sound_thread = async_play(pydub_mock)
        basic.pause()
        sound_thread.join()
        self.assertLess(
            pyaudio_mock.return_value.open.return_value.write.call_count, _length
        )

    def test_can_continue_from_same_point_after_pause(self, pydub_mock, pyaudio_mock):
        basic, sound_thread = async_play(pydub_mock)
        basic.pause()
        sound_thread.join()
        basic.play(_small_chunks)
        self.assertEquals(pyaudio_mock.open.return_value.write.call_count, _length)

    def test_stop_starts_track_from_beginning(self, pydub_mock, pyaudio_mock):
        basic, sound_thread = async_play(pydub_mock)
        basic.stop()
        sound_thread.join()
        basic.play(_small_chunks)
        self.assertGreater(pyaudio_mock.open.return_value.write.call_count, _length)

    def test_can_load_an_mp3_file(self, pydub_mock, _):
        sound.basic.Basic(_mp3_file)
        pydub_mock.from_mp3.assert_called_once()

    def test_verify_passes_if_valid_basic_sound_data(self, _, __):
        sound_data = {"type": "basic", "track": "song.mp3"}
        self.assertTrue(sound.basic.Basic.verify_sound_data(sound_data))

    def test_verify_fails_if_no_track(self, _, __):
        sound_data = {"type": "basic"}
        self.assertFalse(sound.basic.Basic.verify_sound_data(sound_data))

    def test_verify_fails_if_provided_track_does_not_exist(self, _, __):
        sound_data = {"type": "basic", "track": "nofile"}
        self.assertFalse(sound.basic.Basic.verify_sound_data(sound_data))
