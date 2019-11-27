import unittest
import datetime

import alarm.alarm


class AlarmTest(unittest.TestCase):
    def test_get_alarm_returns_correct_datetime_object(self):
        test_alarm = alarm.alarm.Alarm(hour=6, minute=30)
        self.assertEqual(test_alarm.time(), datetime.time(6, 30))

    def test_returns_true_if_day_is_active(self):
        test_alarm = alarm.alarm.Alarm(days=["Monday"])
        self.assertTrue(test_alarm.is_day_active("Monday"))

    def test_raises_exception_if_provided_day_not_valid(self):
        self.assertRaises(ValueError, alarm.alarm.Alarm, days=["Hello"])

    def test_can_store_multiple_days(self):
        test_alarm = alarm.alarm.Alarm(days=["Wednesday", "Sunday"])
        self.assertTrue(
            test_alarm.is_day_active("Wednesday") & test_alarm.is_day_active("Sunday")
        )

    # Figure out how to write a test that verifies the object
    def test_verifies_playback_object_is_valid(self):
        self.fail("Need to implement this!")

    def test_returns_correct_next_alarm_time(self):
        test_alarm = alarm.alarm.Alarm(6, 30, ["Monday"])
        self.assertEqual(test_alarm.find_next_alarm().time(), datetime.time(6, 30))

    def test_returns_correct_next_alarm_day(self):
        test_alarm = alarm.alarm.Alarm(6, 30, ["Wednesday"])
        self.assertEqual(test_alarm.find_next_alarm().weekday(), 2)

    def test_does_not_return_today_if_time_has_passed(self):
        with unittest.mock.patch.object(
            datetime, "datetime", unittest.mock.Mock(wraps=datetime.datetime)
        ) as patched:
            patched.now.return_value = datetime.datetime(
                2019, 7, 23, 8, 0
            )  # 8am on Tuesday
            test_alarm = alarm.alarm.Alarm(hour=6, minute=30, days=["Tuesday"])
            self.assertEqual(
                test_alarm.find_next_alarm(), datetime.datetime(2019, 7, 30, 6, 30)
            )

    def test_raises_if_no_days_in_alarm(self):
        test_alarm = alarm.alarm.Alarm(6, 30)
        self.assertRaisesRegex(
            ValueError,
            "Alarm does not have any valid days enabled",
            test_alarm.find_next_alarm,
        )
