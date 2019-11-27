# Playing Sound

An alarm would likely be fairly useless if it did not make any sound. So this part of the application is quite important. I have grand plans for the sound module, which includes streaming YouTube videos, playing playlists from Plex or Spotify and a whole host of other features. However, at this point all we care about is getting a single music track to play and is all that will be covered here. Hopefully, the more advanced features will be shown in a later posting.

We are going to introduce three separate components for the sound module:
* Audio libraries - python libraries built to help with playing the sound
* Basic sound - a class that can load and play a single track
* Player - a class to determine which sound class to use to play the sound. To start off with this will only be the Basic sound class. 

## Audio libraries

As mentioned, these are pre-built python libraries that do all the heavy lifting for playing a sound such as loading sound tracks (mp3, wav, etc.) and communicating that sound to the speakers. There are a whole range of different libraries that provide a varying range of functionality and features.

The libraries I found were:
* [PyAudio](https://pypi.org/project/PyAudio/) - this is a fairly low level library dedicated to communicating sound to the speakers. It is so low level, that you have to write the byte of the sound file to a function provided by it. This is really useful as we can really easily control the playback but has no capability to load and understand audio files.
* [PyDub](https://pypi.org/project/pydub/) - this actually includes a very good loader for a wide range of audio files and even comes with a playback function that allows you to play those files. Unfortunately, there is no functionality to stop a track when it starts playing, which is not great for us because what do we do when a user snoozes?
* [python-vlc](https://pypi.org/project/python-vlc/) - this is a fantastic all singing all dancing audio library. It seems to be perfect for what we want as it loads all audio types and offers a wide range of playback functionality. Unfortunately, it only allows asynchronous playback (from what I could work out), which adds complexity to our design when it comes to a track finishing/being stopped. In order to be informed about if the track has stopped playing we would have to subscribe to a range of events.
* [SimpleAudio](https://pypi.org/project/simpleaudio/) - this is a very simplistic library that is only able to wav and numpy sounds, which is not too great as it is highly likely we will want to play mp3

There are likely many more libraries out that there, which could include something that does exactly what we need but may brief time on google did not turn it up, so what I ended up choosing was a combination of two libraries. PyDub is used to load various file formats and put them all into a single object type. Then we use PyAudio to play the sounds giving us full control of how the sound is played. For now this will just be a simple synchronous play and stop, but we may fiddle around with this a bit later on.

As always, we need to pip install these libraries!


## Basic sound class

This class should be a simple class that can load an audio file and then play it. It will likely be the foundation of many other classes such as playlist, random, etc. as these will all eventually require the loading and playing of an audio file.

I should note that at this point, we will be doing some test driven development but as with UI, it is quite hard to validate without a human in the loop. For this point we are also going to walk through how to use the python command line to load and run your class in order to manually test that it is working as expected when TDD will no longer suffice.

### Unrecognised file format

Lets start off with something very minor which is throwing an exception when an unrecognised file format is provided to the class. The test should be something like below:
```python
def test_loading_file_fails_on_unrecognised_format(self):
    self.assertRaisesRegex(
        ValueError, "File format not recognised", sound.basic.Basic, "Hello.test"
    )
```

You will notice that we have placed the audio file name directly into the constructor. This is because we intend to load the file in the constructor so that the classing classes just need to create a basic sound and then can play straight away. To get this test working, simply create a constructor with a single argument and place the following exception in there:
```python
def __init__(self, file_path):
    raise ValueError("File format not recognised")
```

We will have make sure that we catch this elsewhere in the application and display a pop-up saying that this file format is not supported. Hopefully we will never even get to that point because a user should only be able to select supported types in the first place but just in case.

### Loading a WAV file

So now that we have given out the warning about incorrect file types, we should try to load our first file. The go to audio file format seems to be .wav so we will start with loading this type of file. Note at this point you are going to be a real ``.wav`` file to test with. As we are using the PyDub library, it is simply a matter of checking to see if the wav loader from this library is called:
```python
@mock.patch("pydub.AudioSegment.from_wav")
def test_can_load_an_mp3_file(self, wav_mock):
    sound.basic.Basic("Hello.wav")
    wav_mock.assert_called_once()
```

All we need to do now is create an if statement that checks to see if the file is a wav file and then call the mocked function for the input parameter file path. As an initial way to check the file type, you can use quite a cool way to access the last four elements of the ``file_path`` string array and compare that to ``".wav"``. Obviously this is not a great solution because it is not case insensitive but it will do for now. We then want to place the exception into the else part of the if statement.
```python
if file_path[-4:] == ".wav":
    track = pydub.AudioSegment.from_wav(file_path)
else:
    raise ValueError("File format not recognised")
```

The ``-4`` here tells python that it needs to find the 4th from end element in the array. The colon tells python be want a range of elements and the lack of a number says that it should be until the end of the string. This code will then get the test to compile. However, as I am writing this, I have found a way to more thoroughly check the file type by checking its MIME type (a magic set of bits that define a file). So lets implement that now!

The library is called [filetype](https://pypi.org/project/filetype/). You can use this library to check the mime type as PyDub does not care about the filename, it loads based on the content of the file. To use this library, we simply pass the file path to the ``guess`` function and then examine the ``mime`` output of the returned object. If this is equal to ``"audio/x-wav"`` then we know it is a ``.wav`` file. We also need to check if the return object is None as this will obviously not have the attribute ``mime``:
```python
file_type = filetype.guess(file_path)
if file_type is not None and file_type.mime == "audio/x-wav":
    track = pydub.AudioSegment.from_wav(file_path) 
```

Hopefully our tests should still be passing. Now that this part is complete and as we know this part of the function will get larger as we introduce new file formats, we should break this part off into a separate function.


### Configure the stream

The next thing that we need to do before we are able to play the file is get the stream, that the file will be playing over, initialised. This part is handled by PyAudio and requires various bits of information from the file in order to play correctly. Here we are going to create a helper function for the test that creates an AudioSegment mock with the correct attributes. We can then compare the values in this mock to what is called when opening the stream.
```python
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
```

Because we need this in the patching decorator, which does not have access to the object variables, we need to declare this in the global scope (outside of the class). This feels a little bit nasty as we are being incredibly prescriptive in the test about what the code needs to do, which I think slightly defeats the point but it is the only way I can think to do it for now. I may come back to this and do it properly later.

The test then simply creates a Basic sound object and checks to see if the open function of PyAudio is called with the correct parameters of the AudioSegment from PyDub:
```python
@mock.patch(
    "pydub.AudioSegment.from_wav", create_audio_mock(_width, _channels, _frame_rate)
)
def test_can_open_stream_with_file_parameters(self, audio_mock):
    sound.basic.Basic("sound/tracks/song.wav")
    audio_mock.return_value.open.assert_called_with(
        format=audio_mock().get_format_from_width(_width),
        channels=_channels,
        rate=_frame_rate,
        output=True,
    )
```

I should note that I have created a class wide patch for PyAudio as every function will need to implement a patch to stop it from trying to play audio files. It also removes the annoying output given by portaudio, which muddies the test output and is really not very helpful.

To get this test passing, it is just a really simple call to the open function in the constructor:
```python
pyaudio.PyAudio().open(
    format=pyaudio.PyAudio().get_format_from_width(track.sample_width),
    channels=track.channels,
    rate=track.frame_rate,
    output=True,
)
```

### Playing the track

Now that we have our file loaded and a stream prepared, all that is left is to actually play the sound. This requires us to write the bytes from the file to the stream, which overall is pretty simple. We will have to do some more complex stuff with this shortly but lets get that functionality in our code first. The test will simply create a sound, play it and then check to see if the the bytes from the file have been passed to the output stream.
```python
def test_writes_sound_buffer_to_stream(self, dub_mock, audio_mock):
    basic = sound.basic.Basic("sound/tracks/song.wav")
    basic.play()
    audio_mock.return_value.open.return_value.write.assert_called_with(
        dub_mock.from_wav().__getitem__().raw_data
    )
```

We have to do some silly tricks with the mocks because we have mocked quite high up and so we need to track the mock through the flow. This is why audio_mock has two return values from the two stages where the mock was used. Essentially ``audio_mock.return_value.open.return_value.write`` is equivalent to ``stream.write``. The second unusual part to this test is the ``__getitem__`` part. This is telling the mock that we are accessing an element in an array. This is to future-proof the test, which you will see soon. 

To get this test to pass, we need to create object variables for both the track and the stream (as we need to access them outside the constructor) and create the following play function, where we pass the bytes to the stream:
```python
def play(self):
    self._stream.write(self._track[:].raw_data)



