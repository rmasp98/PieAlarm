import unittest
import mock

from utils.signal import Signal


class SignalTest(unittest.TestCase):
    def test_throws_if_callback_not_callable(self):
        signal = Signal()
        self.assertRaises(ValueError, signal.subscribe, 5)

    def test_callback_called_by_notify(self):
        signal = Signal()
        callback = mock.Mock()
        signal.subscribe(callback)
        signal.notify()
        callback.assert_called()

    def test_signal_can_notify_multiple_objects(self):
        signal = Signal()
        callback1 = mock.Mock()
        signal.subscribe(callback1)
        callback2 = mock.Mock()
        signal.subscribe(callback2)
        signal.notify()
        callback1.assert_called()
        callback2.assert_called()

    def test_signal_can_pass_arguments_to_objects(self):
        signal = Signal()
        callback = mock.Mock()
        signal.subscribe(callback)
        signal.notify("0000")
        arg_list = callback.call_args[0]
        # This is because we are using args and kwargs
        expected = ("0000",)
        self.assertEqual(arg_list, expected)

    def test_throws_error_if_object_expects_different_arguments_to_notify(self):
        signal = Signal()
        signal.subscribe(lambda arg1, arg2: print(arg1, arg2))
        self.assertRaises(ValueError, signal.notify, "0000")
