import unittest
import unittest.mock as mock

import sound.basic

_width = 1
_channels = 2
_frame_rate = 44100
_format = 32


def create_audio_mock(sample_width, channels, frame_rate):
    audio_mock = mock.Mock()
    audio_mock.return_value.sample_width = sample_width
    audio_mock.return_value.channels = channels
    audio_mock.return_value.frame_rate = frame_rate
    return audio_mock


@mock.patch("pyaudio.PyAudio")
@mock.patch("pydub.AudioSegment")
class BasicTest(unittest.TestCase):
    def test_loading_file_fails_on_unrecognised_format(self, _, __):
        self.assertRaisesRegex(
            ValueError, "File format not recognised", sound.basic.Basic, "README.md"
        )

    def test_can_load_an_mp3_file(self, dub_mock, _):
        sound.basic.Basic("sound/tracks/song.wav")
        dub_mock.from_wav.assert_called_once()

    def test_can_open_stream_with_file_parameters(self, dub_mock, audio_mock):
        dub_mock.from_wav = create_audio_mock(_width, _channels, _frame_rate)
        sound.basic.Basic("sound/tracks/song.wav")
        audio_mock.return_value.open.assert_called_with(
            format=audio_mock().get_format_from_width(_width),
            channels=_channels,
            rate=_frame_rate,
            output=True,
        )

    def test_writes_sound_buffer_to_stream(self, dub_mock, audio_mock):
        basic = sound.basic.Basic("sound/tracks/song.wav")
        basic.play()
        audio_mock.return_value.open.return_value.write.assert_called_with(
            dub_mock.from_wav().__getitem__().raw_data
        )
