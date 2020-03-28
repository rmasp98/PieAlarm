import json
import unittest
import unittest.mock as mock
import requests_mock

import weather.met


@requests_mock.mock()
class MetTest(unittest.TestCase):
    def test_throws_if_bad_response_recieved_on_location(self, get_mock):
        get_mock.get(self.base_url + self.location_path, json={}, status_code=404)
        self.assertRaises(ValueError, self.met.get_locations)

    def test_can_return_list_of_available_locations(self, get_mock):
        get_mock.get(
            self.base_url + self.location_path,
            json=json.loads(open("test_data/met_test_locations_short.json").read()),
        )
        self.assertDictEqual(self.met.get_locations(), self.locations)

    def test_raises_if_bad_response_recieved_on_weather(self, get_mock):
        get_mock.get(self.base_url + self.location_id, status_code=404)
        self.assertRaises(ValueError, self.met.get_weather, self.location)

    def __init__(self, *args, **kwargs):
        super(MetTest, self).__init__(*args, **kwargs)
        self.base_url = (
            "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/"
        )
        self.met = weather.met.MetWeather(self.base_url)
        self.location_path = "sitelist"
        self.locations = {
            "Carlisle Airport": "14",
            "Liverpool John Lennon Airport": "26",
        }
        self.location = "Carlisle Airport"
        self.location_id = "14"
