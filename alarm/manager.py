import datetime
import time

import alarm.scheduler
import alarm.job
import sound.player
import ui.controller


class Manager:
    """Alarm Manager

    Maintains list of alarms controlling the scheduling and execution
    of the alarms. Scheduled alarms emit a signal captured by the class
    which triggers the playback of the signal and scheduling of the next
    alarm.

    It also manages change of screen to a snooze screen and back
    """

    def __init__(
        self,
        new_scheduler=alarm.scheduler.Scheduler(),
        new_player=sound.player.Player(),
    ):
        """Accpets new scheduler and player but this is largely for testing"""
        self._alarms = {}
        self._scheduler = new_scheduler
        self._player = new_player
        alarm.job.Job.subscribe(self._trigger_alarm)
        self._snoozed = 5
        self._snooze_time = 10
        self._focused_alarm = None

    def reset(self):
        """Clears alarm list and scheduled alarms. Largely for closing
        down application"""
        self._scheduler.reset()
        self._alarms = {}

    def get_alarms(self):
        """Returns set containing all stored alarms"""
        return_set = set()
        for return_alarm, _ in self._alarms.items():
            return_set.add(return_alarm)
        return return_set

    def create_alarm(self, new_alarm):
        """Accepts an alarm (of type alarm), adding to internal list and
        scheduling next alarm time"""
        if new_alarm.is_active():
            self._alarms[new_alarm] = self._scheduler.add_job(
                new_alarm.find_next_alarm()
            )
        else:
            self._alarms[new_alarm] = None

    def remove_alarm(self, remove_alarm):
        """Accepts an alarm (of type alarm), removing from internal list
        and removing from scheduler"""
        self._scheduler.remove_job(self._alarms.pop(remove_alarm, None))

    def get_next_alarm_time(self):
        """Gets the next time (of type datetime) an alarm is set to trigger"""
        return self._scheduler.get_next_job_time()

    def snooze(self, time):
        """Stop playback and set alarm to trigger again in 10 minutes"""
        if self._snoozed > 0:
            self._snooze_time = time
            self._snoozed = self._snoozed - 1
            self._player.stop()

    def stop(self):
        """Stop playback and set alarm to trigger on next alarm time"""
        self._snoozed = 0
        self._player.stop()

    def set_focused_alarm(self, focused_alarm):
        """A way of storing a specific alarm to interact with it in another
        location. Mainly used for communicating between view and edit screens"""
        self._focused_alarm = focused_alarm

    def get_focused_alarm(self):
        """Retrieve the set focused alarm"""
        return self._focused_alarm

    def _get_alarm_from_uid(self, uid):
        for get_alarm, get_uid in self._alarms.items():
            if get_uid == uid:
                return get_alarm

    def _trigger_alarm(self, uid, success):
        if success:
            play_alarm = self._get_alarm_from_uid(uid)
            if play_alarm is not None:
                ui.controller.UiController().set_screen("snooze")
                if self._player.play(play_alarm.playback()) and self._snoozed:
                    new_time = datetime.datetime.now() + datetime.timedelta(
                        minutes=self._snooze_time
                    )
                else:
                    self._snoozed = 5
                    new_time = play_alarm.find_next_alarm()
                self._alarms[play_alarm] = self._scheduler.add_job(new_time)
                ui.controller.UiController().set_screen("back")
