# Scheduling alarms

Next we want to create an ability for the alarms to trigger at the correct time. A good approach to that is to use a scheduler. Schedulers are responsible for executing work at a given time. In our case, this means informing us when the alarm time is so that we can trigger our alarm. I have decided to break this down into three classes:
* Job class: responsible emitting a signal when the alarm time has been reached
* Scheduler class: responsible for creating, deleting and managing each of the jobs
* Signal class: this will allow Jobs to inform Scheduler and anyone else interested that the alarm has triggered

## Job Class

The job class will introduce a number of new concepts both in the tests and in the class itself, which includes threading, observers and mocks. 

Threading is the concept of running multiple bits of code simultaneously. This is required as we will have many jobs all counting down the time until they should execute as well as the main UI thread that keeps the user interface responding while this is happening. This uses the threading library and is overall very simple to create but also very simple to introduce bugs. To find out more information about threading, look [here](). We only need a really simple use of the threading library that works as follows:
```python
thread = threading.Thread(target=<function-to-run>)
thread.start()
```

This code will run \<function-to-run> and when the function completes, the thread will be killed.

Observers (or signals) allows an object to inform multiple other objects about an update. In the case of our alarm, it would allow the job objects to let everyone know that an alarm has just triggered. At the very least we want scheduler to know about the completion of the job so that it can clean it up; and the alarm manager so that it can trigger each aspect of an alarm (e.g. sound). All each of these objects have to do is subscribe to the signal with a function they want to be run when the job emits.
