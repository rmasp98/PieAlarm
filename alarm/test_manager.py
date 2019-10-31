import unittest
import datetime
import mock

from alarm.manager import Manager

# tests
# Background job to check num jobs == num alarms


class ManagerTest(unittest.TestCase):
    def test_returns_empty_alarms_set(self):
        self.assertSetEqual(self.manager.get_alarms(), set())

    def test_creating_alarm_adds_it_to_list(self):
        self.manager.create_alarm(self.alarm)
        self.assertSetEqual(self.manager.get_alarms(), set([self.alarm]))

    def test_can_add_multiple_alarms(self):
        self.manager.create_alarm(self.alarm)
        self.manager.create_alarm(mock.Mock())
        self.assertEqual(len(self.manager.get_alarms()), 2)

    def test_get_alarms_cannot_alter_interal_list(self):
        alarms = self.manager.get_alarms()
        alarms.add(self.alarm)
        self.assertEqual(len(self.manager.get_alarms()), 0)

    def test_remove_alarm_removes_alarm_from_list(self):
        self.manager.create_alarm(self.alarm)
        for alarm in self.manager.get_alarms():
            self.manager.remove_alarm(alarm)
        self.assertSetEqual(self.manager.get_alarms(), set())

    def test_create_alarm_schedules_new_job(self):
        self.manager.create_alarm(self.alarm)
        self.scheduler.add_job.assert_called_once()

    def test_remove_alarm_remove_job_from_scheduler(self):
        self.manager.create_alarm(self.alarm)
        for alarm in self.manager.get_alarms():
            self.manager.remove_alarm(alarm)
        self.scheduler.remove_job.assert_called_once()

    def test_can_get_next_alarm_time(self):
        self.manager.get_next_alarm_time()
        self.scheduler.get_next_job_time.assert_called_once()

    def test_inactive_alarm_does_not_add_job_to_scheduler(self):
        self.alarm.is_active.return_value = False
        self.manager.create_alarm(self.alarm)
        self.scheduler.add_job.assert_not_called()

    ##########################################################################
    # These call a private function to remove dependency on scheduler and job

    @mock.patch("ui.controller.UiController", mock.Mock())
    def test_nothing_called_if_job_returns_failed(self):
        self.manager.create_alarm(self.alarm)
        self.scheduler.reset_mock()
        self.manager._trigger_alarm(self.uid, False)
        self.player.play.assert_not_called()
        self.scheduler.add_job.assert_not_called()

    @mock.patch("ui.controller.UiController", mock.Mock())
    def test_trigger_alarm_calls_play_on_player(self):
        self.manager.create_alarm(self.alarm)
        self.manager._trigger_alarm(self.uid, True)
        self.player.play.assert_called_once_with(self.alarm.get_playback())

    @mock.patch("ui.controller.UiController", mock.Mock())
    def test_trigger_alarm_snoozes_by_default(self):
        self.manager.create_alarm(self.alarm)
        self.scheduler.reset_mock()
        with mock.patch.object(
            datetime, "datetime", mock.Mock(wraps=datetime.datetime)
        ) as patched:
            patched.now.return_value = datetime.datetime(
                2019, 7, 21, 8, 0
            )  # 8am on Sunday
            self.manager._trigger_alarm(self.uid, True)
            self.scheduler.add_job.assert_called_once_with(
                datetime.datetime(2019, 7, 21, 8, 10)
            )

    @mock.patch("ui.controller.UiController", mock.Mock())
    def test_trigger_alarm_schedules_next_alarm_if_stop_called(self):
        self.manager.create_alarm(self.alarm)
        self.scheduler.reset_mock()
        self.manager.stop()
        self.manager._trigger_alarm(self.uid, True)
        self.scheduler.add_job.assert_called_once_with(self.alarm.find_next_alarm())

    @mock.patch("ui.controller.UiController", mock.Mock())
    def test_trigger_alarm_schedules_next_alarm_if_playback_fails(self):
        self.manager.create_alarm(self.alarm)
        self.scheduler.reset_mock()
        self.player.play.return_value = False
        self.manager._trigger_alarm(self.uid, True)
        self.scheduler.add_job.assert_called_once_with(self.alarm.find_next_alarm())

    @mock.patch("ui.controller.UiController", mock.Mock())
    def test_rescheduled_alarm_can_be_removed(self):
        self.manager.create_alarm(self.alarm)
        self.scheduler.add_job.return_value = "new_uid"
        self.manager._trigger_alarm(self.uid, True)
        self.manager.remove_alarm(self.alarm)
        self.scheduler.remove_job.assert_called_once_with("new_uid")

    @mock.patch("ui.controller.UiController")
    def test_trigger_alarm_changes_screen_to_snooze_screen_and_back(
        self, controller_mock
    ):
        self.manager.create_alarm(self.alarm)
        self.manager._trigger_alarm(self.uid, True)
        controller_mock.return_value.set_screen.assert_has_calls(
            [mock.call("snooze"), mock.call("back")], any_order=False
        )

    ################################################################################

    def test_snooze_stops_current_playback(self):
        self.manager.snooze()
        self.player.stop.assert_called_once()

    def test_stop_stops_current_playback(self):
        self.manager.stop()
        self.player.stop.assert_called_once()

    def test_returns_none_if_no_alarm_focused(self):
        self.assertIsNone(self.manager.get_focused_alarm())

    def test_can_set_an_alarm_to_focus(self):
        self.manager.set_focused_alarm(self.alarm)
        self.assertEqual(self.manager.get_focused_alarm(), self.alarm)

    def test_calling_reset_calls_scheduler_reset(self):
        self.manager.reset()
        self.scheduler.reset.assert_called_once()

    def __init__(self, *args, **kwargs):
        super(ManagerTest, self).__init__(*args, **kwargs)
        self.uid = "uid"
        self.scheduler = mock.MagicMock()
        self.scheduler.add_job.return_value = self.uid
        self.player = mock.Mock()
        self.player.play.return_value = True
        self.manager = Manager(self.scheduler, self.player)
        self.alarm = mock.Mock()
