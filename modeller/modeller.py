__author__ = 'grainier'
from common.graphs import SessionGraph
from common import redis_key_template
from common.records import TrafficRecord
from common import REDIS_POOL
from factors import *
import cPickle as pickle
import numpy as np
import operator
import redis


class Modeller(object):
    def __init__(self):
        self.redis = redis.Redis(connection_pool=REDIS_POOL)
        pass

    def model(self, key, session, traffic_record=None, persist_for_analysing=True):
        factors = {}
        sg = SessionGraph(session)
        if traffic_record is None:
            traffic_record = TrafficRecord(key)
            pass
        origin = traffic_record['origin_hash']
        destination = traffic_record['destination_hash']

        # add session to the graph
        sg.add_edge(
            {'vertex_id': origin},
            {'vertex_id': destination}
        )
        destination_vertex = sg.get_vertex(destination)

        # update graph variables
        sg.update_request_intervals()
        sg.update_sequence(int(destination_vertex))
        sg.update_user_agent_usage(traffic_record['user_agent'])
        sg.update_response_code_usage(traffic_record['response_code'])
        sg.update_resource_type_usage(traffic_record['response_type'])
        sg.update_consecutive_requests(traffic_record['request_uri'])

        # compute and store factors on session graph
        for Factor in BaseFactor.__subclasses__():
            factor = Factor(session, sg, traffic_record)
            factors[factor._FACTOR_INDEX] = factor._FACTOR_KEY
            factor.compute()
            pass

        # after all the calculations, graph should get saved
        sg.save()

        if persist_for_analysing:
            # persisting a record will notify the analyser to analyse that record
            factors = sorted(factors.items(), key=operator.itemgetter(1))
            factor_values = []
            for f, f_key in factors:
                factor_values.append(sg.get_graph_property(f_key))
                pass
            record = np.array(factor_values)
            self.persist_record(session, record)
            traffic_record.remove_redis_record()
            # sg.print_graph()
        pass

    def persist_record(self, session, record):
        serialized = pickle.dumps(record)
        # md5_sum = hashlib.md5(serialized).hexdigest()
        # self.redis.set(redis_key_template.format(session, "analyse", md5_sum), serialized)
        # using the same key will reduce workload in analyser
        self.redis.set(redis_key_template.format(session, "analyse", None), serialized)
        pass
    pass