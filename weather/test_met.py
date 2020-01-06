import json
import unittest
import unittest.mock as mock
import requests_mock

import weather.met


@requests_mock.mock()
class MetTest(unittest.TestCase):
    def test_throws_if_bad_response_recieved(self, get_mock):
        get_mock.get(self.base_url + self.location_path, json={}, status_code=404)
        self.assertRaises(ValueError, self.met.get_locations, self.location_path)

    def test_can_return_list_of_available_locations(self, get_mock):
        get_mock.get(self.base_url + self.location_path, json=self.locations)
        self.assertListEqual(
            self.met.get_locations(self.location_path), self.location_array
        )

    @mock.patch("weather.met.MetWeather.get_locations")
    def test_get_weather_will_call_get_locations_if_not_already_done(
        self, get_mock, location_mock
    ):
        get_mock.get(self.base_url + self.location_id)
        self.met.get_weather(self.location)
        location_mock.assert_called_once()

    @mock.patch("weather.met.MetWeather.get_locations", mock.Mock())
    def test_raises_if_location_is_not_a_valid_location(self, get_mock):
        get_mock.get(self.base_url + self.location_id)
        self.met.get_locations(self.location)
        self.assertRaises(ValueError, self.met.get_weather, self.location)

    def __init__(self, *args, **kwargs):
        super(MetTest, self).__init__(*args, **kwargs)
        self.base_url = (
            "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/"
        )
        self.met = weather.met.MetWeather(self.base_url)
        self.location_path = "sitelist"
        self.locations = json.loads(
            open("test_data/met_test_locations_short.json").read()
        )
        self.location_array = ["Carlisle Airport", "Liverpool John Lennon Airport"]
        self.location = "Carlisle Airport"
        self.location_id = "14"
