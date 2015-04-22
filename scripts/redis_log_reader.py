from common.graphs.session_graph import SessionGraph
from common.records import TrafficRecord
from modeller.modeller import Modeller
from modeller.factors import *
from common import REDIS_POOL
from common import root_dir
import cPickle as pickle
import numpy as np
import operator
import redis
import time
import re
import os

# ips used in attacking
known_ddos_ip = [
    '124.43.187.61',
    '112.134.8.95',
    '124.43.168.240',
    '112.134.187.171',
    '61.245.173.19',
    '61.245.168.157',
    '61.245.163.160',
    '61.245.163.60'
]

# remove other possible data anomalies (cloudflare in this case)
ips_to_remove = [
    '199.27.130.186',
    '173.245.49.235',
    '173.245.50.125',
    '141.101.106.131'
]

# regex to identify bots
regex = re.compile(
    ur'^((?!Baiduspider|Googlebot|bingbot|Pingdom|Rome Client|Sogou|AhrefsBot|WordPress|Feedfetcher|Feedly|GoogleProducer|WeSEE|ADmantX|GrapeshotCrawler|DuckDuckGo|bot|Bot|Crawler|crawler|Yahoo|MegaIndex|panscient|spider|facebookexternalhit|Mediapartners|HaosouSpider).)*$')

# redis connection
r_db = redis.Redis(connection_pool=REDIS_POOL)
keys = r_db.keys('*type::transport*')
records = [pickle.loads(record) for record in r_db.mget(keys)]
records_dict = {}

# filter known bots / cloud flare anomalies from records
for r in records:
    if r['client_ip'] not in ips_to_remove:
        if r['user_agent'] is None or re.match(regex, r['user_agent']) is not None:
            records_dict[r['requested_time']] = TrafficRecord(record=r)
            pass
        pass
    pass

print "{} bot requests filtered out. Remains {} requests.".format(
    len(records) - len(records_dict), len(records_dict)
)

# sort by request time
filtered_sorted_records = sorted(records_dict.items(), key=operator.itemgetter(0))
keys = None
records = None
records_dict = None

# requires a ModelListener to model captured records
ml = Modeller()
ip_records = {}
counter = 0

# model the traffic and calculate values
for key, record in filtered_sorted_records:
    ml.model(
        None, record['client_ip'],
        traffic_record=record,
        persist_for_analysing=False
    )
    if record['client_ip'] in ip_records:
        ip_records[record['client_ip']] += 1
    else:
        ip_records[record['client_ip']] = 1
    counter += 1
    print "{} of {} records analyzed".format(
        counter, len(filtered_sorted_records)
    )
    pass

# sort factors by index
factors = {}
for Factor in BaseFactor.__subclasses__():
    factor = Factor(None, None, None)
    factors[factor._FACTOR_INDEX] = factor._FACTOR_KEY
    factor = None
    pass
factors = sorted(factors.items(), key=operator.itemgetter(0))

training_data = None
for ip in ip_records:
    data_record = []
    sg = SessionGraph(ip)

    if sg.get_graph_property("FactorBrowsingDepth") == 1 and sg.get_graph_property(
            "FactorPercentageConsecutiveRequests") > 90:
        print "ip : {}, requests : {}, ua : {}".format(ip, len(sg.get_graph_property("request_sequence")),
                                                       sg.get_graph_property("user_agents"))

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

for f_key in factors:
    print f_key
    pass

path = os.path.join(
    root_dir,
    "generated",
    "training_data",
    "training_data_{0}.npy".format(time.strftime("%Y_%m_%d_%H:%M"))
)
np.save(path, training_data)
print "done"