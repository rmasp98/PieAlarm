import json

from settings.settings import GeneralSettings
from settings.settings import AlarmSettings
from settings.settings import LightSettings
from settings.settings import PlayerSettings
from settings.settings import WeatherSettings

packages = {
    "General": GeneralSettings,
    "Alarm": AlarmSettings,
    "Light": LightSettings,
    "Player": PlayerSettings,
    "Weather": WeatherSettings,
}


class Interface:
    def __init__(self):
        self._settings = {}
        self.settings_file = "settings.conf"
        self.load()

    def load(self):
        try:
            with open(self.settings_file) as json_file:
                data = json.load(json_file)
                self._process_json(data)
        except:
            self._process_json({})

    def save(self):
        with open(self.settings_file, "w") as json_file:
            out_settings = {}
            for package in self.list_packages():
                out_settings[package] = self._settings[package].get_settings()
            json.dump(out_settings, json_file)

    def get_settings(self, package):
        return self._settings[package].get_settings()

    def get_setting_options(self, package, setting):
        return self._settings[package].get_setting_options(setting)

    def update_setting(self, package, setting, value, emit=True):
        if package in self._settings:
            self._settings[package].update_setting(setting, value, emit)
            self.save()

    def emit_all(self):
        for settings in self._settings.values():
            settings.emit_all()

    def list_packages(self):
        return set(packages.keys())

    def _process_json(self, data):
        for name, constructor in packages.items():
            self._settings[name] = constructor(data.get(name, {}))
