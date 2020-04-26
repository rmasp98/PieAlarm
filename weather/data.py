import typing
import datetime


class Units(typing.NamedTuple):
    temp: str
    speed: str


class TimeData(typing.NamedTuple):
    temp: float
    feel_temp: float
    w_type: int
    precip: float
    wind_dir: str
    wind_speed: float
    wind_gust: float
    uv: float
    humidity: float
    visibility: float


class WeatherData(typing.NamedTuple):
    location: str
    data: typing.Dict[datetime.datetime, TimeData]
    units: Units
