"""

"""
from common import config, redis_key_template
import cPickle as pickle
import redis


class TrafficRecord(dict):
    def __init__(self, key):
        self.key = key
        self.redis = redis.StrictRedis(
            config.redis.get('host', '127.0.0.1'),
            config.redis.get('port', '6379')
        )
        record = self.redis.get(key)
        if record:
            dictionary = pickle.loads(record)
        else:
            dictionary = {}
        super(TrafficRecord, self).__init__(**dictionary)
        pass

    def populate(self):

        pass

    def calculate(self):

        pass

    def remove_redis_record(self):
        self.redis.delete(self.key)
        pass

    pass

if __name__ == '__main__':
    t = TrafficRecord(redis_key_template.format("192.168.1.100", "transport", "dfa34dd79637b34fa17cfd8f26d9daeb"))
    print "x"
    pass