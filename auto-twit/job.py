import threading
import random
import datetime

# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679


class Job(threading.Thread):
    def __init__(self, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        print(f'Job executed at {datetime.datetime.now()}')
        self.execute(*self.args, **self.kwargs)


# randomTweetTimejob = RandomTimeJob(execute=*function*, randArray=[10,30], argsOfFunction=params)
# randArray is in seconds
class RandomTimeJob(Job):
    def __init__(self, execute, randArray, *args, **kwargs):
        super(RandomTimeJob, self).__init__(execute, *args, **kwargs)
        self.randArray = randArray

    def run(self):
        while not self.stopped.wait(random.randint(self.randArray[0], self.randArray[1])):
            self.execute(*self.args, **self.kwargs)


class EveryOClockJob(Job):
    def run(self):
        print(f'EveryOClockJob starting at {datetime.datetime.now()}')
        currentHour = datetime.datetime.now().hour
        nextHour = None
        if currentHour == 23:
            currentDay = datetime.datetime.now().day
            nextHour = datetime.datetime.now().replace(
                day=currentDay+1, hour=0, minute=0, second=0, microsecond=0)
        else:
            nextHour = datetime.datetime.now().replace(
                hour=currentHour+1, minute=0, second=0, microsecond=0)
        waitTime = (nextHour - datetime.datetime.now()).total_seconds()
        while not self.stopped.wait(waitTime):
            print(f'Job executed at {datetime.datetime.now()}')
            self.execute(*self.args, **self.kwargs)
            waitTime = 3600


class EveryTimeOfTheDayJob(Job):
    def __init__(self, execute, hour, minute=0, second=0, *args, **kwargs):
        super(EveryTimeOfTheDayJob, self).__init__(execute, *args, **kwargs)
        self.hour = hour
        self.minute = minute
        self.second = second

    def run(self):
        currentDate = datetime.datetime.now()
        targetDate = datetime.datetime.now().replace(
            hour=self.hour, minute=self.minute, second=self.second, microsecond=0)
        waitTime = (targetDate - currentDate).total_seconds()
        if waitTime < 0:
            waitTime = 86400 + waitTime
        while not self.stopped.wait(waitTime):
            print(f'Job executed at {datetime.datetime.now()}')
            self.execute(*self.args, **self.kwargs)
            waitTime = 86400
