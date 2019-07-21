
import unittest
import datetime
from alarm.alarm import Alarm


class AlarmTest(unittest.TestCase):

    def test_alarm_set_time_updates_time(self):
        alarm = Alarm()
        alarm.set_time(21, 45)
        self.assertEqual(datetime.time(21, 45), alarm.time)

    def test_alarm_can_track_an_added_day(self):
        alarm = Alarm()
        alarm.add_day("Monday")
        self.assertEqual(set([0]), alarm.days)

    def test_alarm_can_track_multiple_added_days(self):
        alarm = Alarm()
        alarm.add_day("Monday")
        alarm.add_day("Tuesday")
        self.assertEqual(set([0, 1]), alarm.days)

    def test_alarm_raises_if_not_valid_day(self):
        alarm = Alarm()
        with self.assertRaises(KeyError):
            alarm.add_day("Hello")

    def test_alarm_can_remove_day(self):
        alarm = Alarm()
        alarm.add_day("Monday")
        alarm.remove_day("Monday")
        self.assertEqual(set(), alarm.days)

    # def test_alarm_find_days_till_next_alarm(self):
    #     alarm = Alarm()
    #     alarm.add_day("Monday")


if __name__ == '__main__':
    unittest.main()
