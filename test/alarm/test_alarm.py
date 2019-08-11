
import unittest
import datetime
import mock

from alarm.alarm import Alarm

def create_alarm(hour=6, minute=30, days=None, repeat=True, playback=None):
    if days is None:
        days = ["Monday"]
    return Alarm(hour, minute, days, repeat, playback)

class AlarmTest(unittest.TestCase):

    def test_alarm_get_alarm_time(self):
        alarm = create_alarm(hour=6, minute=30)
        self.assertEqual(alarm.get_time(), datetime.time(6, 30))

    def test_alarm_get_alarm_day(self):
        alarm = create_alarm(days=["Monday"])
        self.assertTrue(alarm.is_day_active("Monday"))

    def test_alarm_throws_for_incorrect_days(self):
        self.assertRaises(ValueError, create_alarm, days=["Hello"])

    def test_alarm_can_store_multiple_days(self):
        alarm = create_alarm(days=["Wednesday", "Sunday"])
        self.assertTrue(alarm.is_day_active("Wednesday") &\
                        alarm.is_day_active("Sunday"))

    def test_alarm_returns_if_repeatable(self):
        alarm = create_alarm(repeat=True)
        self.assertTrue(alarm.is_repeating())

    # Figure out how to write a test that verifies the object
    def test_alarm_returns_playback_object(self):
        playback = mock.Mock()
        alarm = create_alarm(playback=playback)
        self.assertEqual(alarm.get_playback(), playback)

    def test_alarm_can_return_next_alarm_time(self):
        with mock.patch.object(datetime, 'datetime', mock.Mock(wraps=datetime.datetime)) as patched:
            patched.now.return_value = datetime.datetime(2019, 7, 21, 8, 0) #8am on Sunday
            alarm = create_alarm()
            self.assertEqual(alarm.find_next_alarm(), datetime.datetime(2019, 7, 22, 6, 30), True)

    def test_alarm_doesnt_return_today_if_time_has_passed(self):
        with mock.patch.object(datetime, 'datetime', mock.Mock(wraps=datetime.datetime)) as patched:
            patched.now.return_value = datetime.datetime(2019, 7, 23, 8, 0) #8am on Tuesday
            alarm = create_alarm(hour=6, minute=30, days=["Tuesday"])
            self.assertEqual(alarm.find_next_alarm(), datetime.datetime(2019, 7, 30, 6, 30))

    def test_alarm_throws_error_for_no_days(self):
        self.assertRaises(ValueError, create_alarm, days=[])
