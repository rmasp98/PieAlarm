import mote

lamp = [255, 140, 50]


class Light:
    def __init__(self, channels=[1], num_leds=16, gamma=False):
        if channels == []:
            raise ValueError(
                "No Channels have been initialised so this will do nothing"
            )

        self._mote = mote.Mote()
        self._channels = channels
        self._num_leds = num_leds
        for channel in channels:
            self._mote.configure_channel(channel, num_leds, gamma)

    def set_all(self, red, green, blue, brightness=1.0):
        self._mote.set_all(red, green, blue, brightness)
        self._mote.show()

    def clear_all(self):
        self._mote.clear()
        self._mote.show()

    def set_warm(self, brightness=1.0):
        self.set_all(255, 140, 50, brightness)
