
import datetime

class Alarm:
    """Alarm container

    Stores all the information required for an alarm including time, days,
    playback metadata and if the alarm is active
    """

    Weekdays = [
        "Monday", "Tuesday", "Wednesday", "Thursday",\
        "Friday", "Saturday", "Sunday"
    ]

    def __init__(self, hour, minute, days, playback, active):
        self._time = datetime.time(hour, minute)
        self._playback = playback
        self._active = bool(active)
        self._days = set()
        for day in days:
            self._days.add(self._check_day_is_valid(day))

    def get_time(self):
        """Returns the time for the alarm as datetime object"""
        return self._time

    def is_day_active(self, day):
        """Returns bool for if the given day is active. Day must be of the
        form displayed in the alarm.Weekdays list"""
        return day in self._days

    def get_playback(self):
        """Returns playback metadata as a dictonary. Details about valid
        keys and values can be found in the sound package"""
        return self._playback

    def is_active(self):
        """Returns bool of if alarm should be scheduled"""
        return self._active

    def find_next_alarm(self):
        """Returns datetime object for when alarm should next be triggered"""
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
        raise ValueError("Someone has broken the constructor (potentially no days!!!")
