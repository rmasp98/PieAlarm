import unittest
import datetime
import time
import threading
import mock

from alarm.job import Job


class JobTest(unittest.TestCase):
    @mock.patch.object(threading.Event, "wait", return_value=False)
    def test_calls_wait_with_time_till_alarm(self, mock_method):
        with mock.patch.object(
            datetime, "datetime", mock.Mock(wraps=datetime.datetime)
        ) as patched:
            patched.now.return_value = datetime.datetime(
                2019, 7, 23, 8, 0
            )  # 8am on Tuesday
            alarm_time = patched.now() + datetime.timedelta(seconds=10)
            job = create_job(dt=alarm_time)
            job.start()
            time.sleep(0.02)  # Bodge because it takes time to start a thread
            mock_method.assert_called_with(10.0)

    def test_emits_success_signal_when_job_complete_successfully(self):
        signal = mock.Mock()
        Job.subscribe(signal)
        job = create_job(uid="0000")
        job.start()
        signal.assert_called_with("0000", True)

    def test_emits_failed_signal_when_job_killed(self):
        signal = mock.Mock()
        Job.subscribe(signal)
        future_time = datetime.datetime.now() + datetime.timedelta(days=1)
        job = create_job(uid="0000", dt=future_time)
        job.start()
        job.kill()
        time.sleep(0.02)  # Bodge because it takes time to start a thread
        signal.assert_called_with("0000", False)


def create_job(uid="uid", dt=datetime.datetime.now()):
    return Job(uid, dt)
