"""

"""
from common import REDIS_POOL, redis_key_template
import cPickle as pickle
from urlparse import urlparse, parse_qs
import hashlib
import redis


class TrafficRecord(dict):
    def __init__(self, key=None, record=None):
        if key is not None:
            self.key = key
            self.redis = redis.Redis(connection_pool=REDIS_POOL)
            record = self.redis.get(key)
            if record:
                dictionary = pickle.loads(record)
            else:
                dictionary = {}
        elif record is not None:
            dictionary = record
        else:
            dictionary = {}

        super(TrafficRecord, self).__init__(**dictionary)
        # TODO : Possible exception
        self.add_missing_attributes()
        pass

    def populate(self):

        pass

    def add_missing_attributes(self):
        url = urlparse(self['request_uri'])
        # strip off query parameters
        self['request_uri'] = url.path if url.path == '/' else url.path.rstrip('/')

        if "origin_hash" not in self:
            if "referer" in self and self['referer']:
                ref_u = urlparse(self['referer'])
                rq_ref_path = ref_u.path if ref_u.path == '/' else ref_u.path.rstrip('/')
                self["origin_hash"] = hashlib.md5(rq_ref_path).hexdigest()
                self.redis.set(redis_key_template.format("any", "url", self["origin_hash"]), rq_ref_path)
                pass
            else:
                rq_params = parse_qs(url.query)
                self["origin_hash"] = rq_params['o_ref'][0] if 'o_ref' in rq_params else None
                pass
            pass

        if "destination_hash" not in self:
            self["destination_hash"] = hashlib.md5(self['request_uri']).hexdigest()
            self.redis.set(redis_key_template.format("any", "url", self["destination_hash"]), self['request_uri'])
            pass

        if "response_type" not in self:
            try:
                self['response_type'] = self['request_uri'][self['request_uri'].rindex('.'):]
            except ValueError:
                self['response_type'] = 'unknown'
                pass
            pass
        pass

    def remove_redis_record(self):
        self.redis.delete(self.key)
        pass

    pass

if __name__ == '__main__':
    t = TrafficRecord(redis_key_template.format("192.168.1.100", "transport", "dfa34dd79637b34fa17cfd8f26d9daeb"))
    print "x"
    pass