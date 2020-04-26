import json
import datetime
import unittest
import requests_mock

import weather.darksky

baseurl = "https://api.darksky.net/forecast/"
key = "key"
location = "Guildford"
options = {"units": "uk2"}
data_times = [
    datetime.datetime.fromtimestamp(1585342800),
    datetime.datetime.fromtimestamp(1585346400),
    datetime.datetime.fromtimestamp(1585350000),
]
test_data = weather.data.TimeData(
    temp=6.44,
    feel_temp=2.24,
    w_type=2,
    precip=0,
    wind_dir="NE",
    wind_speed=16.42,
    wind_gust=29.9,
    uv=0,
    humidity=0.7,
    visibility=10,
)


class DarkskyTest(unittest.TestCase):
    @requests_mock.mock()
    def test_throws_if_not_a_200_response(self, get_mock):
        get_mock.get(
            baseurl + key + "/51.2362,0.5704?units=uk2", json={}, status_code=403
        )
        darksky = weather.darksky.Darksky(baseurl, key)
        self.assertRaises(ValueError, darksky.get_weather, location, options)

    @requests_mock.mock()
    def test_returns_weather_object_containing_lcation(self, get_mock):
        get_mock.get(
            baseurl + key + "/51.2362,0.5704?units=uk2",
            json=json.loads(open("test_data/darksky_response_short.json").read()),
        )
        darksky = weather.darksky.Darksky(baseurl, key)
        weather_location = darksky.get_weather(location, options).location
        self.assertEqual(weather_location, location)

    @requests_mock.mock()
    def test_returns_weather_object_containing_units(self, get_mock):
        get_mock.get(
            baseurl + key + "/51.2362,0.5704?units=uk2",
            json=json.loads(open("test_data/darksky_response_short.json").read()),
        )
        darksky = weather.darksky.Darksky(baseurl, key)
        units = darksky.get_weather(location, options).units
        self.assertEqual(units, weather.data.Units(temp="C", speed="mph"))

    @requests_mock.mock()
    def test_returns_weather_object_containing_correct_times(self, get_mock):
        get_mock.get(
            baseurl + key + "/51.2362,0.5704?units=uk2",
            json=json.loads(open("test_data/darksky_response_short.json").read()),
        )
        darksky = weather.darksky.Darksky(baseurl, key)
        times = darksky.get_weather(location, options).data.keys()
        self.assertListEqual(list(times), data_times)

    @requests_mock.mock()
    def test_returns_weather_object_containing_correct_data(self, get_mock):
        get_mock.get(
            baseurl + key + "/51.2362,0.5704?units=uk2",
            json=json.loads(open("test_data/darksky_response_short.json").read()),
        )
        darksky = weather.darksky.Darksky(baseurl, key)
        data = darksky.get_weather(location, options).data.values()
        self.assertEqual(list(data)[0], test_data)
