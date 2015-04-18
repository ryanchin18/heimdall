"""

"""
from common import REDIS_POOL, config, redis_key_template
import cPickle as pickle
import redis


class SeverityRecord(dict):
    def __init__(self, session, probability=None, is_ddos=None, is_ban=None):
        self.key = redis_key_template.format(session, "severity", None)
        self.redis = redis.Redis(connection_pool=REDIS_POOL)
        record = self.redis.get(self.key)
        if record:
            severity = pickle.loads(record)
        else:
            severity = {
                "session": session,
                "probability": 0.,
                "is_ddos": False,
                "is_ban": False
            }
        severity["probability"] = probability if probability is not None else severity["probability"]
        severity["is_ddos"] = is_ddos if is_ddos is not None else severity["is_ddos"]
        severity["is_ban"] = is_ban if is_ban is not None else severity["is_ban"]
        super(SeverityRecord, self).__init__(**severity)
        pass

    def save(self):
        serialized = pickle.dumps(dict(self))
        self.redis.set(self.key, serialized)
        if not self['is_ban']:
            # if the record is not ban, remove session record after X minuets
            self.redis.expire(self.key, config.get('session_length', 1 * 60 * 5))
        pass

    def ban(self):
        self['is_ban'] = True
        self.save()
        pass

    def unban(self):
        self['is_ban'] = False
        self.save()
        pass

    def is_ban(self):
        return self['is_ban']
        pass

    def remove_redis_record(self):
        self.redis.delete(self.key)
        pass
    pass

if __name__ == '__main__':
    s = SeverityRecord("xxx.xxx.xxx.xxx")
    s.remove_redis_record()
    pass