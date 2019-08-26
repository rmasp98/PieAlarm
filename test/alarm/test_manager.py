
import unittest
import datetime
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

    def test_create_alarm_schedules_new_job(self):
        self.manager.create_alarm("test", self.alarm)
        self.scheduler.add_job.assert_called_once()

    def test_remove_alarm_remove_job_from_schedule(self):
        self.manager.create_alarm("test", self.alarm)
        self.manager.remove_alarm("test")
        self.scheduler.remove_job.assert_called_once_with("test")

    def test_can_get_next_alarm_time(self):
        self.manager.get_next_alarm_time()
        self.scheduler.get_next_job_time.assert_called_once()

    def test_snooze_stops_current_playback(self):
        self.manager.snooze()
        self.player.stop.assert_called_once()

    def test_create_alarm_creates_callback(self):
        with mock.patch("alarm.manager.Manager._create_callback") as create_callback:
            self.manager.create_alarm("test", self.alarm)
            create_callback.assert_called_once_with("test", self.alarm)

############################################################################
    # Have to access private function to test callback factory
    def test_callback_call_play_on_player(self):
        callback = self.manager._create_callback("test", self.alarm)
        callback()
        self.player.play.assert_called_once_with(self.alarm.get_playback())

    def test_callback_will_schedule_next_alarm_once_complete(self):
        callback = self.manager._create_callback("test", self.alarm)
        with mock.patch("alarm.manager.Manager._create_callback") as create_callback:
            callback()
            self.scheduler.add_job.assert_called_once_with("test",\
                self.alarm.find_next_alarm(), create_callback())

    def test_callback_will_schedule_alarm_after_snooze(self):
        callback = self.manager._create_callback("test", self.alarm)
        with mock.patch("alarm.manager.Manager._create_callback") as create_callback:
            self.manager.snooze()
            with mock.patch.object(datetime, 'datetime',\
                mock.Mock(wraps=datetime.datetime)) as patched:
                patched.now.return_value = datetime.datetime(2019, 7, 21, 8, 0) #8am on Sunday
                callback()
                self.scheduler.add_job.assert_called_once_with("test",\
                    datetime.datetime(2019, 7, 21, 8, 10), create_callback())

    def test_callback_will_schedule_next_alarm_if_playback_fails_while_snoozed(self):
        self.player.play.return_value = False
        callback = self.manager._create_callback("test", self.alarm)
        with mock.patch("alarm.manager.Manager._create_callback") as create_callback:
            self.manager.snooze()
            callback()
            self.scheduler.add_job.assert_called_once_with("test",\
                self.alarm.find_next_alarm(), create_callback())

################################################################################

    def __init__(self, *args, **kwargs):
        super(ManagerTest, self).__init__(*args, **kwargs)
        self.scheduler = mock.Mock()
        self.player = mock.Mock()
        self.player.play.return_value = True
        self.manager = Manager(self.scheduler, self.player)
        self.alarm = mock.Mock()


# tests
# Background job to check num jobs == num alarms
# schedule a callback internal to the manager class
# using player to play selected soundtrack
# snooze
# stop
# Should a boolean variable that defines if snooze has been pressed
