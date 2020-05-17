import datetime
import types

import sound.player


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

    def __init__(self, hour, minute, days, playback, active):
        """Create alarm providing an integer for hour and minute, a list of days from 
        Alarm.Weekdays, playback to provide to player, and boolean for if the alarm is active"""
        self._time = datetime.time(hour, minute)
        if sound.player.Player.verify_sound_data(playback) == False:
            raise ValueError("Sound Metadata for alarm playback is not valid")
        self._playback = playback
        self._active = bool(active)
        self._days = set()
        if isinstance(days, (list, set)) and days:
            for day in days:
                self._days.add(self._check_day_is_valid(day))
        else:
            raise TypeError(
                "Not provided any days for alarm or provided incorrect type"
            )

    def time(self):
        """Returns the time for the alarm as datetime object"""
        return self._time

    def active_days(self):
        """Returns a set of active days in Weekdays format"""
        return set(self._days)

    def playback(self):
        """Returns playback metadata as a dictionary. Details about valid
        keys and values can be found in the sound package"""
        return self._playback

    def is_active(self):
        """Returns bool if alarm should be scheduled"""
        return self._active

    def find_next_alarm(self):
        """Returns datetime object for when alarm should next be triggered"""
        alarm_time = self._find_next_alarm_day()
        return alarm_time.replace(
            hour=self._time.hour, minute=self._time.minute, second=0, microsecond=0
        )

    def serialise(self):
        return {
            "hour": self._time.hour,
            "minute": self._time.minute,
            "days": list(self._days),
            "playback": self._playback,
            "active": self._active,
        }

    def _check_day_is_valid(self, day):
        if day in self.Weekdays:
            return day
        raise ValueError(str(day) + " is not an accepted day")

    def _find_next_alarm_day(self):
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
