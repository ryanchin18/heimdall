"""

"""
from common import REDIS_POOL, config, redis_key_template
import cPickle as pickle
import redis


class SeverityRecord(dict):
    def __init__(self, session, value, is_ddos):
        self.key = redis_key_template.format(session, "severity", None)
        self.redis = redis.Redis(connection_pool=REDIS_POOL)
        severity = {
            "session": session,
            "value": value,
            "is_ddos": is_ddos
        }
        super(SeverityRecord, self).__init__(**severity)
        pass

    def save(self):
        serialized = pickle.dumps(dict(self))
        self.redis.set(self.key, serialized)
        self.redis.expire(self.key, config.get('session_length', 1 * 60 * 60))
        pass

    def update_severity(self, value, is_ddos):
        self['severity'] = value
        self['is_ddos'] = is_ddos
        pass

    def remove_redis_record(self):
        self.redis.delete(self.key)
        pass
    pass

if __name__ == '__main__':
    s = SeverityRecord("xxx.xxx.xxx.xxx")
    s.save()
    s.update_severity(4, True)
    s.save()
    s.remove_redis_record()
    pass