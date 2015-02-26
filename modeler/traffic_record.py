"""

"""
from util import config
import cPickle as pickle
import redis


class TrafficRecord(dict):
    def __init__(self, key):
        self.key = key
        self.redis = redis.StrictRedis(
            config.redis.get('host', '127.0.0.1'),
            config.redis.get('port', '6379')
        )
        traffic_str = self.redis.get(key)
        if traffic_str:
            dictionary = pickle.loads(traffic_str)
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
    t = TrafficRecord("session::192.168.1.100||type::transport||hash::dfa34dd79637b34fa17cfd8f26d9daeb")
    print "x"
    pass