import unittest
import unittest.mock as mock
import datetime

import scheduler.scheduler

time = datetime.datetime(2222, 8, 21, 8, 23)


class JobMock(scheduler.job.Job):
    pass


class SchedulerTest(unittest.TestCase):
    def test_returns_none_for_time_when_no_job(self):
        sched = scheduler.scheduler.Scheduler()
        self.assertIsNone(sched.get_next_job_time())

    @mock.patch("threading.Thread.start", mock.Mock())
    def test_returns_time_for_submitted_job(self):
        sched = scheduler.scheduler.Scheduler()
        sched.add_job(time)
        self.assertEqual(sched.get_next_job_time(), time)

    @mock.patch("threading.Thread.start", mock.Mock())
    def test_returns_nearest_job_time_for_two_submitted_jobs(self):
        sched = scheduler.scheduler.Scheduler()
        first_time = time - datetime.timedelta(days=1)
        sched.add_job(first_time)
        sched.add_job(time)
        self.assertEqual(sched.get_next_job_time(), first_time)

    @mock.patch("threading.Thread.start", mock.Mock())
    def test_does_not_update_time_if_job_in_past(self):
        sched = scheduler.scheduler.Scheduler()
        sched.add_job(datetime.datetime(1989, 12, 24))
        self.assertIsNone(sched.get_next_job_time())

    @mock.patch("threading.Thread.start", mock.Mock())
    def test_adding_jobs_returns_uid_for_job(self):
        sched = scheduler.scheduler.Scheduler()
        uid = sched.add_job(time)
        self.assertRegex(uid, "^[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}$")

    @mock.patch("scheduler.job.Job")
    def test_adding_job_runs_the_job(self, job_mock):
        sched = scheduler.scheduler.Scheduler()
        job_mock.return_value.get_time.return_value = time
        # Bodge because default parameter created before above patch
        with mock.patch.object(
            scheduler.scheduler.Scheduler.add_job, "__defaults__", (scheduler.job.Job,)
        ):
            uid = sched.add_job(time)
        job_mock.assert_called_with(uid, time)

    @mock.patch("scheduler.job.Job")
    def test_removing_job_kills_the_job(self, job_mock):
        sched = scheduler.scheduler.Scheduler()
        job_mock.return_value.get_time.return_value = time
        # Bodge because default parameter created before above patch
        with mock.patch.object(
            scheduler.scheduler.Scheduler.add_job, "__defaults__", (scheduler.job.Job,)
        ):
            uid = sched.add_job(time)
        sched.remove_job(uid)
        job_mock.return_value.kill.assert_called_once()

    @mock.patch("threading.Thread.start", mock.Mock())
    def test_removing_job_updates_job_time(self):
        sched = scheduler.scheduler.Scheduler()
        uid = sched.add_job(time)
        later_alarm = time + datetime.timedelta(days=1)
        sched.add_job(later_alarm)
        sched.remove_job(uid)
        self.assertEqual(sched.get_next_job_time(), later_alarm)

    def test_removing_non_existing_job_fails_silently(self):
        sched = scheduler.scheduler.Scheduler()
        try:
            sched.remove_job("Hello")
        except KeyError:
            self.fail("Should not have raised an exception")

    @mock.patch("scheduler.scheduler.Scheduler.remove_job")
    def test_job_removed_when_complete(self, remove_mock):
        sched = scheduler.scheduler.Scheduler()
        sched.add_job(datetime.datetime.now())
        remove_mock.assert_called()

    @mock.patch("scheduler.job.Job")
    def test_resetting_scheduler_kills_all_jobs(self, job_mock):
        sched = scheduler.scheduler.Scheduler()
        job_mock.return_value.get_time.return_value = time
        for _ in range(5):
            # Bodge because default parameter created before above patch
            with mock.patch.object(
                scheduler.scheduler.Scheduler.add_job,
                "__defaults__",
                (scheduler.job.Job,),
            ):
                sched.add_job(time)
        sched.reset()
        self.assertEqual(job_mock.return_value.kill.call_count, 5)

    @mock.patch("scheduler.test_scheduler.JobMock")
    def test_can_use_custom_job_class(self, job_mock):
        sched = scheduler.scheduler.Scheduler()
        job_mock.return_value.get_time.return_value = time
        sched.add_job(time, job_mock)
        job_mock.assert_called_once()
