import unittest
import datetime
import mock

from alarm.scheduler import Scheduler


class SchedulerTest(unittest.TestCase):
    @mock.patch("alarm.job.Job.start", mock.Mock())
    def test_returns_none_for_time_when_no_job(self):
        self.assertIsNone(self.scheduler.get_next_job_time())

    @mock.patch("alarm.job.Job.start", mock.Mock())
    def test_returns_time_for_submitted_job(self):
        self.scheduler.add_job(self.time)
        self.assertEqual(self.scheduler.get_next_job_time(), self.time)

    @mock.patch("alarm.job.Job.start", mock.Mock())
    def test_returns_nearest_job_time_for_two_submitted_jobs(self):
        first_time = self.time - datetime.timedelta(days=1)
        self.scheduler.add_job(first_time)
        self.scheduler.add_job(self.time)
        self.assertEqual(self.scheduler.get_next_job_time(), first_time)

    @mock.patch("alarm.job.Job.start", mock.Mock())
    def test_does_not_update_time_if_job_in_past(self):
        self.scheduler.add_job(datetime.datetime(1989, 12, 24))
        self.assertIsNone(self.scheduler.get_next_job_time())

    @mock.patch("alarm.job.Job.start", mock.Mock())
    def test_adding_job_runs_the_job(self):
        with mock.patch("alarm.job.Job.start") as start_method:
            self.scheduler.add_job(self.time)
            start_method.assert_called_once()

    @mock.patch("alarm.job.Job.start", mock.Mock())
    def test_adding_jobs_returns_uid_for_job(self):
        uid = self.scheduler.add_job(self.time)
        self.assertRegex(uid, "^[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}$")

    @mock.patch("alarm.job.Job.start", mock.Mock())
    def test_removing_job_kills_the_job(self):
        with mock.patch("alarm.job.Job.kill") as kill_method:
            uid = self.scheduler.add_job(self.time)
            self.scheduler.remove_job(uid)
            kill_method.assert_called_once()

    @mock.patch("alarm.job.Job.start", mock.Mock())
    def test_removing_job_updates_job_time(self):
        uid = self.scheduler.add_job(self.time)
        later_alarm = self.time + datetime.timedelta(days=1)
        self.scheduler.add_job(later_alarm)
        self.scheduler.remove_job(uid)
        self.assertEqual(self.scheduler.get_next_job_time(), later_alarm)

    @mock.patch("alarm.job.Job.start", mock.Mock())
    def test_destroy_scheduler_kills_all_jobs(self):
        with mock.patch("alarm.job.Job.kill") as kill_method:
            for _ in range(5):
                self.scheduler.add_job(self.time)
            self.scheduler.reset()
            self.assertEqual(kill_method.call_count, 5)

    @mock.patch("alarm.job.Job.start", mock.Mock())
    def test_can_return_number_of_running_jobs(self):
        for _ in range(3):
            self.scheduler.add_job(self.time)
        self.assertEqual(self.scheduler.get_num_jobs(), 3)

    def test_job_removed_when_complete(self):
        self.scheduler.add_job(datetime.datetime.now())
        self.assertEqual(self.scheduler.get_num_jobs(), 0)

    def __init__(self, *args, **kwargs):
        super(SchedulerTest, self).__init__(*args, **kwargs)
        self.scheduler = Scheduler()
        self.time = datetime.datetime(2222, 8, 21, 8, 23)
        self.now = datetime.datetime.now()
        self.callback = mock.Mock()
