from common import REDIS_POOL
from common.records import TrafficRecord
from modeler import ModelerListener
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

# requires a ModelListener to model captured records
# initialize the ModelerListener but do not listen to events
ml = ModelerListener(connection_pool=REDIS_POOL)

# model and calculate values
for record in sorted_records:
    ml.process_command(None, 'set', record['client_ip'], 'transport', None, traffic_record=record, notify_analyser=False)
    print "Done"
    pass


