"""
"""
from common.records import SeverityRecord
from tools import RFClassifier
from common import REDIS_POOL
import cPickle as pickle
import redis


class Analyser(object):
    """
    Using various factors identified can calculated by the modeller,
    this will analyse and compute a severity value to reflect the
    possibility of a requester been an attacker.
    The severity factor should be represented by a numerical value.
    """

    def __init__(self):
        self.redis = redis.Redis(connection_pool=REDIS_POOL)
        self._rf_clf = RFClassifier()
        pass

    def analyse(self, session, record_key):
        serialized_record = self.redis.get(record_key)
        record = pickle.loads(serialized_record)
        prob, cls = self._rf_clf.analyse(record)
        # analyse it using rf_classifier
        # update severity with returned values
        self.update_severity(session, prob, cls == 1)
        self.remove_redis_record(record_key)
        pass

    def update_severity(self, session, value, is_ddos):
        severity = SeverityRecord(session, value, is_ddos)
        severity.save()
        severity = None
        pass

    def remove_redis_record(self, record_key):
        self.redis.delete(record_key)
        pass
    pass