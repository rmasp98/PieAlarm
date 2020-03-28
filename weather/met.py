import os
import datetime
import requests

import weather.weather


class MetWeather:
    def __init__(
        self,
        base_url="http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/",
    ):
        self._base_url = base_url
        self._locations = {}
        # self._api_key = os.environ["MET_API_KEY"]
        self._api_key = open("api_key", "r").read().strip("\x0A")

    def get_locations(self):
        response = requests.get(self._base_url + "sitelist?key=" + self._api_key)
        if response.status_code == 200:
            return self._process_location_response(response.json())
        # TODO: figure out a better exception to use
        raise ValueError("Error with the Met API")

    def get_weather(self, location):
        try:
            print(self._base_url + location + "?res=3hourly&key=" + self._api_key)
            response = requests.get(
                self._base_url + location,
                params={"res": "3hourly", "key": self._api_key},
            )
            print(response.request.url)
            return self._process_weather_response(response.json())

        except:
            raise ValueError("{} does not appear to be a valid location".format("FIX"))

    def _process_location_response(self, response):
        self._locations = {}
        for location in response["Locations"]["Location"]:
            self._locations[location["name"]] = location["id"]
        return dict(self._locations)

    def _process_weather_response(self, response):
        all_weather = {}
        for day in response["SiteRep"]["DV"]["Location"]["Period"]:
            start_date = datetime.datetime.strptime(day["value"], "%Y-%m-%dZ")
            if len(day["Rep"]) != 8:
                start_date = datetime.datetime.strptime(
                    response["SiteRep"]["DV"]["dataDate"], "%Y-%m-%dT%H:%M:%SZ"
                )
            it = 0
            for three_hour in day["Rep"]:
                all_weather[
                    start_date + datetime.timedelta(hours=it * 3)
                ] = weather.weather.WeatherData(
                    temp=three_hour["T"],
                    feel_temp=three_hour["F"],
                    w_type=0,
                    precip=three_hour["Pp"],
                    wind_dir=three_hour["D"],
                    wind_speed=three_hour["S"],
                    wind_gust=three_hour["G"],
                    uv=three_hour["U"],
                    humidity=three_hour["H"],
                    visibility=three_hour["V"],
                )
                it = it + 1
        return weather.weather.Weather(
            location=response["SiteRep"]["DV"]["Location"]["name"],
            data=all_weather,
            units=self._get_units(response),
        )

    def _get_units(self, response):
        temp = speed = ""
        for params in response["SiteRep"]["Wx"]["Param"]:
            if params["name"] == "T":
                temp = params["units"]
            elif params["name"] == "S":
                speed = params["units"]
        return weather.weather.WeatherUnits(temp, speed)
