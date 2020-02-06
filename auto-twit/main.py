import time
import signal
import random
import datetime
from twitter import TwitterError
from config import twitterApi, db
from job import RandomTimeJob, EveryOClockJob, EveryTimeOfTheDayJob


def signal_handler(signum, frame):
    raise ProgramKilled


def tweetFromFirestore():
    documentId = None
    document = None
    try:
        results = db.collection(u'toTweets').where(
            u'isDone', u'==', False).limit(1).get()
        snap = list(results)[0]
        documentId = snap.id
        document = snap.to_dict()
        print(document)
    except IndexError as err:
        print("No tweets to be tweeted!")
        return
    except:
        print("Something went wrong. Try Again")
        return

    try:
        resTwitter = twitterApi.PostUpdate(document[u'message'])
        db.collection(u'toTweets').document(
            documentId).update({u'isDone': True})
    except TwitterError as err:
        print(err.message)


def tweetCurrentTime():
    try:
        resTwitter = twitterApi.PostUpdate(
            f'It is currently {datetime.datetime.now()}')
    except TwitterError as err:
        print(err.message)


def tweetSomething(message):
    try:
        resTwitter = twitterApi.PostUpdate(message)
    except TwitterError as err:
        print(err.message)


class ProgramKilled(Exception):
    pass


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    everyTimeOfTheDayTweetJob = EveryTimeOfTheDayJob(
        execute=tweetFromFirestore, hour=23, minute=23, second=0)
    everyTimeOfTheDayTweetJob.start()

    while True:
        try:
            time.sleep(1)
        except ProgramKilled:
            print("Program killed: running cleanup code")
            everyTimeOfTheDayTweetJob.stop()
            break
