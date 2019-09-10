
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
        self._snoozed = False

    def get_alarms(self):
        return dict(self._alarms)

    def create_alarm(self, name, new_alarm):
        self._alarms[name] = new_alarm
        self._scheduler.add_job(name, new_alarm.find_next_alarm(),\
            self._create_callback(name, new_alarm))

    def remove_alarm(self, name):
        self._alarms.pop(name, None)
        self._scheduler.remove_job(name)

    def get_next_alarm_time(self):
        return self._scheduler.get_next_job_time()

    def snooze(self):
        self._snoozed = True
        self._player.stop()

    def stop(self):
        self._player.stop()

    #TODO need to update alarm on main screen when creating new job
    def _create_callback(self, name, callback_alarm):
        def callback():
            ui.controller.UiController().set_screen("snooze")
            success = self._player.play(callback_alarm.get_playback())
            if success and self._snoozed:
                self._scheduler.add_job(name,\
                    datetime.datetime.now() + datetime.timedelta(minutes=1),\
                    self._create_callback(name, callback_alarm))
                self._snoozed = False
                return
            self._scheduler.add_job(name, callback_alarm.find_next_alarm(),\
                self._create_callback(name, callback_alarm))
        return callback
