import unittest
import unittest.mock as mock
import datetime
import time


import alarm.job


class JobTest(unittest.TestCase):
    @mock.patch("threading.Thread.start")
    def test_creates_new_thread_to_run_in(self, start_mock):
        alarm.job.Job("uid", datetime.datetime.now())
        start_mock.assert_called()

    @mock.patch("utils.observer.Observer.subscribe")
    def test_can_subscribe_to_job_class(self, sub_mock):
        callback = mock.Mock()
        alarm.job.Job.subscribe(callback)
        sub_mock.assert_called_with(callback)

    def test_emits_success_signal_when_job_complete_successfully(self):
        signal = mock.Mock()
        alarm.job.Job.subscribe(signal)
        alarm.job.Job("uid", datetime.datetime.now())
        signal.assert_called_with("uid", True)

    @mock.patch("threading.Event.wait", return_value=False)
    def test_calls_wait_with_time_till_alarm(self, mock_method):
        with mock.patch.object(
            datetime, "datetime", mock.Mock(wraps=datetime.datetime)
        ) as patched:
            patched.now.return_value = datetime.datetime.now()
            alarm_time = patched.now() + datetime.timedelta(seconds=10)
            alarm.job.Job("uid", alarm_time)
            # BODGE: Need to keep wait patch in scope until wait gets called in thread
            time.sleep(0.001)
            mock_method.assert_called_with(10.0)

    def test_emits_failed_signal_when_job_killed(self):
        signal = mock.Mock()
        alarm.job.Job.subscribe(signal)
        future_time = datetime.datetime.now() + datetime.timedelta(days=1)
        job = alarm.job.Job("uid", future_time)
        job.kill()
        # BODGE: Need to wait for notify to be called
        time.sleep(0.001)
        signal.assert_called_with("uid", False)
