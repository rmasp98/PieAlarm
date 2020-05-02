import threading
import time
import datetime
import logging
import typing

log = logging.getLogger(__name__)


class ShortData(typing.NamedTuple):
    time: datetime.datetime
    temp: float
    w_type: int


class Weather:
    def __init__(self, api, location="Guildford", options={"units": "uk2"}):
        self._location = location
        self._options = options
        self._api = api
        self._weather_data = None
        self._repeat_time = None
        self._event = threading.Event()
        self._thread = threading.Thread(target=self._get_weather)

    def start_api_poll(self, repeat_time=900):
        self._repeat_time = repeat_time
        self._thread.start()

    def get_weather(self):
        return self._weather_data

    def get_short_weather(self):
        data = self._weather_data.data
        ordered = sorted(data)
        output = [
            ShortData(ordered[0], data[ordered[0]].feel_temp, data[ordered[0]].w_type,)
        ]
        for index in range(3, 14, 3):
            averaged = [
                data[ordered[index - 1]],
                data[ordered[index]],
                data[ordered[index + 1]],
            ]
            temp = self._get_average_temp(averaged)
            w_type = self._get_common_weather(averaged)
            output.append(ShortData(ordered[index], temp, w_type))
        return output

    def kill(self):
        self._event.set()

    def _get_weather(self):
        while True:
            try:
                self._weather_data = self._api.get_weather(
                    self._location, self._options
                )
            except:
                log.error("Weather Api is throwing errors")
            if self._event.wait(self._repeat_time):
                break

    def _get_average_temp(self, data):
        total = 0
        for datum in data:
            total += datum.feel_temp
        return total / len(data)

    def _get_common_weather(self, data):
        lst = [i.w_type for i in data]
        for index in range(len(lst)):
            if lst.count(index) > 1:
                return lst[index]
        return lst[1]
