import unittest
import unittest.mock as mock

import settings.interface


simple_json = {"General": {"test": "me"}, "Alarm": {"do it": "now"}}


@mock.patch("builtins.open")
@mock.patch("json.load")
class TestInterface(unittest.TestCase):
    @mock.patch("settings.interface.Interface.load")
    def test_init_loads_settings_from_file(self, load_mock, _, __):
        settings.interface.Interface()
        load_mock.assert_called_once()

    def test_load_gets_json_from_file(self, json_mock, open_mock):
        settings.interface.Interface()
        open_mock.assert_called_with("settings.conf")
        json_mock.assert_called_once()

    def test_load_catches_errors_and_sets_defaults(self, _, open_mock):
        open_mock.side_effect = FileNotFoundError()
        settings.interface.Interface()

    @mock.patch("settings.interface.GeneralSettings")
    def test_creates_general_with_defined_inputs(self, general_mock, json_mock, _):
        json_mock.return_value = simple_json
        settings.interface.Interface()
        general_mock.assert_called_with(simple_json["General"])

    @mock.patch("settings.interface.PlayerSettings")
    def test_creates_general_with_empty_input_if_load_fails(
        self, player_mock, json_mock, open_mock
    ):
        open_mock.side_effect = FileNotFoundError()
        json_mock.return_value = simple_json
        settings.interface.Interface()
        player_mock.assert_called_with({})

    @mock.patch("settings.interface.AlarmSettings")
    def test_get_settings_calls_the_relevant_setting_object(self, alarm_mock, _, __):
        i = settings.interface.Interface()
        i.get_settings("Alarm")
        alarm_mock.return_value.get_settings.assert_called_once()

    @mock.patch("json.dump")
    def test_save_opens_file_and_dumps_json(self, json_mock, _, open_mock):
        i = settings.interface.Interface()
        open_mock.reset()
        i.save()
        open_mock.assert_called_with("settings.conf", "w")
        json_mock.assert_called_once()

    @mock.patch("json.dump")
    def test_save_dumps_all_settings(self, json_mock, _, open_mock):
        with mock.patch.multiple(
            "settings.interface",
            GeneralSettings=mock.DEFAULT,
            AlarmSettings=mock.DEFAULT,
            LightSettings=mock.DEFAULT,
            PlayerSettings=mock.DEFAULT,
            WeatherSettings=mock.DEFAULT,
        ) as mocks:
            i = settings.interface.Interface()
            i.save()
            json_mock.assert_called_with(
                {
                    "General": mocks["GeneralSettings"].return_value.get_settings(),
                    "Alarm": mocks["AlarmSettings"].return_value.get_settings(),
                    "Light": mocks["LightSettings"].return_value.get_settings(),
                    "Player": mocks["PlayerSettings"].return_value.get_settings(),
                    "Weather": mocks["WeatherSettings"].return_value.get_settings(),
                },
                open_mock.return_value.__enter__(),
            )

    def test_can_update_package_setting(self, json_mock, _):
        json_mock.return_value = simple_json
        i = settings.interface.Interface()
        i.update_setting("General", "Brightness", 50)
        self.assertEqual(i.get_settings("General")["Brightness"], 50)
