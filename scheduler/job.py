import threading
import datetime

import utils.observer


class Job:
    """Basic job to be scheduled

    Job will emit a signal at the specified time unless the job has been
    killed. In order to receive the signal, subscribe using the class
    function subscribe

    To seperate job types, create a class that inherits this class
    and create a _local_complete class observer e.g.
    class NewJob(Job):
        _local_complete = utils.observer.Observer()
    This class should then be passed to scheduler when adding a new job
    """

    _complete = utils.observer.Observer()

    @classmethod
    def subscribe(cls, callback):
        """Subscribe to all job success and failure events. Callback
        should accept a uid (string) and success (bool) parameters.
        If Job is subclassed and has subclass _local_complete, it 
        will subscripe to that instead"""
        try:
            getattr(cls, "_local_complete").subscribe(callback)
        except:
            cls._complete.subscribe(callback)

    def __init__(self, uid, time):
        """Provide a unique identifier (uid) and the time that the job
        should trigger. This will create a thread that will count down to 
        notification"""
        self._uid = uid
        self._time = time
        self._event = threading.Event()
        threading.Thread(target=self._execute).start()

    def get_time(self):
        """Returns datetime for when the job will execute"""
        return self._time

    def kill(self):
        """Kills job which emits a job failure signal"""
        self._event.set()

    def _execute(self):
        time_till_alarm = self._time.timestamp() - datetime.datetime.now().timestamp()
        success = not self._event.wait(time_till_alarm)
        self._complete.notify(self._uid, success)
        try:
            getattr(self, "_local_complete").notify(self._uid, success)
        except:
            pass
