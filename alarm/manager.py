
import datetime

import alarm.scheduler
import sound.player
import ui.controller

class Manager:

    def __init__(self, new_scheduler=alarm.scheduler.Scheduler(),\
                       new_player=sound.player.Player()):
        self._alarms = {}
        self._scheduler = new_scheduler
        self._player = new_player
        self._snoozed = True
        self._focused_alarm = None

    def __del__(self):
        self._scheduler.__del__()

    def get_alarms(self):
        return dict(self._alarms)

    def create_alarm(self, new_alarm):
        self._alarms[new_alarm] = self._scheduler.add_job(
            new_alarm.find_next_alarm(), self._create_callback(new_alarm))

    def remove_alarm(self, remove_alarm):
        self._scheduler.remove_job(self._alarms.pop(remove_alarm, None))

    def get_next_alarm_time(self):
        return self._scheduler.get_next_job_time()

    def snooze(self):
        self._player.stop()

    def stop(self):
        self._snoozed = False
        self._player.stop()

    def set_focused_alarm(self, focused_alarm):
        self._focused_alarm = focused_alarm

    def get_focused_alarm(self):
        return self._focused_alarm

    def _create_callback(self, callback_alarm):
        def callback():
            ui.controller.UiController().set_screen("snooze")
            success = self._player.play(callback_alarm.get_playback())
            if success and self._snoozed:
                new_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
            else:
                new_time = callback_alarm.find_next_alarm()
                self._snoozed = True

            self._scheduler.add_job(new_time, self._create_callback(callback_alarm))
            ui.controller.UiController().set_screen("back")
        return callback
