import pyaudio
import pydub


class Basic:
    def __init__(self, file, chunk_size=1024):
        if file[-3:] == "mp3":
            self._track = pydub.AudioSegment.from_mp3(file)
        elif file[-3:] == "wav":
            self._track = pydub.AudioSegment.from_wav(file)
        # self._track = wave.open(file)
        self._pause = False
        self._stream = pyaudio.PyAudio().open(
            format=pyaudio.PyAudio().get_format_from_width(self._track.sample_width),
            channels=self._track.channels,
            rate=self._track.frame_rate,
            output=True,
        )
        self._chunks = pydub.utils.make_chunks(self._track, chunk_size)
        self._chunk_index = 0

    def __del__(self):
        self._stream.stop_stream()
        self._stream.close()
        self._track.close()

    def play(self):
        self._pause = False
        while self._chunk_index < len(self._chunks):
            if self._pause:
                return
            self._stream.write(self._chunks[self._chunk_index].raw_data)
            self._chunk_index = self._chunk_index + 1

    def pause(self):
        self._pause = True

    def stop(self):
        self._pause = True
        self._chunk_index = 0
