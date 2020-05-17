import datetime
import time

import ui
from scheduler.scheduler import Scheduler
from scheduler.job import Job
from scheduler.observer import Observer
from sound.player import Player
from settings.settings import AlarmSettings
from alarm.alarm import Alarm


class AlarmJob(Job):
    _local_complete = Observer()


class Manager:
    """Alarm Manager

    Maintains list of alarms controlling the scheduling and execution
    of the alarms. Scheduled alarms emit a signal captured by the class
    which triggers the playback of the signal and scheduling of the next
    alarm.

    It also manages change of screen to a snooze screen and back
    """

    def __init__(
        self, settings, new_scheduler=Scheduler(), new_player=Player(),
    ):
        """Accpets new scheduler and player but this is largely for testing"""
        self._alarms = {}
        self._snooze_time = 10
        self._snoozed = self._default_snoozed = 5
        self._settings = settings
        AlarmSettings.connect(self._update_alarm_setting)
        self._scheduler = new_scheduler
        self._player = new_player
        AlarmJob.subscribe(self._trigger_alarm)

    def reset(self):
        """Clears alarm list and scheduled alarms. Largely for closing
        down application"""
        self._scheduler.reset()
        self._alarms = {}

    def get_alarms(self):
        """Returns set containing all stored alarms"""
        return set(self._alarms.keys())

    def create_alarm(self, new_alarm):
        """Accepts an alarm (of type alarm), adding to internal list and
        scheduling next alarm time"""
        if new_alarm.is_active():
            self._alarms[new_alarm] = self._schedule_alarm(new_alarm.find_next_alarm())
        else:
            self._alarms[new_alarm] = None
        self._save_alarms()

    def remove_alarm(self, remove_alarm):
        """Accepts an alarm (of type alarm), removing from internal list
        and removing from scheduler"""
        self._scheduler.remove_job(self._alarms.pop(remove_alarm, None))
        self._save_alarms()

    def get_next_alarm_time(self):
        """Gets the next time (of type datetime) an alarm is set to trigger"""
        return self._scheduler.get_next_job_time()

    def snooze(self):
        """Stop playback and set alarm to trigger again in 10 minutes"""
        if self._snoozed > 0:
            self._player.stop()

    def stop(self):
        """Stop playback and set alarm to trigger on next alarm time"""
        self._snoozed = 0
        self._player.stop()

    def _get_alarm_from_uid(self, uid):
        for get_alarm, get_uid in self._alarms.items():
            if get_uid == uid:
                return get_alarm

    def _schedule_alarm(self, time):
        return self._scheduler.add_job(time, AlarmJob)

    def _trigger_alarm(self, uid, success):
        if success:
            play_alarm = self._get_alarm_from_uid(uid)
            if play_alarm is not None:
                ui.Ctrl().set_screen(ui.Screen.SNOOZE)
                if self._player.play(play_alarm.playback()) and self._snoozed:
                    self._snoozed = self._snoozed - 1
                    new_time = datetime.datetime.now() + datetime.timedelta(
                        minutes=self._snooze_time
                    )
                else:
                    self._snoozed = self._default_snoozed
                    new_time = play_alarm.find_next_alarm()
                self._alarms[play_alarm] = self._schedule_alarm(new_time)
                ui.Ctrl().back()

    def _save_alarms(self):
        self._settings.update_setting(
            "Alarm", "Alarms", [a.serialise() for a in self._alarms.keys()], False
        )
        self._settings.save()

    def _update_alarm_setting(self, setting, value):
        if setting == "Snooze Time":
            self._snooze_time = value
        elif setting == "No. of Snoozes":
            self._snoozed = self._default_snoozed = value
        elif setting == "Alarms":
            for new_alarm in value:
                self.create_alarm(
                    Alarm(
                        new_alarm["hour"],
                        new_alarm["minute"],
                        new_alarm["days"],
                        new_alarm["playback"],
                        new_alarm["active"],
                    )
                )
