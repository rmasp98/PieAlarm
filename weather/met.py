import requests


class MetWeather:
    def __init__(
        self,
        base_url="http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/",
    ):
        self._base_url = base_url
        self._locations = {}
        self._api_key = "d2d309da-21b4-4a9d-9cc2-84a6c7ce483d"

    def get_locations(self, path="sitelist"):
        response = requests.get(self._base_url + path + "?key=" + self._api_key)
        if response.status_code == 200:
            return self._process_location_response(response.json())
        # TODO: figure out a better exception to use
        raise ValueError("Error with the Met API")

    def get_weather(self, location):
        if not self._locations:
            self.get_locations()

        if location in self._locations:
            return

        raise ValueError("{} does not appear to be a valid location".format(location))

    def _process_location_response(self, response):
        self._locations = {}
        for location in response["Locations"]["Location"]:
            self._locations[location["name"]] = location["id"]
        return list(self._locations.keys())
