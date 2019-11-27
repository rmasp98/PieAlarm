import unittest
import unittest.mock as mock
import datetime

import alarm.scheduler


class SchedulerTest(unittest.TestCase):
    def test_returns_none_for_time_when_no_job(self):
        self.assertIsNone(self.scheduler.get_next_job_time())

    @mock.patch("threading.Thread.start", mock.Mock())
    def test_returns_time_for_submitted_job(self):
        self.scheduler.add_job(self.time)
        self.assertEqual(self.scheduler.get_next_job_time(), self.time)

    @mock.patch("threading.Thread.start", mock.Mock())
    def test_returns_nearest_job_time_for_two_submitted_jobs(self):
        first_time = self.time - datetime.timedelta(days=1)
        self.scheduler.add_job(first_time)
        self.scheduler.add_job(self.time)
        self.assertEqual(self.scheduler.get_next_job_time(), first_time)

    @mock.patch("threading.Thread.start", mock.Mock())
    def test_does_not_update_time_if_job_in_past(self):
        self.scheduler.add_job(datetime.datetime(1989, 12, 24))
        self.assertIsNone(self.scheduler.get_next_job_time())

    @mock.patch("threading.Thread.start", mock.Mock())
    def test_adding_jobs_returns_uid_for_job(self):
        uid = self.scheduler.add_job(self.time)
        self.assertRegex(uid, "^[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}$")

    @mock.patch("alarm.job.Job")
    def test_adding_job_runs_the_job(self, job_mock):
        job_mock.return_value.get_time.return_value = self.time
        uid = self.scheduler.add_job(self.time)
        job_mock.assert_called_with(uid, self.time)

    @mock.patch("alarm.job.Job")
    def test_removing_job_kills_the_job(self, job_mock):
        job_mock.return_value.get_time.return_value = self.time
        uid = self.scheduler.add_job(self.time)
        self.scheduler.remove_job(uid)
        job_mock.return_value.kill.assert_called_once()

    @mock.patch("threading.Thread.start", mock.Mock())
    def test_removing_job_updates_job_time(self):
        uid = self.scheduler.add_job(self.time)
        later_alarm = self.time + datetime.timedelta(days=1)
        self.scheduler.add_job(later_alarm)
        self.scheduler.remove_job(uid)
        self.assertEqual(self.scheduler.get_next_job_time(), later_alarm)

    def test_removing_non_existing_job_fails_silently(self):
        try:
            self.scheduler.remove_job("Hello")
        except KeyError:
            self.fail("Should not have raised an exception")

    @mock.patch("alarm.scheduler.Scheduler.remove_job")
    def test_job_removed_when_complete(self, remove_mock):
        self.scheduler.add_job(datetime.datetime.now())
        remove_mock.assert_called()

    @mock.patch("alarm.job.Job")
    def test_resetting_scheduler_kills_all_jobs(self, job_mock):
        job_mock.return_value.get_time.return_value = self.time
        for _ in range(5):
            self.scheduler.add_job(self.time)
        self.scheduler.reset()
        self.assertEqual(job_mock.return_value.kill.call_count, 5)

    def __init__(self, *args, **kwargs):
        super(SchedulerTest, self).__init__(*args, **kwargs)
        self.scheduler = alarm.scheduler.Scheduler()
        self.time = datetime.datetime(2222, 8, 21, 8, 23)

    #     self.now = datetime.datetime.now()
    #     self.callback = mock.Mock()
