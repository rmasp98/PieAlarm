
import threading
import datetime


class Job:
    """Basic job to be scheduled

    Expects a datetime for when the execution should occur and a
    callback function to executed at datetime. If datetime is in the
    past, callback will execute immediately

    Can optionally add a complete callback using Job.complete class
    variable that will execute when job is killed or has completed
    """

    # TODO: convert this into a signal
    complete = None

    def __init__(self, name, time, callback):
        """Should provide a time in the form of datetime and a callback
        function to be executed"""
        self._name = name
        self._callback = callback
        self._time = time
        self._event = threading.Event()
        self._thread = threading.Thread(target=self._execute)

    def get_time(self):
        return self._time

    def start(self):
        self._thread.start()

    def kill(self):
        self._event.set()

    def _execute(self):
        time_till_alarm = self._time.timestamp() - datetime.datetime.now().timestamp()
        if not self._event.wait(time_till_alarm):
            if callable(Job.complete):
                Job.complete(self._name)
            self._callback()
