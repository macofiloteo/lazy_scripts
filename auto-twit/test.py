# from pytz import utc
# from apscheduler.schedulers.blocking import BlockingScheduler
# from firestoredb import FirestoreDBJobstore
# from config import db, twitterApi


# def tweetAtARandomRate():
#     results = db.collection(u'toTweets').where(u'isDone', u'==', False).limit(1).get()
#     doc = list(results).to_dict()
#     try:
#         resTwitter = twitterApi.PostUpdate(f'It is currently {datetime.datetime.now()}')
#     except TwitterError as err:
#         print(err.message)

# jobstores = {
#   'default': FirestoreDBJobstore(collection='jobs', client=db)
# }
# sched = BlockingScheduler(jobstores=jobstores)
# sched.add_job(tweetAtARandomRate)
# sched.start()


def printString(thisTest):
  print(thisTest)
  print("Ended!")

class ArgTesto(object):
  def __init__(self, willnotBeUsed, function, time=0, *args, **kwargs):
    self.willnotBeUsed = willnotBeUsed
    self.args = args
    self.kwargs = kwargs
    self.function = function

  def run(self):
    self.function(*self.args, **self.kwargs)


argTest = ArgTesto("gay", printString, thisTest="hey")
argTest.run()