
import unittest
import datetime
# import time
import mock
import time

from alarm.scheduler import Scheduler

# Stop Job class from spinning up unneeded threads and waiting
@mock.patch("alarm.job.Job.start", mock.Mock())
class SchedulerTest(unittest.TestCase):

    def test_returns_none_for_time_when_no_job(self):
        self.assertIsNone(self.scheduler.get_next_job_time())

    def test_returns_time_for_submitted_job(self):
        self.scheduler.add_job("name", self.time, self.callback)
        self.assertEqual(self.scheduler.get_next_job_time(), self.time)

    def test_returns_nearest_job_time_for_two_submitted_jobs(self):
        first_time = self.time - datetime.timedelta(days=1)
        self.scheduler.add_job("nearest_job", first_time, self.callback)
        self.scheduler.add_job("furtherest_job", self.time, self.callback)
        self.assertEqual(self.scheduler.get_next_job_time(), first_time)

    def test_does_not_update_time_if_job_in_past(self):
        self.scheduler.add_job("past_job", datetime.datetime(1989, 12, 24), self.callback)
        self.assertIsNone(self.scheduler.get_next_job_time())

    def test_adding_job_runs_the_job(self):
        with mock.patch("alarm.job.Job.start") as start_method:
            self.scheduler.add_job("name", self.time, self.callback)
            start_method.assert_called_once()

    def test_adding_same_job_name_kills_old_job(self):
        with mock.patch("alarm.job.Job.kill") as kill_method:
            self.scheduler.add_job("same_name", self.time, self.callback)
            self.scheduler.add_job("same_name", self.time, self.callback)
            kill_method.assert_called_once()

    def test_removing_job_kills_the_job(self):
        with mock.patch("alarm.job.Job.kill") as kill_method:
            self.scheduler.add_job("remove_job", self.time, self.callback)
            self.scheduler.remove_job("remove_job")
            kill_method.assert_called_once()

    def test_destroy_scheduler_kills_all_jobs(self):
        with mock.patch("alarm.job.Job.kill") as kill_method:
            for i in range(5):
                self.scheduler.add_job("remove_job" + str(i), self.time, self.callback)
            self.scheduler.__del__()
            self.assertEqual(kill_method.call_count, 5)

    # Prevent the kill method trying to join a thread that is not there
    @mock.patch("alarm.job.Job.kill", mock.Mock())
    def test_removing_job_updates_next_time(self):
        remaining_time = self.time + datetime.timedelta(days=1)
        self.scheduler.add_job("job1", self.time, self.callback)
        self.scheduler.add_job("job2", remaining_time, self.callback)
        self.scheduler.remove_job("job1")
        self.assertEqual(self.scheduler.get_next_job_time(), remaining_time)

    def test_can_return_number_of_running_jobs(self):
        for i in range(3):
            self.scheduler.add_job("name" + str(i), self.time, self.callback)
        self.assertEqual(self.scheduler.get_num_jobs(), 3)

    # TODO: Figure out why this test doesn't work (even removing all patching)
    # def test_jobs_call_remove_job_callback_when_job_complete(self):
    #     self.scheduler.add_job("name", self.now, self.callback)
    #     time.sleep(0.01)
    #     self.assertEqual(self.scheduler.get_num_jobs(), 0)

    def __init__(self, *args, **kwargs):
        super(SchedulerTest, self).__init__(*args, **kwargs)
        self.scheduler = Scheduler()
        self.time = datetime.datetime(2222, 8, 21, 8, 23)
        self.now = datetime.datetime.now()
        self.callback = mock.Mock()
