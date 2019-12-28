import pyaudio
import pydub
import filetype


class Basic:
    def __init__(self, file_path):
        self._pause = False
        self._track_pos = 0
        self._track = self._load_file(file_path)
        self._stream = pyaudio.PyAudio().open(
            format=pyaudio.PyAudio().get_format_from_width(self._track.sample_width),
            channels=self._track.channels,
            rate=self._track.frame_rate,
            output=True,
        )

    def _load_file(self, file_path):
        file_type = filetype.guess(file_path)
        if file_type is not None:
            if file_type.mime == "audio/x-wav":
                return pydub.AudioSegment.from_wav(file_path)
        raise ValueError("File format not recognised. Please check " + file_path)

    def close(self):
        self._stream.stop_stream()
        self._stream.close()

    def __del__(self):
        self.close()

    def play(self, chunk_size=1000):
        self._pause = False
        while self._track_pos < len(self._track):
            if self._pause:
                return
            end_pos = self._track_pos + chunk_size
            if end_pos > len(self._track):
                end_pos = len(self._track)
            self._stream.write(self._track[self._track_pos : end_pos].raw_data)
            self._track_pos = self._track_pos + chunk_size

    def pause(self):
        self._pause = True

    def stop(self):
        self._pause = True
        self._track_pos = 0
