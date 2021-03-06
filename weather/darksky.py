import requests
import datetime

import weather.data


url = "https://api.darksky.net/forecast/"
default_options = {"units": "uk2"}

locations = {"Guildford": "51.2362,0.5704"}
icons = {
    "clear-day": 1,
    "clear-night": 2,
    "rain": 3,
    "snow": 4,
    "sleet": 5,
    "wind": 6,
    "fog": 7,
    "cloudy": 8,
    "partly-cloudy-day": 9,
    "partly-cloudy-night": 10,
}


class Darksky:
    def __init__(
        self,
        base_url="https://api.darksky.net/forecast/",
        api_key=open("api_key", "r").read().strip("\x0A"),
    ):
        self._base_url = base_url
        self._api_key = api_key

    def get_weather(self, location, options=default_options):
        response = requests.get(
            self._base_url + self._api_key + "/" + locations[location], params=options
        )
        if response.status_code == 200:
            return self._process_weather_response(response.json(), location)
        else:
            raise ValueError("Server returned: " + str(response.status_code))

    def _process_weather_response(self, response, location):
        new_data = {}
        for data in response["hourly"]["data"]:
            new_data[
                datetime.datetime.fromtimestamp(data["time"])
            ] = weather.data.TimeData(
                temp=data["temperature"],
                feel_temp=data["apparentTemperature"],
                w_type=self._get_icon(data["icon"]),
                precip=data["precipProbability"],
                wind_dir=self._get_compass_direction(data["windBearing"]),
                wind_speed=data["windSpeed"],
                wind_gust=data["windGust"],
                uv=data["uvIndex"],
                humidity=data["humidity"],
                visibility=data["visibility"],
            )

        new_units = weather.data.Units(temp="C", speed="mph")
        if response["flags"]["units"] == "uk2":
            new_units = weather.data.Units(temp="C", speed="mph")

        return weather.data.WeatherData(
            location=location, data=new_data, units=new_units
        )

    def _get_compass_direction(self, bearing):
        compass = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        offset = 22.5
        for i in range(1, len(compass) - 1):
            middle = 45 * i
            if bearing > middle - offset and bearing < middle + offset:
                return compass[i]
        return compass[0]

    def _get_icon(self, icon):
        if icons[icon] > 0 and icons[icon] < len(icons) + 1:
            return icons[icon]
        return 0
