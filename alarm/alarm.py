
import datetime

class Alarm:
    Weekdays = [
        "Monday", "Tuesday", "Wednesday", "Thursday",\
        "Friday", "Saturday", "Sunday"
    ]

    def __init__(self, hour, minute, days, repeat, playback):
        self._time = datetime.time(hour, minute)
        self._repeat = bool(repeat)
        self._playback = playback
        # if not days:
        #     raise ValueError("You have not assigned any days")
        self._days = set()
        for day in days:
            self._days.add(self._check_day_is_valid(day))

    def get_time(self):
        return self._time

    def is_day_active(self, day):
        return day in self._days

    def is_repeating(self):
        return self._repeat

    def get_playback(self):
        return self._playback

    def find_next_alarm(self):
        delta_days = self._find_days_till_next_alarm()
        alarm_time = datetime.datetime.now() + datetime.timedelta(days=delta_days)
        alarm_time = alarm_time.replace(hour=self._time.hour, \
            minute=self._time.minute, second=0)
        return alarm_time

    def _check_day_is_valid(self, day):
        if day in self.Weekdays:
            return day
        raise ValueError(str(day) + " is not an accepted day")

    def _find_days_till_next_alarm(self):
        now = datetime.datetime.now()
        for day_offset in range(8):
            if self.Weekdays[(now.weekday() + day_offset) % 7] in self._days:
                if day_offset != 0:
                    return day_offset
                elif now.time() < self._time:
                    return 0
        raise ValueError("Someone has broken the constructor!!!")
