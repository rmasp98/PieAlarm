import unittest
import unittest.mock as mock

import utils.observer


class ObserverTest(unittest.TestCase):
    def test_throws_if_callback_not_callable(self):
        observer = utils.observer.Observer()
        self.assertRaises(ValueError, observer.subscribe, "Hello")

    def test_callback_called_by_notify(self):
        observer = utils.observer.Observer()
        callback = mock.Mock()
        observer.subscribe(callback)
        observer.notify()
        callback.assert_called()

    def test_can_notify_multiple_objects(self):
        observer = utils.observer.Observer()
        callback1 = mock.Mock()
        observer.subscribe(callback1)
        callback2 = mock.Mock()
        observer.subscribe(callback2)
        observer.notify()
        callback1.assert_called()
        callback2.assert_called()

    def test_can_pass_arguments_to_objects(self):
        observer = utils.observer.Observer()
        callback = mock.Mock()
        observer.subscribe(callback)
        observer.notify("0000")
        arg_list = callback.call_args[0]
        # This is because we are using args and kwargs
        expected = ("0000",)
        self.assertEqual(arg_list, expected)

    def test_throws_error_if_object_expects_different_arguments_to_notify(self):
        observer = utils.observer.Observer()
        observer.subscribe(lambda arg1, arg2: print(arg1, arg2))
        self.assertRaises(ValueError, observer.notify, "0000")
