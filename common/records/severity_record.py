"""

"""
from common import REDIS_POOL, config, redis_key_template
import cPickle as pickle
import redis


class SeverityRecord(dict):

    def __init__(self, ip, severity=None):
        self.key = redis_key_template.format(ip, "severity", None)
        self.redis = redis.Redis(connection_pool=REDIS_POOL)
        if severity:
            dictionary = {
                "ip": ip,
                "severity": severity
            }
            pass
        else:
            record = self.redis.get(self.key)
            if record:
                dictionary = pickle.loads(record)
                pass
            else:
                dictionary = {
                    "ip": ip,
                    "severity": 0
                }
                pass
            pass

        super(SeverityRecord, self).__init__(**dictionary)
        pass

    def save(self):
        serialized = pickle.dumps(dict(self))
        self.redis.set(self.key, serialized)
        self.redis.expire(self.key, config.get('ban_time', 5 * 60))
        pass

    def get_level(self):
        return self['severity']
        pass

    def update_severity(self, level):
        self['severity'] = level
        pass

    def remove_redis_record(self):
        self.redis.delete(self.key)
        pass

    pass

if __name__ == '__main__':
    s = SeverityRecord("xxx.xxx.xxx.xxx")
    s.save()
    s.update_severity(4)
    s.save()
    s.remove_redis_record()
    pass