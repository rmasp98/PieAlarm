import threading
import datetime

import utils.observer


class Job:
    """Basic job to be scheduled

    Job will emit a signal at the specified time unless the job has been
    killed. In order to receive the signal, subscribe using the class
    function subscribe
    """

    _complete = utils.observer.Observer()

    @classmethod
    def subscribe(cls, callback):
        """Subscribe to all job success and failure events. Callback
        should accept a uid (string) and success (bool) parameters"""
        cls._complete.subscribe(callback)

    def __init__(self, uid, time):
        """Provide a unique identifier (uid) and the time that the job
        should trigger. This will create a thread that will count down to 
        notification"""
        self._uid = uid
        self._time = time
        self._event = threading.Event()
        job_thread = threading.Thread(target=self._execute)
        job_thread.start()

    def get_time(self):
        """Returns datetime for when the job will execute"""
        return self._time

    def kill(self):
        """Kills job which emits a job failure signal"""
        self._event.set()

    def _execute(self):
        time_till_alarm = self._time.timestamp() - datetime.datetime.now().timestamp()
        self._complete.notify(self._uid, not self._event.wait(time_till_alarm))
