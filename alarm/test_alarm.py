import unittest
import unittest.mock
import datetime

import alarm.alarm


class AlarmTest(unittest.TestCase):
    def test_get_alarm_returns_correct_datetime_object(self):
        test_alarm = create_alarm(hour=6, minute=30)
        self.assertEqual(test_alarm.time(), datetime.time(6, 30))

    def test_returns_list_of_active_days(self):
        test_alarm = create_alarm(days=["Monday"])
        self.assertEqual({"Monday"}, test_alarm.active_days())

    def test_raises_exception_if_provided_day_not_valid(self):
        self.assertRaises(ValueError, create_alarm, days=["Hello"])

    def test_rasies_exception_if_empty_list_provided(self):
        self.assertRaises(TypeError, create_alarm, days=[])

    def test_can_store_multiple_days(self):
        test_alarm = create_alarm(days=["Wednesday", "Sunday"])
        self.assertEqual({"Wednesday", "Sunday"}, test_alarm.active_days())

    @unittest.mock.patch("sound.player.Player")
    def test_verifies_playback_object_is_valid(self, player_mock):
        create_alarm(6, 30, ["Monday"])
        player_mock.verify_sound_data.assert_called_once()

    def test_returns_correct_next_alarm_time(self):
        test_alarm = create_alarm(6, 30, ["Monday"])
        self.assertEqual(test_alarm.find_next_alarm().time(), datetime.time(6, 30))

    def test_returns_correct_next_alarm_day(self):
        test_alarm = create_alarm(6, 30, ["Wednesday"])
        self.assertEqual(test_alarm.find_next_alarm().weekday(), 2)

    def test_does_not_return_today_if_time_has_passed(self):
        with unittest.mock.patch.object(
            datetime, "datetime", unittest.mock.Mock(wraps=datetime.datetime)
        ) as patched:
            patched.now.return_value = datetime.datetime(
                2019, 7, 23, 8, 0
            )  # 8am on Tuesday
            test_alarm = create_alarm(hour=6, minute=30, days=["Tuesday"])
            self.assertEqual(
                test_alarm.find_next_alarm(), datetime.datetime(2019, 7, 30, 6, 30)
            )


def create_alarm(
    hour=0,
    minute=0,
    days=["Monday"],
    playback={"type": "basic", "track": "sound/tracks/song.mp3"},
    active=True,
):
    return alarm.alarm.Alarm(hour, minute, days, playback, active)
