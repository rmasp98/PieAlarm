
import alarm


class Manager:

    def __init__(self, scheduler=alarm.scheduler.Scheduler()):
        self._alarms = {}
        self._scheduler = scheduler

    def get_alarms(self):
        return dict(self._alarms)

    def create_alarm(self, name, new_alarm):
        self._alarms[name] = new_alarm

    def remove_alarm(self, name):
        self._alarms.pop(name, None)


    # def __init__(self, scheduler=alarm.scheduler.Scheduler):
    #     self._scheduler = scheduler

    # def create_alarm(self, name, new_alarm):
    #     new_job = alarm.job.Job(name, new_alarm.find_next_alarm(), None)
    #     self._scheduler.add_job(name, new_job)
