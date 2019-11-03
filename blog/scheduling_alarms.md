# Scheduling alarms

Now that we have a class that stores all the information needed for an alarm, we need a class that we can use to trigger the alarm at the correct time. A good approach to that is to use a scheduler. Schedulers are responsible for executing work at a given time. In our case, this means informing us when the alarm time is so that we can trigger our alarm. I have decided to break this down into three classes:
* Job class: responsible for triggering the alarm at a given time
* Scheduler class: responsible for creating, deleting and managing each of the jobs
* Observer class: this will allow Jobs to inform Scheduler and anyone else interested that the alarm has triggered


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

The Job class will introduce a new concept, threading. Threading is the concept of running multiple bits of code simultaneously. This is required as we will have many jobs all counting down the time until they should execute as well as the main UI thread that keeps the user interface responding. This uses the threading library and is overall very simple to create but also very simple to introduce bugs. To find out more information about threading, look [here](https://realpython.com/intro-to-python-threading/). We only need a really simple use of the threading library that works as follows:
```python
thread = threading.Thread(target=<function-to-run>)
thread.start()
```

This code will run \<function-to-run> and when the function completes, the thread will be killed. I bugs in threading generally arise from multiple threads altering the same data. If this is done in the wrong order or if data that one thread is accessing is deleted by another thread, everything generally goes wrong. And a big warning, these bugs are incredibly difficult to find! So, whenever you start writing threaded code, try and keep it very simple and really think about the design to make sure these type of bugs don't arise.

Fortunately, for all the classes we have created so far, we do not need to worry about threading. This is because both the Alarm and Job classes are immutable (once created the data inside never change), the only data object in the Observer class is the ``_observers`` set but fortunately python sets are thread safe (I think). However, it means that all classes we make from now on, need to have threading kept in mind to ensure we don't accidentally introduce a race condition.





















