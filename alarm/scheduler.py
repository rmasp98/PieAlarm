import datetime
import uuid

import alarm.job


class Scheduler:
    """Basic scheduler

    Accepts a time to schedule a job, which is added to a list and
    started immediately. Each job is assigned a uid which is returned
    to calling function. Job is then removed upon completion
    """

    def __init__(self):
        self._time = None
        self._jobs = {}
        alarm.job.Job.subscribe(self._job_complete)

    def get_next_job_time(self):
        """Returns time (as datetime) of soonest job to execute"""
        return self._time

    def add_job(self, time):
        """Accepts a datetime object for when job will execute.
        Jobs in past will execute immediately"""
        uid = str(uuid.uuid4())
        self._jobs[uid] = alarm.job.Job(uid, time)
        self._update_next_job_time()
        return uid

    def remove_job(self, uid):
        """If job exists in list, it will be killed and removed from list"""
        removed_job = self._jobs.pop(uid, None)
        if removed_job is not None:
            removed_job.kill()
            self._update_next_job_time()

    def reset(self):
        """This will ensure that all job threads are killed of at the end"""
        jobs = list(self._jobs.keys())
        for remove_job in jobs:
            self.remove_job(remove_job)

    def _update_next_job_time(self):
        next_time = None
        for update_job in self._jobs.values():
            if update_job.get_time() > datetime.datetime.now() and (
                next_time is None or update_job.get_time() < next_time
            ):
                next_time = update_job.get_time()

        self._time = next_time

    def _job_complete(self, uid, _):
        self.remove_job(uid)
