import unittest
import unittest.mock as mock

import settings.settings

general_default = {"Brightness": 20, "Theme": "Dark"}
alarm_default = {"No. of Snoozes": 5, "Snooze Time": 10, "Alarms": []}
light_default = {
    "Warm": [255, 140, 50],
    "Custom1": [0, 0, 0],
    "Custom2": [0, 0, 0],
    "Custom3": [0, 0, 0],
    "Main Light Colour": "Warm",
}
player_default = {
    "Volume": 40,
    "Cross Fade": False,
    "Gapless": False,
    "Normalise Volume": True,
}

# tests
# test update signal
# test AlarmSettings alarm update


class TestSettings(unittest.TestCase):
    def test_general_returns_default_settings_with_empty_input(self):
        g = settings.settings.GeneralSettings({})
        self.assertDictEqual(g.get_settings(), general_default)

    def test_general_returns_updated_settings(self):
        g = settings.settings.GeneralSettings({"Brightness": 40, "Theme": "light"})
        self.assertDictEqual(g.get_settings(), {"Brightness": 40, "Theme": "light"})

    def test_general_does_not_process_unrecognised_options(self):
        g = settings.settings.GeneralSettings({"Test": "Do Not Return"})
        self.assertDictEqual(g.get_settings(), general_default)

    def test_general_can_update_setting(self):
        g = settings.settings.GeneralSettings({})
        g.update_setting("Brightness", 40)
        self.assertDictEqual(g.get_settings(), {"Brightness": 40, "Theme": "Dark"})

    def test_general_raiss_when_adding_unrecognised_settings(self):
        g = settings.settings.GeneralSettings({})
        self.assertRaises(ValueError, g.update_setting, "Test", "Do Not Return")
        # self.assertDictEqual(g.get_settings(), general_default)

    def test_alarm_returns_default_settings_with_empty_input(self):
        a = settings.settings.AlarmSettings({})
        self.assertDictEqual(a.get_settings(), alarm_default)

    def test_light_returns_default_settings_with_empty_input(self):
        l = settings.settings.LightSettings({})
        self.assertDictEqual(l.get_settings(), light_default)

    def test_player_returns_default_settings_with_empty_input(self):
        p = settings.settings.PlayerSettings({})
        self.assertDictEqual(p.get_settings(), player_default)

    def test_get_settings_returns_copy_of_settings(self):
        w = settings.settings.WeatherSettings({})
        s = w.get_settings()
        s["Api"] = "Met"
        self.assertEqual(w.get_settings()["Api"], "Darksky")

    def test_can_connect_to_recieve_updates_from_settings(self):
        update_mock = mock.Mock()
        settings.settings.GeneralSettings.connect(update_mock)
        g = settings.settings.GeneralSettings({})
        g.update_setting("Theme", "Light")
        update_mock.assert_called_with("Theme", "Light")

    def test_can_return_setting_options(self):
        w = settings.settings.AlarmSettings({})
        o = w.get_setting_options("Snooze Time")
        self.assertListEqual(o.options, list(range(1, 30)))

    def test_raises_for_invalid_select_setting(self):
        l = settings.settings.LightSettings({})
        self.assertRaises(ValueError, l.update_setting, "Main Light Colour", -5)

    def test_raises_for_invalid_toggle_setting(self):
        p = settings.settings.PlayerSettings({})
        self.assertRaises(ValueError, p.update_setting, "Cross Fade", -5)

    def test_raises_for_invalid_text_setting(self):
        w = settings.settings.WeatherSettings({})
        self.assertRaises(ValueError, w.update_setting, "Api Key", [-5, 1, 7])

    def test_raises_for_invalid_colour_setting(self):
        l = settings.settings.LightSettings({})
        self.assertRaises(ValueError, l.update_setting, "Custom1", -5)

    def test_raises_for_colour_setting_with_incorrect_num_values(self):
        l = settings.settings.LightSettings({})
        self.assertRaises(ValueError, l.update_setting, "Custom1", [-5])

    def test_raises_for_colour_setting_with_numbers_outside_range(self):
        l = settings.settings.LightSettings({})
        self.assertRaises(ValueError, l.update_setting, "Custom1", [1000, -5, 257])

    def test_can_trigger_emit_of_all_settings(self):
        update_mock = mock.Mock()
        a = settings.settings.AlarmSettings({})
        settings.settings.AlarmSettings.connect(update_mock)
        a.emit_all()
        update_mock.assert_has_calls(
            [
                mock.call("No. of Snoozes", 5),
                mock.call("Snooze Time", 10),
                mock.call("Alarms", []),
            ],
            any_order=True,
        )
