from common import REDIS_POOL
from common.records import TrafficRecord
import cPickle as pickle
import redis
import operator


r_db = redis.Redis(connection_pool=REDIS_POOL)
keys = r_db.keys('*type::transport*')
records = [pickle.loads(record) for record in r_db.mget(keys)]
records_dict = {}
for r in records:
    records_dict[r['requested_time']] = TrafficRecord(record=r)
    pass
sorted_records = sorted(records_dict.items(), key=operator.itemgetter(0))
keys = None
records = None
records_dict = None

# model and calculate values
for record in sorted_records:

    pass


