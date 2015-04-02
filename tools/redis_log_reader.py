import re
import numpy as np
from common import REDIS_POOL
from common.graphs.session_graph import SessionGraph
from common.records import TrafficRecord
from modeler import ModelerListener
import cPickle as pickle
import redis
import operator
from modeler.factors import *

known_ddos_ip = []
regex = re.compile(ur'^((?!Baiduspider|Googlebot|bingbot|Pingdom|Rome Client|Sogou|AhrefsBot|WordPress|Feedfetcher|Feedly|GoogleProducer|WeSEE|ADmantX|GrapeshotCrawler|DuckDuckGo|bot|Bot|Crawler|crawler|Yahoo|MegaIndex|panscient|spider|facebookexternalhit|Mediapartners|HaosouSpider).)*$')
r_db = redis.Redis(connection_pool=REDIS_POOL)
keys = r_db.keys('*type::transport*')
records = [pickle.loads(record) for record in r_db.mget(keys)]
records_dict = {}
# filter known bots from records
for r in records:
    if r['user_agent'] is None or re.match(regex, r['user_agent']) is not None:
        records_dict[r['requested_time']] = TrafficRecord(record=r)
        pass
    pass

filtered_sorted_records = sorted(records_dict.items(), key=operator.itemgetter(0))
keys = None
records = None
records_dict = None

# requires a ModelListener to model captured records
# initialize the ModelerListener but do not listen to events
ml = ModelerListener(connection_pool=REDIS_POOL)
ip_records = {}
counter = 0

# model and calculate values
for key, record in filtered_sorted_records:
    ml.process_command(None, 'set', record['client_ip'], 'transport',
                       None, traffic_record=record,
                       notify_analyser=False, bulk_restore=True)

    if record['client_ip'] in ip_records:
        ip_records[record['client_ip']] += 1
    else:
        ip_records[record['client_ip']] = 1
    counter += 1
    print "{} of {} records analyzed".format(counter, len(filtered_sorted_records))
    pass

factors = {}
for Factor in BaseFactor.__subclasses__():
    factor = Factor(None, None, None)
    factors[factor._FACTOR_INDEX] = factor._FACTOR_KEY
    pass
factors = sorted(factors.items(), key=operator.itemgetter(1))

training_data = None
for ip in ip_records:
    data_record = [ip]
    sg = SessionGraph(ip)

    if sg.get_graph_property("FactorBrowsingDepth") == 1 and sg.get_graph_property("FactorPercentageConsecutiveRequests") > 90:
        print "============================="
        print "ip : {}, requests : {}, ua : {}".format(ip, len(sg.get_graph_property("request_sequence")), sg.get_graph_property("user_agents"))
        print "============================="

    for f, f_key in factors:
        data_record.append(sg.get_graph_property(f_key))
        pass

    if ip in known_ddos_ip:
        data_record.append(1)
    else:
        data_record.append(0)
        pass

    if training_data is not None:
        training_data = np.vstack([training_data, data_record])
    else:
        training_data = np.array(data_record)
    pass


np.save("training_data", training_data)
# td = np.load("")
print "done."