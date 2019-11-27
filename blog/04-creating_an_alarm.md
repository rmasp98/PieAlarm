# Creating an alarm

Now that we have a basis for the application upon which we can build, we need to work on the alarm part of an alarm clock.

There is a reasonable chance I have over complicated this but here is how I plan to design the alarm part of the alarm clock:
* Alarm - this will contain all the required information for a single alarm
* Manager - this will hold all the alarms and cover other aspects such as scheduling and playing each alarm
* Scheduler - this will be responsible for tracking each of the alarm times and triggering when the alarm time is reached
* Player - the alarms are sounds so we need something to play the sounds

For this installment we will be  purely focusing on the alarm class. However, before we delve into this exciting world, I should probably introduce you to a very good development practice call test driven development (TDD). 

## TDD

[Test driven development](https://en.wikipedia.org/wiki/Test-driven_development) is the concept of writing tests before you write code. Essentially you write a test that demonstrates a small piece of functionality you want in your code. When you first run this test, it should fail as we have not implemented that functionality yet. Then we write the minimum amount of code required to make the test pass.

Once this test passes, you can then take time to look back at the code you have written and tidy it up making sure you follow best practice. You can then rerun the tests to ensure you have not broken anything. Once this process is complete, you then start with your next test/piece of functionality.

There are many great advantages to this approach such as better overall code, but the thing I like most is the confidence it gives me when changing code that I have not broken anything. And at the end you have a set of tests that both demonstrate and document the capability of the code.

There are generally two sides to a test. The testing framework which can be used to write the test. For this project I will be using the unittest library. The second is the test runner, which is responsible for finding and running all the tests in the project, which will be nose. There are other frameworks and runners so if you don't like these you can happily use alternatives.

The basics for using unittest and nose, is that all test cases (a python class) should end with Test (e.g. AlarmTest) and should inherit from unittest.TestCase; and all tests (functions in the test case) should begin with test_ (e.g. test_get_alarm_time()). Most of this should hopefully become a bit more clear in the next section.

## The Alarm class

The first thing we want to do is create a new package called alarm. To do this, create a folder called alarm and then inside that folder create two files: one called ``alarm.py`` and the other called ``__init__.py``. The ``__init__.py`` file can give information about the package such as files to import. However, we don't need any of that yet so we will leave it empty.

Next, insert the following bare-bones into the ``alarm.py`` file for the alarm class:
```python
class Alarm:
    pass
```

Now create another file called ``test_alarm.py`` and insert the following test code below:
```python
import unittest

class AlarmTest(unittest.TestCase):
    def test_my_first_test(self):
        pass
``` 

We can now run the tests. If all is well, you can select the test tube looking button on the far left. This is the testing tab and if you are lucky, you will see your test listed in there. If not you may need to install nose and configure it with VS Code. To install nose, following the standard pip install command:
```python
.venv/bin/pip install nose
```

Then pressing Ctrl+Shift+P to bring up the VS Code command. Then type ``python:configure tests``, choose nose and then choose the root directory. This should then populate your tests. To run all the tests, simply press the green arrow at the top of the test sidebar. You can also click on on the green arrows for test cases or even individual tests.

Hopefully, we should see that one test has passed. This is because in order to make a test fail, you need to run a check that fails which can be achieved using the self.Assert* functions. These include things like two objects being equal to each other. You can see this affect by replacing pass in the above test with the following code:
```python
self.assertEqual(1, 2)
```

This code is asserting that one is equal to two which is clearly correct right... Well when we run the test we get test failed because one does not equal two. Who would have thought.

### get_time()

Now onto an actual test that we would like to write. So we will start with something simple. Can the alarm return the alarm time. Generally you could not write tests for what are called getters and setters (functions that get or set the value of a private variable in the class). However, we intend to do something special with this and that is return a different object to what is given to the class. In this case, we will provide two integers (one for hours and one for minutes) to the class but expect a datetime.time object in return.

The logic behind this is that when a user is setting the time for the alarm, they are likely to set the hour and the minutes as two separate inputs. However, all other interaction with time will be using datetime objects (pythons built in type that stores dates and time). This will likely make much more sense when we create the alarm edit screen but for now you may have to trust me.

So on to the test. We need to provide the alarm class with two numbers (hour and minute) and will expect the alarm to return this as a datetime.time version of that time. This can be written as follows:
```python
def test_get_alarm_returns_correct_datetime_object(self):
    alarm = alarm.alarm.Alarm(6, 30)
    self.assertEqual(datetime.time(6, 30), test_alarm.get_time())
```

Running quickly through this code, we have the function name, which starts with test and describes succinctly what the test is doing. Next we create an alarm object giving it the time 06:30. Finally we retrieve the time from the alarm object and compare this to a datetime.time object that is set to 06:30.

Firstly, you are going to get an error in the test. This is because we have not imported datetime or Alarm. Then we are going to get an error saying that Alarm takes no arguments and will get an error telling you that Alarm has no attribute get_time. We can quickly solve both those latter problems with the following functions in the Alarm class. To note we have added default values for hour and minutes, so that we can easily make a default alarm:
```python
def __init__(self, hour=0, minute=0):
    pass

def get_time(self):
    pass
```

Now we will start getting proper errors. It should now return that None != datetime.time(6, 30). That is because we are not returning any values in the function get_time and by default, if nothing is returned by a function, it will return None. The minimum amount of code we require to get this test to pass is by returning the hard-coded value we require. This seems relative unintuitive as we know this will never be what we want in the end but this approach is supposed to help with trying to keep code as minimal and simple as possible.
```python
def get_time(self):
```

Rerunning the test will return success. We have now written our first bit of functionality. However, you are probably painfully aware that this will fail very quickly. So on to our next test:
```python
def test_get_alarm_returns_correct_datetime_object_for_different_time(self):
    test_alarm = alarm.alarm.Alarm(18, 45)
    self.assertEqual(datetime.time(18, 45), test_alarm.get_time())
```

Now we have introduced some complexity to the function. We can no longer hard-code the return because that would make the original test fail. We could potentially switch statement, but sometimes you can fast forward these solutions and we know that we would have to make thousands of cases. So we now fall down to storing the value given in the constructor and returning that in the get_time function

There are two ways that we can do this. We can either convert it to a datetime object when the class is constructed or when we return time. It does not make a huge amount of difference. Storing a datetime object would take more memory than the original two integers but converting to a datetime object on every get would take more processing. However, it is unlikely that our alarm application will ever struggle for memory nor processing power. I have chosen to store as a datetime object
```python
def __init__(self, hour=0, minute=0):
    self._time = datetime.time(hour, minute)

def get_time(self):
    return self._time
```

Now when we run the tests, we get that both have passed. Now for another unintuitive step. We are going to delete the second test. Now that we have the main functionality, we don't really need both tests as we are highly unlikely to regress this functionality. We only need to keep tests that either provide unique testing for given functionality or provides useful documentation on how to use the class. As the second does neither, we will remove it and move onto our next test.

### is_day_active()

Next we want to focus on the enabled days for the alarm. Here I have decided to provide a function where the user will provide a day and the function will return true if the day is enabled, otherwise false. We will also introduce a new constructor parameter, days. Our first test will provide a day to the days parameter and test that the day returns true:
```python
def test_returns_true_if_day_is_active(self):
    test_alarm = alarm.alarm.Alarm(days=["Monday"])
    self.assertTrue(test_alarm.is_day_active("Monday"))
```

So again we are going to have a few silly errors to do with missing parameter in the constructor and no is_day_active function. I will leave you to figure out how to get up to the real errors. And again we will come up to the problem of hard-coding and then building the functionality until we get the functionality that we require. I think overall you get the idea of the process.

Overall the simplest form to solve this problem in a dynamic way (can accept multiple different days) is to simply store the contents of the days parameter is a instance variable array. Then check for the existence of the day provided in the ``is_day_active`` function inside this array. This would look largely like below:
```python
def __init__(self, hour=0, minute=0, days=[]):
    ...
    self._days = days

def is_day_active(self, day):
    return day in self._days
```

Note that apparently using an empty array as a default variable is bad practice, so we will be changing that as soon as I have figured out how... The new concept here is probably the ``in`` keyword. This allows you to check for the existence of an element in the array, returning true if it is in there. Running out test you should see it now passing but this does not sit right with me. 

Currently a user could store the string ``'monkey'`` and check if that is active and it would return true. Probably the larger problem would be if one part of the application stored ``'Monday'`` and another checked to see if ``'monday'`` was active. This would return false because the case is not correct. We can approach this in two different ways. We can create a clever function that can account for all the different variations on a day (e.g. m, MO, mon, etc) or we can limit what can be provided to a subset of those choices. I have decided to go with the former as it feels a little cleaner.

Firstly we need to create a test that for what we want to happen. In this case we want to raise an error if an incorrect day is provided to the constructor fo the alarm. We can do this with the following test:
```python
def test_raises_exception_if_provided_day_not_valid(self):
        self.assertRaises(ValueError, alarm.alarm.Alarm, days=["Hello"])
```

Here we have introduced a new concept: raise. This is called an exception, which tells the program that something has gone wrong. It will then throw a hissy fit and crash the program unless the exception is handled correctly. In this case someone has provided an invalid day into our alarm class so we want to let them know immediately that this is bad so will crash the program. 

An instance of when you might want to catch this exception and stop it crashing is if the user is able to type the day (a little strange I know). In this case we would not want to crash the program but simply catch the exception and display an error to the user informing them of their idiocy. This could be achieved with the below code:
```python
try:
    check_day_is_valid(user_input_day)
except (ValueError):
    create_error_dialog("You have input an incorrect value for day")
```

However, that would be the responsibility of the user interface to ensure that the exception is handled correctly. Admittedly that will be us soon but that is for future us to worry about.

So now we need to create the subset of days we discussed earlier, have a way of validating the input against it and then populating ``self._days`` with the validated input. I decided to store the subset in an array as a class variables, where the index follows the indexing of weekdays in ``datetime.weekday()``. This will make sense a bit later.
```python
Weekdays = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]
```

Then we can create a validate days function that follows a very similar approach to the ``is_day_active`` function:
```python
def _check_day_is_valid(self, day):
    if day in self.Weekdays:
        return day
    raise ValueError(str(day) + " is not an accepted day")
```

Here we introduce another new concept: naming convention. You will notice that there is an underscore before the name. This tells other developers that this function is for use within the class only and should not be used outside the class. I have decided to do this because I would prefer the use of Weekdays to be other users source of truth for correct days rather than this function.

Finally we need to check the input days in the constructor with our new function:
```python
for day in days:
    self._days.add(self._check_day_is_valid(day))
```

Running the test hopefully we will see that it has passed. If it doesn't check your code against the final code at the bottom of this page, to see where you might have gone wrong.

### find_next_alarm()

Now that we have the time of the alarm and the days the alarm will be active, we can calculate when the alarm will next trigger. The alarm class seems like a sensible place to put this functionality.

So lets write the simplest test and that is to make sure that the time returned for the alarm is actually correct. This should be relatively straight forward to implement because it mostly just requires returning the stored alarm time value. The test for this is:
```python
def test_returns_correct_next_alarm_time(self):
    test_alarm = alarm.alarm.Alarm(6, 30, ["Monday"])
    self.assertEqual(test_alarm.find_next_alarm().time(), datetime.time(6, 30))
```

So here we are expecting the output of ``find_next_alarm()`` to be a datetime object as later it will also contain the date of the next alarm. We are then extracting the time from that and comparing it to an expected time of 6.30am. Now it turns out implementing this is not quite as straight forward as I though because you cannot simply populate the time part of a datetime object. The date also needs to be populated. To temporarily overcome this, I have just populated the date with the now() function which should suit our needs for this test. The result looks like this:
```python
def find_next_alarm(self):
    return datetime.datetime.now().replace(
        hour=self._time.hour, minute=self._time.minute, second=0, microsecond=0
    )
```

You will notice that we include the second and the microsecond, in the replace function setting both to zero. This unfortunately is a side affect of the test. We could mock the datetime object (as we will shortly) but for this test it didn't really seem to do much harm in being very accurate.

Next we want to make sure that the correct day is returned by the function. Again, this is quite a simple test to write but the solution is likely going to be a lot more complicated:
```python
def test_returns_correct_next_alarm_day(self):
    test_alarm = alarm.alarm.Alarm(6, 30, ["Monday"])
    self.assertEqual(test_alarm.find_next_alarm().weekday(), 0)
```

The simplest solution to that would be to hard-code a date that we know is a Monday. But predictably, that will fail the second we start request different days. The simplest way I could think of to solve this was to start with todays date, and then repeatedly add a day until we get a monday and return that date. This would work well with the actual goal as it should return the genuine next alarm date, not just the correct day. I have split this out into a separate function:
```python
def _find_next_alarm_date(self):
    alarm_date = datetime.datetime.now()
    for _ in range(7):
        if alarm_date.weekday() == 0:
            return alarm_date
        alarm_date = alarm_date + datetime.timedelta(days=1)
```

As you can see this is still hard-coding the day (in the if statement) but we will solve that part shortly. This here is an example of why we sometimes hard-code because it allows us to test the surrounding functionality and when we know that is working, we can then make the solution more dynamic.

Now we need to call this function in our ``find_next_alarm`` function:
```python
alarm_time = self._find_days_till_next_alarm()
return alarm_time.replace(
    hour=self._time.hour, minute=self._time.minute, second=0, microsecond=0
)
```

Low and behold, we have passed our test but as mentioned earlier this will again fail when we change the days. So lets get back to that if statement. Here we want to check that the alarm_date falls on a day that is in ``self._days``. This simplest way I thought to do this is to convert alarm_date to its string equivalent and check if that string is in ``self._days``. This is why we earlier set up the ``Weekdays`` array to follow the datetime indexing. We can now change the if statement to the following:
```python
if self.Weekdays[alarm_date.weekday()] in self._days:
```

Viola. This will now work no matter what day is provided and as an added bonus, it will also work for multiple days supplied choosing the earliest day. One word of caution: this test will pass straight away, if you are testing on a Monday. It is probably worth mocking the datetime object like we are about to do for our next test.

Now this functionality appears as if it is working properly. However, did you consider what would happen if we set an alarm for Monday-6.30am on a Monday after this time. It would claim the next alarm was in the past. We can't have that can we. However, we now have a complexity for writing a test. When the next alarm triggers depends on what the current date and time is, but that is always changing, so how do we define what we expect to be the output. We could write some complicated function that determines what the next alarm time should be based on the current time, but then we will basically be reimplementing the functionality that we are trying to test. Luckily we have another tool in our toolbelt, just for this problem: Mocks.

Mocks are a very powerful testing tool that allows you to replace any object in your code with an object that can be explicitly defined. This mocked object will happily accept any function calls (even though they are not defined) and will return any values that we tell it to return. Mocks are very powerful for objects that return non-deterministic values as we can then define the mock to return a single known value for testing purposes.

In this case, we will mock the datetime class so that any calls to ``datetime.now()`` return the same date. This can be done using the following code:
```python
with mock.patch.object(datetime, "datetime", mock.Mock(wraps=datetime.datetime)) as patched:
    patched.now.return_value = datetime.datetime(2019, 7, 23, 8, 0)
```

This was a pain in the butt to figure out as you are not really allowed to alter the attribute of a built-in class. So we have to wrap the ``datetime.datetime`` class and then assign the attribute of the wrapping mock. If there is a better way of doing this, please let me know.

Now that we have have replaced the current datetime, with a fixed one, we can write a fairly simple test that asserts that the next alarm time is equal to some fixed datetime. In the case below, that is the Monday following the mocked datetime at 6.30am:
```python
test_alarm = alarm.alarm.Alarm(6, 30, ["Tuesday"])
self.assertEqual(
    test_alarm.find_next_alarm(), datetime.datetime(2019, 7, 30, 6, 30)
)
```

For the alarm code, we need to make two alterations. One is to the range of the for loop. Currently we only loop over 7 days, but this will never reach the following Tuesday and so will return None. So this needs to be changed to ``range(8)``. The second change is the addition of an if statement for when we return ``alarm_date``. We want it to always return if ``alarm_date`` is not today and if it is today, only return if ``alarm_dates`` time (which is actually the time now) is before the alarm time. This can be put quite concisely into a single if statement as follows:
```python
if (
    alarm_date.day != datetime.datetime.now().day 
    or alarm_date.time() < self._time
):
    return alarm_date
```

There is one more bit of functionality I would like to implement, which is an edge-case and that is where alarm does not contain any days. As we said earlier, this will return None and cause the program to crash because None does not have attribute: replace. I would prefer to crash the program on my own terms and give a bit more indicative error message. The test for this is quite simple:
```python
def test_raises_if_no_days_in_alarm(self):
    test_alarm = alarm.alarm.Alarm(6, 30)
    self.assertRaisesRegex(
        ValueError,
        "Alarm does not have any valid days enabled",
        test_alarm.find_next_alarm,
    )
```

To then get this test to pass, we simply add the following line to the end of the ``_find_next_alarm_date()`` function:
```python
raise ValueError("Alarm does not have any valid days enabled")
```

### Finishing touches

That are now just a few last things that we need to implement. These include the validation of the playback metadata (data required to play the alarm sound) and then getters for both the playback metadata and if the alarm is active.

The first part is complicated to do at the moment because we have not yet written the player so we do not know what data should be expected. Furthermore, this functionality should not really be implemented here but simply called. But to make sure we don't forget about it, I am going to make a test that immediately fails so that it appears in all future tests. The test is just as follows:
```python
def test_verifies_playback_object_is_valid(self):
    self.fail("Need to implement this!")
```

Now every time you run your tests, you will be reminded that you need to go back and implement this. I don't know if this is bad practice but I think it is fine at this scale. I would also advise not doing this too much as it will end up flooding the information you actually want from the test.

Finally we need to implement the playback and active inputs into the constructor and create getters to retrieve them. I am reasonably sure that it is standard practice to not test getters and setters so we will not write any tests for them, just simply insert the following code into the constructor:
```python
def __init__(self, hour=0, minute=0, days=[], playback=None, active=True):
    ...
    self._playback = playback
    self._active = bool(active)
```

It is here that we would validate the contents of playback (and maybe populate it with default values if it is empty). You will also notice that we have cast active into a bool. This is just to guarantee that we return a boolean with the getter. The following code also defines the getters:
```python
def get_playback(self):
    return self._playback

def is_active(self):
    return self._active  
```

There we go! We have (almost) finished the alarm class so now we can start to implement the higher level classes such as the manager and the scheduler.

Below is a dump of the final class, which can also be found [here](https://github.com/rmasp98/PieAlarm/blob/master/alarm/alarm.py)

```python
import datetime


class Alarm:
    """Alarm container

    Stores all the information required for an alarm including time, days,
    playback metadata and if the alarm is active
    """

    Weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    def __init__(self, hour=0, minute=0, days=None, playback=None, active=True):
        """Create alarm providing an integer for hour and minute, a list of days from 
        Alarm.Weekdays, playback to provide to player, and boolean for if the alarm is active"""
        self._time = datetime.time(hour, minute)
        self._playback = playback
        self._active = bool(active)
        self._days = set()
        if days is not None:
            for day in days:
                self._days.add(self._check_day_is_valid(day))

    def get_time(self):
        """Returns the time for the alarm as datetime object"""
        return self._time

    def is_day_active(self, day):
        """Returns bool for if the given day is active. Day must be of the
        form displayed in the alarm.Weekdays list"""
        return day in self._days

    def get_playback(self):
        """Returns playback metadata as a dictionary. Details about valid
        keys and values can be found in the sound package"""
        return self._playback

    def is_active(self):
        """Returns bool if alarm should be scheduled"""
        return self._active

    def find_next_alarm(self):
        """Returns datetime object for when alarm should next be triggered"""
        alarm_time = self._find_days_till_next_alarm()
        return alarm_time.replace(
            hour=self._time.hour, minute=self._time.minute, second=0, microsecond=0
        )

    def _check_day_is_valid(self, day):
        if day in self.Weekdays:
            return day
        raise ValueError(str(day) + " is not an accepted day")

    def _find_days_till_next_alarm(self):
        alarm_date = datetime.datetime.now()
        for _ in range(8):
            if self.Weekdays[alarm_date.weekday()] in self._days:
                if (
                    alarm_date.day != datetime.datetime.now().day
                    or alarm_date.time() < self._time
                ):
                    return alarm_date
            alarm_date = alarm_date + datetime.timedelta(days=1)
        raise ValueError("Alarm does not have any valid days enabled")
```