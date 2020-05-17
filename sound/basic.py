import os.path

import pyaudio
import pydub
import filetype


class Basic:
    """Basic player

    Class to load and process a single audio file. This should only be
    used by the Player class or other sound classes.
    """

    _pa = pyaudio.PyAudio()
    track_dir = "sound/tracks/"

    def __init__(self, file_path):
        self._pause = False
        self._track_pos = 0
        self._track = self._load_file(self.track_dir + file_path)
        self._stream = self._open_stream()

    @classmethod
    def verify_sound_data(cls, sound_data):
        """Check to see if sound_data contains track and the track exists"""
        if "track" in sound_data and os.path.exists(
            cls.track_dir + sound_data["track"]
        ):
            return True
        return False

    def play(self, chunk_size=50):
        """Start playback of track. chunk_size defines chunks in milliseconds
        that are written to stream. The is a balance of responsiveness to
        CPU consumption
        """
        self._pause = False
        self._write_to_stream(chunk_size)

    def pause(self):
        """Pause track. Playback will continue from where it stopped"""
        self._pause = True

    def stop(self):
        """Stop track. Playback will start from beginning"""
        self._pause = True
        self._track_pos = 0

    def close(self):
        """Stops and closes stream. Should be run when this class is no
        longer required.
        """
        self._stream.stop_stream()
        self._stream.close()

    def _load_file(self, file_path):
        file_type = filetype.guess(file_path)
        if file_type is not None:
            if file_type.mime == "audio/x-wav":
                return pydub.AudioSegment.from_wav(file_path)
            if file_type.mime == "audio/mpeg":
                return pydub.AudioSegment.from_mp3(file_path)
        raise ValueError("File format not recognised. Please check " + file_path)

    def _open_stream(self):
        return self._pa.open(
            format=self._pa.get_format_from_width(self._track.sample_width),
            channels=self._track.channels,
            rate=self._track.frame_rate,
            output=True,
        )

    def _write_to_stream(self, chunk_size):
        while self._track_pos < len(self._track):
            if self._pause:
                return
            end_pos = self._track_pos + chunk_size
            if end_pos > len(self._track):
                end_pos = len(self._track)
            self._stream.write(self._track[self._track_pos : end_pos].raw_data)
            self._track_pos = self._track_pos + chunk_size
