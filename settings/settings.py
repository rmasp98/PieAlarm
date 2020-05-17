import typing

from scheduler.observer import Observer


class Settings:
    _signal = Observer()
    _options = {}

    def __init__(self, settings):
        self._settings = self._process_settings(settings)

    def get_settings(self):
        return self._settings.copy()

    def update_setting(self, setting, value, emit=True):
        if setting in self._settings:
            if self._validate_new_setting(setting, value):
                self._settings[setting] = value
                if emit:
                    self._signal.notify(setting, value)
            else:
                raise ValueError("Setting not an acceptable value")
        else:
            raise ValueError("The setting, " + setting + ", does not exist")

    def get_setting_options(self, setting):
        return self._options[setting]

    @classmethod
    def connect(cls, func):
        cls._signal.subscribe(func)

    def emit_all(self):
        for setting, value in self._settings.items():
            self._signal.notify(setting, value)

    def _process_settings(self, settings):
        return {
            key: settings.get(key, self._get_default(value))
            for key, value in self._options.items()
        }

    def _get_default(self, setting):
        if setting.o_type == "select":
            return setting.options[setting.default]
        else:
            return setting.default

    def _validate_new_setting(self, setting, value):
        option = self._options[setting]
        if option.o_type == "select":
            return value in option.options
        elif option.o_type == "toggle":
            return value == True or value == False
        elif option.o_type == "text":
            return isinstance(value, str)
        elif option.o_type == "colour":
            return (
                isinstance(value, list)
                and len(value) == 3
                and value[0] in range(256)
                and value[1] in range(256)
                and value[2] in range(256)
            )
        return True


class OptionMetadata(typing.NamedTuple):
    o_type: str
    options: list
    default: str


class GeneralSettings(Settings):
    _signal = Observer()
    _settings = {}
    _options = {
        "Brightness": OptionMetadata(
            o_type="select", options=list(range(1, 101)), default=19
        ),
        "Theme": OptionMetadata(o_type="select", options=["Dark", "Light"], default=0),
    }


class AlarmSettings(Settings):
    _signal = Observer()
    _settings = {}
    _options = {
        "No. of Snoozes": OptionMetadata(
            o_type="select", options=list(range(10)), default=5
        ),
        "Snooze Time": OptionMetadata(
            o_type="select", options=list(range(1, 30)), default=9
        ),
        "Alarms": OptionMetadata(o_type="none", options=None, default=[]),
    }


class Colour(typing.NamedTuple):
    name: str
    colour: list


class LightSettings(Settings):
    _signal = Observer()
    _settings = {}
    _options = {
        "Warm": OptionMetadata(o_type="colour", options=[], default=[255, 140, 50]),
        "Custom1": OptionMetadata(o_type="colour", options=[], default=[0, 0, 0]),
        "Custom2": OptionMetadata(o_type="colour", options=[], default=[0, 0, 0]),
        "Custom3": OptionMetadata(o_type="colour", options=[], default=[0, 0, 0]),
        "Main Light Colour": OptionMetadata(
            o_type="select",
            options=["Warm", "Custom1", "Custom2", "Custom3"],
            default=0,
        ),
    }


class PlayerSettings(Settings):
    _signal = Observer()
    _settings = {}
    _options = {
        "Volume": OptionMetadata(o_type="select", options=list(range(100)), default=40),
        "Cross Fade": OptionMetadata(o_type="toggle", options=None, default=False),
        "Gapless": OptionMetadata(o_type="toggle", options=None, default=False),
        "Normalise Volume": OptionMetadata(o_type="toggle", options=None, default=True),
    }


class WeatherSettings(Settings):
    _signal = Observer()
    _settings = {}
    _options = {
        "Api": OptionMetadata(o_type="select", options=["Darksky"], default=0),
        "Api Key": OptionMetadata(o_type="text", options=None, default="",),
        "Home Weather": OptionMetadata(
            o_type="select", options=["Hourly", "Three hourly", "Daily"], default=1,
        ),
    }
