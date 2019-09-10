import wave
import pyaudio

class Basic:
    def __init__(self, file):
        self._track = wave.open(file)
        self._pause = False
        self._stream = pyaudio.PyAudio().open(\
            format=pyaudio.PyAudio().get_format_from_width(self._track.getsampwidth()),\
            channels=self._track.getnchannels(),\
            rate=self._track.getframerate(),\
            output=True)

    def __del__(self):
        self._stream.stop_stream()
        self._stream.close()
        self._track.close()

    def play(self, chunk=1024):
        self._pause = False
        data = self._track.readframes(chunk)
        while not self._pause and data != '':
            self._stream.write(data)
            data = self._track.readframes(chunk)

    def pause(self):
        self._pause = True

    def stop(self):
        self._pause = True
        self._track.setpos(0)
