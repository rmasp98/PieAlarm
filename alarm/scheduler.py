
import datetime
import uuid

from alarm import job

class Scheduler:
    """Basic scheduler

    Accepts job object and a job name, which is added to a list and
    started immediately. Any jobs with the same name will kill and
    override old jobs.

    The class has four public functions:
     - get_next_job_time() returns the time of the next job to execute
     - get_num_jobs() returns number of active jobs
     - add_job(name, job) adds job to queue with name and starts
     - remove_job(name) kill name job and removes it from the list
    """

    def __init__(self):
        self._time = None
        self._jobs = {}
        job.Job.complete = self.remove_job

    def __del__(self):
        self._remove_all_jobs()

    def get_next_job_time(self):
        return self._time

    def get_num_jobs(self):
        return len(self._jobs)

    def add_job(self, time, callback):
        uid = str(uuid.uuid4())
        new_job = job.Job(uid, time, callback)
        # self.remove_job(name)
        self._jobs[uid] = new_job
        self._update_next_job_time()
        new_job.start()
        return uid

    def remove_job(self, uid):
        removed_job = self._jobs.pop(uid, None)
        if removed_job is not None:
            removed_job.kill()
            self._update_next_job_time()

    def _update_next_job_time(self):
        next_time = None
        for update_job in self._jobs.values():
            if update_job.get_time() > datetime.datetime.now() and \
                (next_time is None or update_job.get_time() < next_time):
                next_time = update_job.get_time()

        self._time = next_time

    def _remove_all_jobs(self):
        jobs = list(self._jobs.keys())
        for remove_job in jobs:
            self.remove_job(remove_job)
