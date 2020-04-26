import unittest
import unittest.mock as mock
import time
import datetime

import weather.weather
import weather.data


class TestWeather(unittest.TestCase):
    def test_starting_poll_calls_api_periodically(self):
        api_mock = mock.Mock()
        w = weather.weather.Weather(api_mock)
        w.start_api_poll(0.01)
        time.sleep(0.05)  # let loop poll a few times
        w.kill()  # needed to finish test
        time.sleep(0.01)  # wait for loop to fully exit
        self.assertGreater(api_mock.get_weather.call_count, 1)

    def test_get_weather_returns_weather_response(self):
        api_mock = mock.Mock()
        api_mock.get_weather.return_value = weather_data
        w = run_weather(api_mock)
        self.assertEqual(w.get_weather(), weather_data)

    def test_get_short_returns_correct_length_list(self):
        api_mock = mock.Mock()
        api_mock.get_weather.return_value = weather_data
        w = run_weather(api_mock)
        self.assertEqual(len(w.get_short_weather()), 5)

    def test_get_short_returns_correct_times(self):
        api_mock = mock.Mock()
        api_mock.get_weather.return_value = weather_data
        w = run_weather(api_mock)
        actual = [i.time for i in w.get_short_weather()]
        expected = [
            datetime.datetime(2020, 1, 1, 0, 0),
            datetime.datetime(2020, 1, 1, 3, 0),
            datetime.datetime(2020, 1, 1, 6, 0),
            datetime.datetime(2020, 1, 1, 9, 0),
            datetime.datetime(2020, 1, 1, 12, 0),
        ]
        self.assertListEqual(actual, expected)

    def test_get_short_returns_first_element_of_weather_data(self):
        api_mock = mock.Mock()
        api_mock.get_weather.return_value = weather_data
        w = run_weather(api_mock)
        self.assertEqual(
            w.get_short_weather()[0],
            weather.weather.ShortData(datetime.datetime(2020, 1, 1, 0, 0), 10, 5),
        )

    def test_get_short_returns_averaged_temp_over_time(self):
        api_mock = mock.Mock()
        api_mock.get_weather.return_value = weather_data
        w = run_weather(api_mock)
        self.assertEqual(w.get_short_weather()[1].temp, 10)

    def test_get_short_returns_common_weather_type(self):
        api_mock = mock.Mock()
        api_mock.get_weather.return_value = weather_data
        w = run_weather(api_mock)
        self.assertEqual(w.get_short_weather()[1].w_type, 2)

    def test_get_short_returns_central_weather_type_if_all_different(self):
        api_mock = mock.Mock()
        api_mock.get_weather.return_value = weather_data
        w = run_weather(api_mock)
        self.assertEqual(w.get_short_weather()[2].w_type, 2)


def run_weather(mock):
    w = weather.weather.Weather(mock)
    w.start_api_poll(0.01)
    time.sleep(0.05)  # let loop poll a few times
    w.kill()  # needed to finish test
    time.sleep(0.01)  # wait for loop to fully exit
    return w


weather_data = weather.data.WeatherData(
    "Guildford",
    {
        datetime.datetime(2020, 1, 1, 0, 0): weather.data.TimeData(
            1, 10, 5, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 1, 0): weather.data.TimeData(
            2, 0, 0, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 2, 0): weather.data.TimeData(
            3, 13, 2, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 3, 0): weather.data.TimeData(
            4, 6, 1, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 4, 0): weather.data.TimeData(
            5, 11, 2, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 5, 0): weather.data.TimeData(
            6, 0, 1, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 6, 0): weather.data.TimeData(
            7, 0, 2, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 7, 0): weather.data.TimeData(
            8, 0, 3, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 8, 0): weather.data.TimeData(
            9, 0, 0, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 9, 0): weather.data.TimeData(
            10, 0, 0, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 10, 0): weather.data.TimeData(
            11, 0, 0, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 11, 0): weather.data.TimeData(
            12, 0, 0, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 12, 0): weather.data.TimeData(
            13, 0, 0, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 13, 0): weather.data.TimeData(
            14, 0, 0, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 14, 0): weather.data.TimeData(
            15, 0, 0, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 15, 0): weather.data.TimeData(
            16, 0, 0, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 16, 0): weather.data.TimeData(
            17, 0, 0, 0, "test", 0, 0, 0, 0, 0
        ),
        datetime.datetime(2020, 1, 1, 17, 0): weather.data.TimeData(
            18, 0, 0, 0, "test", 0, 0, 0, 0, 0
        ),
    },
    weather.data.Units("C", "MPH"),
)
