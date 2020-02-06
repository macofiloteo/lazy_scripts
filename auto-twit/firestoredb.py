from __future__ import absolute_import
from apscheduler.jobstores.base import BaseJobStore, JobLookupError, ConflictingIdError
from apscheduler.util import maybe_ref, datetime_to_utc_timestamp, utc_timestamp_to_datetime
from apscheduler.job import Job

try:
    import cPickle as pickle
except ImportError:  # pragma: nocover
    import pickle




class FirestoreDBJobstore(BaseJobStore):
    """
    Stores jobs in a MongoDB database. Any leftover keyword arguments are directly passed to
    pymongo's `MongoClient
    <http://api.mongodb.org/python/current/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient>`_.

    Plugin alias: ``mongodb``

    :param str database: database to store jobs in
    :param str collection: collection to store jobs in
    :param client: a :class:`~pymongo.mongo_client.MongoClient` instance to use instead of
        providing connection arguments
    :param int pickle_protocol: pickle protocol level to use (for serialization), defaults to the
        highest available
    """

    def __init__(self, collection='jobs', client=None,
                 pickle_protocol=pickle.HIGHEST_PROTOCOL, **connect_args):
        super(FirestoreDBJobstore, self).__init__()
        self.pickle_protocol = pickle_protocol

        if not collection:
            raise ValueError('The "collection" parameter must not be empty')
        if not client:
            raise ValueError('The "client" parameter must not be empty')
        self.client = maybe_ref(client)
        self.collection = self.client.collection(collection)

    def start(self, scheduler, alias):
        super(FirestoreDBJobstore, self).start(scheduler, alias)
        #self.collection.ensure_index('next_run_time', sparse=True) not needed as firestore autmatically creates indeces

    #@property
    # def connection(self):
    #     warnings.warn('The "connection" member is deprecated -- use "client" instead',
    #                   DeprecationWarning)
    #     return self.client

    def lookup_job(self, job_id):
        # document = self.collection.find_one(job_id, ['job_state'])
        document = self.collection.document(job.id).get().to_dict()
        return self._reconstitute_job(document['job_state']) if document else None

    def get_due_jobs(self, now):
        timestamp = datetime_to_utc_timestamp(now)
        documents = []
        snapshots = self.collection.where(u'next_run_time', u'<=', timestamp).get()
        for snap in snapshots:
            documents.append(snap.to_dict())
        return self._reconstituteAndAppendJobs(documents)
        # return self._get_jobs({'next_run_time': {'$lte': timestamp}})

    def get_next_run_time(self):
        print("get_next_run_time not yet available")
        document = self.collection.where(u'next_run_time', u'>', 0).order_by(u'next_run_time').limit(1).get()
        document = list(document)
        try:
            document = document[0].to_dict()
        except IndexError:
            document = None
        #  document = self.collection.find_one({'next_run_time': {'$ne': None}},
        #                                      projection=['next_run_time'],
        #                                      sort=[('next_run_time', ASCENDING)])
        return utc_timestamp_to_datetime(document['next_run_time']) if document else None

    def get_all_jobs(self):
        # jobs = self._get_jobs({})
        documents = []
        snapshots = self.collection.get()
        for snap in snapshots:
            documents.append(snap.to_dict())
        jobs = self._reconstituteAndAppendJobs(documents)
        self._fix_paused_jobs_sorting(jobs)
        return jobs

    def add_job(self, job):
        try:
            self.collection.document(job.id).set({
                    '_id': job.id,
                    'next_run_time': datetime_to_utc_timestamp(job.next_run_time),
                    'job_state': pickle.dumps(job.__getstate__(), self.pickle_protocol)
            })
        except:
            print("error")
        # except DuplicateKeyError:
        #     raise ConflictingIdError(job.id)

    def update_job(self, job):
        changes = {
            'next_run_time': datetime_to_utc_timestamp(job.next_run_time),
            'job_state': pickle.dumps(job.__getstate__(), self.pickle_protocol)
        }
        result = self.collection.document(job.id).update(changes)
        print(result)
        # if result and result['n'] == 0:
        #     raise JobLookupError(job.id)

    def remove_job(self, job_id):
        result = self.collection.document(job_id).delete()
        # if result and result['n'] == 0:
        #     raise JobLookupError(job_id)
        print(result)

    def remove_all_jobs(self):
        print("remove_all_jobs not yet available")
        # self.collection.remove()

    def shutdown(self):
        print("Firestore does not require to 'close' connection")
        # self.client.close()

    def _reconstitute_job(self, job_state):
        job_state = pickle.loads(job_state)
        job = Job.__new__(Job)
        job.__setstate__(job_state)
        job._scheduler = self._scheduler
        job._jobstore_alias = self._alias
        return job

    def _reconstituteAndAppendJobs(self, documents):
        jobs = []
        failed_job_ids = []

        #sort DOCUMENTS TO ASCENDING DONT FORGET
        for document in documents:
            try:
                jobs.append(self._reconstitute_job(document['job_state']))
            except BaseException:
                self._logger.exception('Unable to restore job "%s" -- removing it',
                                       document['_id'])
                failed_job_ids.append(document['_id'])

        # Remove all the jobs we failed to restore DONT FORGET THIS
        if failed_job_ids:
            for jobId in failed_job_ids:
                self.remove_job(jobId)

        return jobs

    def __repr__(self):
        return '<%s (client=%s)>' % (self.__class__.__name__, self.client)
