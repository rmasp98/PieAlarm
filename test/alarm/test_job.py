
import unittest
import datetime
import time
import threading
import mock

from alarm.job import Job

def create_job(name="name", dt=datetime.datetime.now(), callback=mock.Mock()):
    return Job(name, dt, callback)

class JobTest(unittest.TestCase):

    def test_runs_callback_on_execute(self):
        callback = mock.Mock()
        job = create_job(callback=callback)
        job.start()
        callback.assert_called()

    def test_returns_job_time(self):
        job_time = datetime.datetime(2019, 8, 21, 8, 34)
        job = create_job(dt=job_time)
        self.assertEqual(job.get_time(), job_time)


    @mock.patch.object(threading.Event, 'wait', return_value=False)
    def test_calls_wait_with_time_till_alarm(self, mock_method):
        with mock.patch.object(datetime, 'datetime', mock.Mock(wraps=datetime.datetime)) as patched:
            patched.now.return_value = datetime.datetime(2019, 7, 23, 8, 0) #8am on Tuesday
            alarm_time = patched.now() + datetime.timedelta(seconds=10)
            job = create_job(dt=alarm_time, callback=mock.Mock())
            job.start()
            time.sleep(0.02) # Bodge because it takes time to start a thread
            mock_method.assert_called_with(10.0)

    def test_exits_without_calling_callback_on_kill(self):
        alarm_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
        callback = mock.Mock()
        job = create_job(dt=alarm_time, callback=callback)
        job.start()
        job.kill()
        callback.assert_not_called()

    def test_runs_callback_when_job_complete(self):
        Job.complete = mock.Mock()
        job = create_job(name="name")
        job.start()
        Job.complete.assert_called_with("name")
