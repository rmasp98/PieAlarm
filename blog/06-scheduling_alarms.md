# Scheduling alarms

Now that we have created the Job class, we can write a class to utilise those jobs: the Scheduler. In terms of functionality, we want the scheduler to be able to create and delete jobs, and find the next job time. We will also need a function to remove all jobs so that we can kill off all the threads before the application shuts down. 


### Get next job time

So the first and hopefully smallest bit of functionality we can introduce for the scheduler is finding the next job time. Even easier is finding the next alarm time when there are no alarms. I have decided to return ``None`` if there are no alarms:
```python
def test_returns_none_for_time_when_no_job(self):
    scheduler = alarm.scheduler.Scheduler()
    self.assertIsNone(scheduler.get_next_job_time())
```

Which actually only requires us to define the ``get_next_job_time`` function as functions in python return None by default. This test will however, allow us to ensure this functionality remains when we evolve the function. 

One thing we are going to do before we move on is tidy up this test and all future tests, by declaring some of the variables and objects in a class constructor for use in each test. This hides away unnecessary parts of the test that do not help to understand what is happening. For example, every test needs to construct a scheduler, but the construction is straightforward and has nothing to do with the test itself.

To do this, I have used the constructor of the test case class, to initialise these parts and keep them out of the test. We haven't done this up to this point because there has not been a large amount in common between cases but if you want to simplify the tests for example by extracting out some of the hard coded parts, then definitely go ahead. The ``SchedulerTest`` constructor needs to run the constructor of the super class (``TestCase``):
```python
 def __init__(self, *args, **kwargs):
    super(SchedulerTest, self).__init__(*args, **kwargs)
    self.scheduler = alarm.scheduler.Scheduler()
```

This means we can remove the construction of the scheduler in the above case but we also need to prefix the call to the scheduler with a ``self``.

Next we want to add a job to the scheduler and see if we can return the time of that job. From here on out we are going to need to mock the Job class because we don't want it to start spawning threads and waiting. You can see this in the below test:
```python
@mock.patch("alarm.job.Job", mock.Mock())
def test_returns_time_for_submitted_job(self):
    self.scheduler.add_job(self.time)
    self.assertEqual(self.scheduler.get_next_job_time(), self.time)
```

Here we have defined a time in the constructor as the actual time we provide is not important, it is just important that the input is the same as the output. The rest of the test I hope is self explanatory.

To start off with in getting this test running, we need to define an empty ``add_job`` function that takes a single parameter. As we are going to need to return the time supplied, we are also going to need to store the provided time as a member variable in the ``add_job`` function and then finally we need to return this new variable in ``get_next_job_time``. One little trick we can do to keep our previous test passing is to initialise the member variable in the constructor as ``None``.
```python
def __init__(self):
    self._time = None

def add_job(self, time):
    self._time = time

def get_next_job_time(self):
    return self._time 
```

So what will happen if we add two jobs where the first job will trigger before the second. In our current flow, the second job will overwrite ``self._time`` and would return the second job time as being the next job time, which is incorrect. So we need to write a test that will drive this desired functionality into the code:
```python
@mock.patch("alarm.job.Job", mock.Mock())
def test_returns_nearest_job_time_for_two_submitted_jobs(self):
    first_time = self.time - datetime.timedelta(days=1)
    self.scheduler.add_job(first_time)
    self.scheduler.add_job(self.time)
    self.assertEqual(self.scheduler.get_next_job_time(), first_time)
```

To fix this, we need to simply add an if statement that checks to see if the current value of ``self._time`` is greater than the new time. We will also need to check to see if ``self._time`` is None as the above equality will cause the application to crash if it is:
```python
if self._time is None or self._time > time:
    self._time = time
```

Next I want to make sure that the ``self._time`` is not updated if the time is in the past. This type of job should trigger instantly so there should be no need to update the time. This test is fairly straightforward:
```python
@mock.patch("alarm.job.Job", mock.Mock())
def test_does_not_update_time_if_job_in_past(self):
    self.scheduler.add_job(datetime.datetime(1989, 12, 24))
    self.assertIsNone(self.scheduler.get_next_job_time())
```

This again is quite a simple fix and that is to add another component to the if statement that checks if time is in the future:
```python
if time > datetime.datetime.now() and (self._time is None or self._time > time):
    self._time = time
```

### Returning job UID

Now that we have started to get time functionality up and running, we need to start focusing on other parts of the scheduler. One thing we need to implement is the tracking of jobs. For this we will assign a UID to each job which will be returned to the class creating the job. To create a genuinely unique identifier, we are going to use a built in python class especially dedicated for this task: ``uuid``. So first let's write the test:
```python
@mock.patch("alarm.job.Job", mock.Mock())
def test_adding_jobs_returns_uid_for_job(self):
    uid = self.scheduler.add_job(self.time)
    self.assertRegex(uid, "^[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}$")
```

Here we are introducing a new type of test and that is a regular expression test. Here you provide a [regex](https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285) string that should match with all wanted outputs of a function. In this case we want a 32 character UUID generated by the ``uuid`` library. All the above regex is saying is that we expect to see ``"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"`` where ``X`` can be any letter (upper or lower case) or a number.

To get this running, all we need to do is return the output of the call to the ``uuid`` library in the add_job function:
```python
return str(uuid.uuid4())
```

### Creating a Job

So now onto the main purpose of this class: creating Jobs. As we know that a job can handle itself, all we need to do is create an instance of the Job in order to get it all running. So let's drive that functionality into the class:
```python
@mock.patch("alarm.job.Job")
def test_adding_job_runs_the_job(self, job_mock):
    uid = self.scheduler.add_job(self.time)
    job_mock.assert_called_with(uid, self.time)
```

And again really simple to implement. All we have to do is call the constructor of the Job class providing the time given to ``add_job`` and the uid we just generated:
```python
uid = str(uuid.uuid4())
alarm.job.Job(uid, time)
return uid
```

### Removing a Job

So great we now have the main basis of the class done and that is to create jobs. However, it is really important that we can remove the jobs when they are no longer needed. Consider creating an alarm and then realising you don't actually want it anymore. It would be a bit of useless alarm clock if that alarm still went off after you removed it.

So lets implement the remove alarm functionality. All we want to see at the moment is that when we remove an job, the ``Job.kill`` function is called:
```python
@mock.patch("alarm.job.Job")
def test_removing_job_kills_the_job(self, job_mock):
    uid = self.scheduler.add_job(self.time)
    self.scheduler.remove_job(uid)
    job_mock.return_value.kill.assert_called_once()
```

You will notice that the last line is a little weird. That is because we are mocking the constructor of the Job class and the constructor does not have the ``kill`` method. It is the object returned from the constructor that has a ``kill`` method.

We are going to have to add a couple things in here. Firstly we need to store the created alarm, so we will need to create a member variable and then store the created alarm from ``add_job`` in that variable. We can then run the kill method on the stored job inside the new ``remove_job`` function. Obviously this is not really going to work because what happens when we add multiple alarms. 


### Update time

The next step we need to tackle is updating the next job time when we remove a job. As always lets start with the test (there is nothing special in this test):
```python
@mock.patch("alarm.job.Job", mock.Mock())
def test_removing_job_updates_job_time(self):
    uid = self.scheduler.add_job(self.time)
    later_alarm = self.time + datetime.timedelta(days=1)
    self.scheduler.add_job(later_alarm)
    self.scheduler.remove_job(uid)
    self.assertEqual(self.scheduler.get_next_job_time(), later_alarm)
```

Clearly, we need to store all alarms that are generated and associate them with the uid in order to be able to recalculate the next job time. The most obvious way of doing this is to store them in a [dictionary](https://www.w3schools.com/python/python_dictionaries.asp). A dictionary is simply a way of mapping one object to another, in this case it is mapping the uid string to the job object. For this we need to add code in the constructor, ``add_job`` function and ``remove_job`` function as below:
```python
 def __init__(self):
    ...
    self._jobs = {}
    ...

def add_job(self, time):
    ...
    self._jobs[uid] = alarm.job.Job(uid, time)
    ...

def remove_job(self, uid):
    self._jobs[uid].kill()
```

Note that remove_job will throw an exception if uid does not exist in ``self._jobs``. But this code gets our test passing and that is all that is important for the time being.

However, this still does not solve our problem. We still need to calculate the next job time. The easiest way to solve this is to simply loop over all the jobs in ``self._jobs`` and figure out which is the soonest. But in order for this to work, we also need to make sure that we remove the job from the dictionary first. This can be done using the dictionaries ``pop`` function:
```python
self._jobs.pop(uid).kill()
```

Now we are going to introduce a new function, that performs the looping over the dictionary and calculating the next alarm time:
```python
def _update_next_job_time(self):
    next_time = None
    for update_job in self._jobs.values():
        if update_job.get_time() > datetime.datetime.now() and (
            next_time is None or update_job.get_time() < next_time
        ):
            next_time = update_job.get_time()

    self._next_job_time = next_time
```

This simply performs the same if statement we used earlier but inside of a loop over all alarms. It makes sense therefore to also call this function when we add a job as well, just to keep everything clean and simple.

Unfortunately this will break a few of our tests because we have mocked the Job class them and in our update function, we have called the get_time() from the job class, which the mock will not know how to treat. This will then return another mock. However, we then do a comparison to the returned value to a datetime object and clearly python does not know how to do this comparison. Fortunately, there is quite an easy fix for this. Simply add the following line of code to any classes that mock the Job class, before ``add_job`` is called:
```python
job_mock.return_value.get_time.return_value = self.time
```

### No exception on failed remove

As we mentioned earlier, if we try to remove a job that does not exist in the dictionary, it will throw an exception. I don't think it is necessary to crash the application when this occurs but simultaneously there is not very much we can do if the uid we have does not exist. It is probably worth logging it but not really throwing an exception. So we are going to write a test to make sure this does not occur:
```python
def test_removing_non_existing_job_fails_silently(self):
    try:
        self.scheduler.remove_job("Hello")
    except KeyError:
        self.fail("Should not have raised an exception")
```

To prevent the key access failure, we can add an additional parameter to the pop function. This additional parameter tells pop what to do in the case of no key, in this case nothing. You will however notice that this will still throw an exception because the ``None`` type does not have the attribute kill. Therefore, we need to dump the output of pop to a variable and then check to see if it is not None:
```python
def remove_job(self, uid):
    removed_job = self._jobs.pop(uid, None)
    if removed_job is not None:
        removed_job.kill()
        self._update_next_job_time()
```

### Subscribing to Job

As you will remember earlier, we created a notification mechanism in the Job class. Well here is one of the places where we need to use it. This is because when the job has completed, we want the scheduler to be informed so that it can remove the job from the dictionary. To check this works, we are going to write a fairly simple test, this time not mocking Job so that the notification triggers and the job is removed from the dictionary:
```python
@mock.patch("alarm.scheduler.Scheduler.remove_job")
def test_job_removed_when_complete(self, remove_mock):
    self.scheduler.add_job(datetime.datetime.now())
    remove_mock.assert_called()
```

You may notice that I chose to use ``assert_called`` rather than ``assert_called_once``. This is due to a slightly annoying aspect of the testing framework where all tests are run in the same process, so every time the scheduler is created, which it is done for every test, another subscription is made to the Job class. This means that when we get round to checking if the subscription successfully notifies, we get calls equal to the number of tests that have run. Fortunately for us, the fact that this is called once is sufficient to know that the test has passed.

For this test, we need just two bits of code. The first is the subscription to the Job class in the constructor and the second is the function that we are going to pass to the Job observer:
```python
def __init__(self):
    ...
    alarm.job.Job.subscribe(self._job_complete)

def _job_complete(self, uid, _):
    self.remove_job(uid)
```

Something that may be new in the ``_job_complete`` function is the underscore as the second parameter. This means that we expect two parameters to be passed to the function but we don't care about the second. The second parameter is simply whether the job is successful or not but we will want to remove the job either way so we ignore it.


### Reset scheduler

We pretty much have all the functionality we need from the scheduler but there is one minor thing that we will eventually need to help the application close down cleanly, and that is a way to just kill all jobs, which will in turn kill all additional job threads. If we do not do this, the application will continue running after the window has closed and you will have to actively kill the process.
```python
@mock.patch("alarm.job.Job")
def test_resetting_scheduler_kills_all_jobs(self, job_mock):
    job_mock.return_value.get_time.return_value = self.time
    for i in range(3):
        self.scheduler.add_job(self.time)
    self.scheduler.reset()
    self.assertEqual(job_mock.return_value.kill.call_count, 3)
```

You would think we simply need to loop over ``self._jobs`` and pass the each to remove job. However, as we remove jobs, ``self._jobs`` changes and python does not like you looping over a changing dictionary (and rightly so). So what we need to do is pull out all the uids and add them to a list. Then loop over the list calling ``remove_job``.
```python
def reset(self):
    jobs = list(self._jobs.keys())
    for remove_job in jobs:
        self.remove_job(remove_job)
```

### Final class

There you have it. We have completed all the required functionality of the scheduler class. At least for now. Here is the what my version of the class looks like:
```python
import datetime
import uuid

import alarm.job


class Scheduler:
    """Basic scheduler

    Accepts a time to schedule a job, which is added to a list and
    started immediately. Each job is assigned a uid which is returned
    to calling function. Job is then removed upon completion
    """

    def __init__(self):
        self._time = None
        self._jobs = {}
        alarm.job.Job.subscribe(self._job_complete)

    def get_next_job_time(self):
        """Returns time (as datetime) of soonest job to execute"""
        return self._time

    def add_job(self, time):
        """Accepts a datetime object for when job will execute.
        Jobs in past will execute immediately"""
        uid = str(uuid.uuid4())
        self._jobs[uid] = alarm.job.Job(uid, time)
        self._update_next_job_time()
        return uid

    def remove_job(self, uid):
        """If job exists in list, it will be killed and removed from list"""
        removed_job = self._jobs.pop(uid, None)
        if removed_job is not None:
            removed_job.kill()
            self._update_next_job_time()

    def reset(self):
        """This will ensure that all job threads are killed of at the end"""
        jobs = list(self._jobs.keys())
        for remove_job in jobs:
            self.remove_job(remove_job)

    def _update_next_job_time(self):
        next_time = None
        for update_job in self._jobs.values():
            if update_job.get_time() > datetime.datetime.now() and (
                next_time is None or update_job.get_time() < next_time
            ):
                next_time = update_job.get_time()

        self._time = next_time

    def _job_complete(self, uid, _):
        self.remove_job(uid)
```