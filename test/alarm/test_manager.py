
import unittest
import mock

from alarm.manager import Manager

class ManagerTest(unittest.TestCase):

    def test_returns_empty_alarms_dict(self):
        self.assertDictEqual(self.manager.get_alarms(), {})

    def test_creating_alarm_adds_it_to_list(self):
        self.manager.create_alarm("test", self.alarm)
        self.assertDictEqual(self.manager.get_alarms(), {"test":self.alarm})

    def test_get_dict_cannot_alter_interal_dict(self):
        get_dict = self.manager.get_alarms()
        get_dict["test"] = self.alarm
        self.assertNotEqual(self.manager.get_alarms(), get_dict)

    def test_remove_alarm_removes_alarm_from_list(self):
        self.manager.create_alarm("test", self.alarm)
        self.manager.remove_alarm("test")
        self.assertDictEqual(self.manager.get_alarms(), {})

    # def test_create_alarm_schedules_new_job(self):
    #     scheduler = mock.Mock()
    #     manager = Manager(scheduler)
    #     manager.create_alarm("test", self.alarm)
    #     scheduler.add_job.assert_called_once_with(self.alarm.get_time, self.alarm.get_callback)

    # def test_create_alarm_schedules_job(self):
    #     sched = mock.Mock()
    #     manager = Manager(sched)
    #     alarm = Alarm(22, 35, ["Monday"], True, mock.Mock())
    #     manager.create_alarm("name", alarm)
    #     # sched.add_job.

    # def test_can_get_list_of_active_alarms(self):

    def __init__(self, *args, **kwargs):
        super(ManagerTest, self).__init__(*args, **kwargs)
        self.manager = Manager()
        self.alarm = mock.Mock()


# tests
# create alarm
#   add alarm to list/dictionary - done
#   add alarm to scheduler
# edit alarm
#   remove alarm from scheduler
#   replace alarm in list/dictionary
# remove alarm
#   remove alarm from scheduler
#   remove alarm from list/dictionary - done
# get alarms
#   return dictionary of alarms - done
# get next alarm
#   return scheduler.get_next_job)time()
# Background job to check num jobs == num alarms
