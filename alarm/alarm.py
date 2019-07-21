from datetime import time, datetime

Weekdays = {
    "Monday"    :0,
    "Tuesday"   :1,
    "Wednesday" :2,
    "Thursday"  :3,
    "Friday"    :4,
    "Saturday"  :5,
    "Sunday"    :6
}

class Alarm:
    def __init__(self):
        self.time = time(0, 0)
        self.days = set()
        self.trigger = "What will happen at alarm"

    def set_time(self, hour, minute):
        self.time = time(hour, minute)

    def add_day(self, day):
        self.days.add(Weekdays[day])

    def remove_day(self, day):
        self.days.discard(Weekdays[day])

    # def find_next_day(self):
    #     today = datetime.now().weekday()
    #     for i in range(8):
    #         if (today + i) % 7 in self.days:
    #             if (i == 0) and (datetime.now().time() < self.time):
    #                 return 0
    #             elif i != 0:
    #                 return i
    #     return -1
