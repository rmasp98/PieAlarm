import datetime


class Alarm:
    """Alarm container

    Stores all the information required for an alarm including time, days,
    playback metadata and if the alarm is active
    """

    Weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    def __init__(self, hour=0, minute=0, days=None, playback=None, active=True):
        """Create alarm providing an integer for hour and minute, a list of days from 
        Alarm.Weekdays, playback to provide to player, and boolean for if the alarm is active"""
        self._time = datetime.time(hour, minute)
        self._playback = playback
        self._active = bool(active)
        self._days = set()
        if days is not None:
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
        """Returns playback metadata as a dictionary. Details about valid
        keys and values can be found in the sound package"""
        return self._playback

    def is_active(self):
        """Returns bool if alarm should be scheduled"""
        return self._active

    def find_next_alarm(self):
        """Returns datetime object for when alarm should next be triggered"""
        alarm_time = self._find_days_till_next_alarm()
        return alarm_time.replace(
            hour=self._time.hour, minute=self._time.minute, second=0, microsecond=0
        )

    def _check_day_is_valid(self, day):
        if day in self.Weekdays:
            return day
        raise ValueError(str(day) + " is not an accepted day")

    def _find_days_till_next_alarm(self):
        alarm_date = datetime.datetime.now()
        for _ in range(8):
            if self.Weekdays[alarm_date.weekday()] in self._days:
                if (
                    alarm_date.day != datetime.datetime.now().day
                    or alarm_date.time() < self._time
                ):
                    return alarm_date
            alarm_date = alarm_date + datetime.timedelta(days=1)
        raise ValueError("Alarm does not have any valid days enabled")
