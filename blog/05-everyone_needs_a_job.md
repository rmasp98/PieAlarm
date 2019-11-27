# Everyone needs a job

The first step needed in the scheduler part of the alarm application is creating the units of work that can be scheduled: the job. The job class itself will also need a small utility class called the observer class.


## Observer Class

Observers (or signals) allows an object to inform multiple other objects about an update. In the case of our alarm, it would allow the job objects to let everyone know that an alarm has just triggered. At the very least we want scheduler to know about the completion of the job so that it can clean it up; and the alarm manager so that it can trigger each aspect of an alarm (e.g. sound). All each of these objects have to do is subscribe to the signal with a function they want to be run when the job emits.

For the time being we are going to make the class very simple, it will have a function to subscribe, providing a callback function; and a function to emit, that will loop over the subscribers and call each callback function. We can later implement.

The simplest test we can probably write to start off with is a validation of the callback function when subscribing. If the callback parameter is not callable, then we should raise an exception. For the test we are simply going to provide a string to the subscribe function, which should not be callable (I hope...):
```python
def test_throws_if_callback_not_callable(self):
    observer = utils.observer.Observer()
    self.assertRaises(ValueError, observer.subscribe, "Hello")
```

Standard practice here of making sure the test runs and fails properly, which will involve creating the observer class and a subscribe function for it. Once that is working all we need to do at this point is raise an exception in the subscribe function to get the test to pass.

Next we want to check to see if our callback is actually called when we subscribe and call emit. For this we are going to use another function of a mock that we have not used yet and that is to detect function calls. We can pass a mock as our callback function and ask the mock if it ever gets called using the ``assert_called`` function:
```python
def test_callback_called_by_notify(self):
    observer = utils.observer.Observer()
    callback = mock.Mock()
    observer.subscribe(callback)
    observer.notify()
    callback.assert_called()
```

Now we need to do some more interesting stuff. We will need to store the callback function in an instance variable and then call it in emit. We also need to place an if around the exception to make sure it does not trigger when our callback is callable. Firstly the subscribe function should look a little like this:
```python
def subscribe(self, callback):
    if callable(callback):
        self._callback = callback
    else:
        raise ValueError("Callback must be a callable object")
```

We can thankfully use the callable function to determine is an object is callable. The emit function should now look like this:
```python
def notify(self):
    self._callback()
```

This code should make our tests pass (hopefully!). But it leaves us fairly limited. Only one object can subscribe to the observer class at a time. Next we are going to write a test that has multiple subscribers, and expect each one to be called on an emit:
```python
 def test_can_notify_multiple_objects(self):
    observer = utils.observer.Observer()
    callback1 = mock.Mock()
    observer.subscribe(callback1)
    callback2 = mock.Mock()
    observer.subscribe(callback2)
    observer.notify()
    callback1.assert_called()
    callback2.assert_called()
```

At the subscribe side, this is a relatively simple fix changing self._callback to a set (and renaming it to something a bit better). Then all we need to do on the emit side is look over all elements in the set and call the callbacks:
```python
for observer in self._observers:
    observer()
```

Now we want to make sure that we can pass information through the emit. In the case of the job, we probably need to give the scheduler and manager some information that identifies the job so that it can process it properly. Lets write a quick test that provides some UID in the notify function:
```python
def test_can_pass_arguments_to_objects(self):
    observer = utils.observer.Observer()
    callback = mock.Mock()
    observer.subscribe(callback)
    observer.notify("0000")
    arg_list = callback.call_args[0]
    # This is because we are using args and kwargs
    expected = ("0000",)
    self.assertEqual(arg_list, expected)
```

We can do this in multiple ways including hard-coding a specific number of parameters. However we are going to introduce yet another new concept (python is never ending!), which is ``*args`` and ``**kwargs``. You can see mention of this in the test.

Args and Kwargs are sort of like a template allowing a function to pass on arbitrary arguments to another function. In this case because the observer class is a high level class that has no concept of what arguments it should accept, it will accept anything expecting the callback functions to know what arguments to expect. I may get lots of people telling me this is bad practice but it does its job so I will keep it until I find  better way.

This is a very simple fix of just adding args and kwargs to both the parameters of the notify function and the parameters of the callback functions:
```python
def notify(self, *args, **kwargs):
    for observer in self._observers:
        observer(*args, **kwargs)
```

This should now make that test pass. The final test I want to write is one that raises an exception when a callback function receives the incorrect number of parameters (or more accurately an incorrect callback function is provided). This is a fairly simple test to write but again we will introduce a new concept: lambdas. This will allows us to create a simple inline function to provide to the subscribe function:
```python
def test_throws_error_if_object_expects_different_arguments_to_notify(self):
    observer = utils.observer.Observer()
    observer.subscribe(lambda arg1, arg2: print(arg1, arg2))
    self.assertRaises(ValueError, observer.notify, "0000")
```

Here the lambda keyword informs python that we are using a lambda (who would have thought), the following parts are the input variables to the lambda, then the code following the colon in the body of the lambda function. In this case we take two arguments and try to print them. This should throw an exception because the notify that follows only provides a single argument, but it will throw a ``TypeError`` where we want to throw a specific ``ValueError``.

In order to prevent the TypeError from ending the program, we need to place the calling on each callback function into a try-catch statement. We can then raise our own exception in the catch part of the statement:
```python
try:
    observer(*args, **kwargs)
except TypeError:
    raise ValueError(
        "Subscriber has not provided a function "
        "with correct number of arguments. Please check "
        "notifier to determine what is expected"
    )
```

That should hopefully get all of our tests to pass and gives us enough functionality for us to move onto the next class for the scheduler: the Job class.


## Job Class

The Job class is entirely responsible for making sure alarms trigger. For this we will provide a ``datetime`` object to tell it when to trigger (through a notification). As we want to be able to delete alarms, we need to introduce a way of interrupting the countdown, we need a way of identifying the job and we want a way of informing (through the notification) that the job was unsuccessful so that it doesn't accidentally trigger the alarm.

### Threading

The Job class will introduce a new concept, threading. Threading is the concept of running multiple bits of code simultaneously. This is required as we will have many jobs all counting down the time until they should execute as well as the main UI thread that keeps the user interface responding. This uses the threading library and is overall very simple to create but also very simple to introduce bugs. To find out more information about threading, look [here](https://realpython.com/intro-to-python-threading/). We only need a really simple use of the threading library that works as follows:
```python
thread = threading.Thread(target=<function-to-run>)
thread.start()
```

This code will run \<function-to-run> and when the function completes, the thread will be killed. I bugs in threading generally arise from multiple threads altering the same data. If this is done in the wrong order or if data that one thread is accessing is deleted by another thread, everything generally goes wrong. And a big warning, these bugs are incredibly difficult to find! So, whenever you start writing threaded code, try and keep it very simple and really think about the design to make sure these type of bugs don't arise.

Fortunately, for all the classes we have created so far, we do not need to worry about threading. This is because both the Alarm and Job classes are immutable (once created the data inside never changes), and the only data object in the Observer class is the ``_observers`` set but fortunately python sets are thread safe (I think). However, it means that all classes we make from now on, need to have threading kept in mind to ensure we don't accidentally introduce a race condition.

### Creates thread

Now onto the Job class. The first thing that we want to do is make sure that the job class creates a separate thread to wait in so that we do not stall that main thread. To do this we need to mock the ``Thread`` class and search for a call to start.
```python
@mock.patch("threading.Thread")
def test_creates_new_thread_to_run_in(self, thread_mock):
    alarm.job.Job("uid", datetime.datetime.now())
    thread_mock.return_value.start.assert_called()
```

Here you will notice that we provide a string and a ``datetime.datetime.now()`` object to the job constructor. This is because eventually we want to provide a unique identifier and the time it should execute to the job class, and I want to account for that now so that we don't have to rewrite all the tests later. To get this working we just need a pretty simple constructor running the threaded code we stated above:
```python
def __init__(self, uid, time):
    thread = threading.Thread(target=print)
    thread.start()
```

Because ``Thread`` requires a target, we just gave it a simple function, in this case print (which works surprisingly!). Next we want to allow interested classes to subscribe to notifications from the Job class. So we are going to mock the observer class to make sure the subscription method is called properly. 

### Subscription

A new concept we are going to introduce here is the class method. This is a method that is associated with the class rather than a specific object. The reason we want this is because we want interested parties to subscribe the Job notifications once and not to have to do it for every single job that is created. This can be seen in the test as the subscribe call is prefixed by the class name, rather than an object name:
```python
@mock.patch.object(utils.observer.Observer, "subscribe")
def test_can_subscribe_to_job_class(self, sub_mock):
    callback = mock.Mock()
    alarm.job.Job.subscribe(callback)
    sub_mock.assert_called_with(callback)
```

Here we need to create an class level observer object. This can be done by defining the variable outside of any functions within the class. The second step is to create a subscribe function, which will allow subscription to this new observer object. This function needs to be a class function which needs to be decorated with ``@classmethod``, and by social norms, name the first parameter cls to allow us to access class variables (e.g. the observer):
```python
_complete = utils.observer.Observer()
@classmethod
def subscribe(cls, callback):
    cls._complete.subscribe(callback)
```

### Notification

Now that we have the subscription set up, we want to make sure that a notification is sent out when the job is completed. We will assume the default state of a successful notification, as a failed notification needs explicit interference.
```python
def test_emits_success_signal_when_job_complete_successfully(self):
    signal = mock.Mock()
    alarm.job.Job.subscribe(signal)
    alarm.job.Job("uid", datetime.datetime.now())
    signal.assert_called_with("uid", True)
```

Now we need to set up the function that is started in the thread creating by the constructor. Lets do that first. So the line in the constructor should now read as:
```python
thread = threading.Thread(target=self._execute)
```

Also creating an empty function for ``execute``. Then putting into the ``execute`` function a call to the notify function of the observer object. As shown in the test this should give ``"uid"`` and ``True`` as the arguments:
```python
def _execute(self):
    self._complete.notify("uid", True)
```

A quick refactor can see us storing the ``"uid"`` passed to the constructor and using that in the notify call, to make it more adaptable to changing uid. Now that we have the job notifying, we have to deal with the problem that the class is notifying immediately, when it should be waiting until the supplied datetime has passed (admittedly we keep on passing now in so technically the time has passed but we know it will fail if we put a time in the future).

### Waiting

In order to facilitate this wait, we could calculate the time until the alarm should go off and then sleep that long. The problem with that is that the thread will become completely unresponsive, so if we decide to remove an alarm, we would have to kill the thread to stop it executing. This is not  very elegant solution but luckily other python schedulers have shown me a really clever way to do this and that is using an Event.wait. 

Event.wait will stop a thread until it receives a signal that it can continue. I hear you asking: "How does that help us?". The answer is because we can tell the function how long we want it to wait before giving up and moving on anyway. This therefore gives us an interruptible sleep. Cool, right? Unfortunately, the test for this is quite complicated. I will show it first and then explain each part:
```python
@mock.patch.object(threading.Event, "wait", return_value=False)
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
```

So the first complexity arises because we need to mock two things. The first is the ``Event.wait`` function, as we need to know if it has been called and we don't want the test to actually wait because this would make our tests unbearably long. The second is the ``datetime.now`` function, because we will be using that in the Job class to calculate how long we should wait. Unfortunately we would need to know that value **exactly** at the time it is called within the Job class in order to calculate the expected delay for the ``Event.wait`` function. Instead, we can mock the datetime.now (as we have previously) and set it to a static known value.

Next we create a ``job_time`` that is 10 seconds after our newly patched time and create a job with this time. However, you will notice that straight after that we put a sleep in. This is because we need to make sure that the patch for ``Event.wait`` is still active when we reach that it of code in the new thread. Also we want to make sure ``Event.wait`` is called before we run the assert called with. There is probably a more elegant way to do this, and I will be searching for it but for now, it will do.

So now we need to do two things in the ``_execute`` function. The first is to calculate the correct delay, and the second is to feed this into Event.wait. Calculating the delay is straightforward with one slightly new thing and that is the timestamp attribute of the datetime object. This returns the time in seconds since the epoch until the time given by the datetime object. This is a simple way of converting the two datetime objects (now and job time) into seconds and find the difference in seconds. There are probably other ways to do this but it works well for what we need. Then we simply need to call ``Event.wait`` with this calculated time:
```python
time_till_alarm = self._time.timestamp() - datetime.datetime.now().timestamp()
self._event.wait(time_till_alarm)
```

### Kill

Now that we have our delay, we are still missing something quite important and that is the ability to kill the job before it sends the successful notification. So lets write a test for that, where we provide a mock to the observer, create and alarm, kill the alarm and check to see if we get a failed notification.
```python
def test_emits_failed_signal_when_job_killed(self):
    signal = mock.Mock()
    alarm.job.Job.subscribe(signal)
    future_time = datetime.datetime.now() + datetime.timedelta(days=1)
    job = alarm.job.Job("uid", future_time)
    job.kill()
    # BODGE: Need to wait for notify to be called
    time.sleep(0.001)
    signal.assert_called_with("uid", False)
```

First the first thing we need to implement is the kill function, which will simply call the ``set`` in the ``Event`` object,  which will release the ``wait`` returning true from the function.
```python
def kill(self):
    self._event.set()
```

However, this still does not send a failed notification but we can do something quite clever. Instead of calling ``Event.wait``, then checking the return value in an if statement to decide what type of notification we should provide, we are simply going to provide the ``Event.wait`` as a parameter to the notify function. This will trigger the required delay before notify is called and will inject the return value of the wait straight into the notify function. Note we need to invert the return value because a return value of try means that an interrupt signal was received.
```python
self._complete.notify(self._uid, not self._event.wait(time_till_alarm))
```

Viola, we have a job class. The is one final bit of functionality we need to implement and that is a getter for the job time, as this will later be used by the scheduler to figure out which job will execute next. The final class should look a little like this:
```python
import threading
import datetime

import utils.observer


class Job:
    """Basic job to be scheduled

    Job will emit a signal at the specified time unless the job has been
    killed. In order to receive the signal, subscribe using the class
    function subscribe
    """

    _complete = utils.observer.Observer()

    @classmethod
    def subscribe(cls, callback):
        """Subscribe to all job success and failure events. Callback
        should accept a uid (string) and success (bool) parameters"""
        cls._complete.subscribe(callback)

    def __init__(self, uid, time):
        """Provide a unique identifier (uid) and the time that the job
        should trigger. This will create a thread that will count down to 
        notification"""
        self._uid = uid
        self._time = time
        self._event = threading.Event()
        job_thread = threading.Thread(target=self._execute)
        job_thread.start()

    def get_time(self):
        """Returns datetime for when the job will execute"""
        return self._time

    def kill(self):
        """Kills job which emits a job failure signal"""
        self._event.set()

    def _execute(self):
        time_till_alarm = self._time.timestamp() - datetime.datetime.now().timestamp()
        self._complete.notify(self._uid, not self._event.wait(time_till_alarm))
```
