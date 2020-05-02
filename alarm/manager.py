import datetime
import time

import scheduler.scheduler
import sound.player
import ui
import scheduler.observer


class AlarmJob(scheduler.job.Job):
    _local_complete = scheduler.observer.Observer()


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
        new_scheduler=scheduler.scheduler.Scheduler(),
        new_player=sound.player.Player(),
    ):
        """Accpets new scheduler and player but this is largely for testing"""
        self._alarms = {}
        self._scheduler = new_scheduler
        self._player = new_player
        AlarmJob.subscribe(self._trigger_alarm)
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
            self._alarms[new_alarm] = self._schedule_alarm(new_alarm.find_next_alarm())
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
                    self._snoozed = 5
                    new_time = play_alarm.find_next_alarm()
                self._alarms[play_alarm] = self._schedule_alarm(new_time)
                ui.Ctrl().back()
