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
            factor = None
            pass

        # after all the calculations, graph should get saved
        sg.save()

        if persist_for_analysing:
            # persisting a record will notify the analyser to analyse that record
            factors = sorted(factors.items(), key=operator.itemgetter(0))
            fv_arr = []
            fv_map = {}
            for f_index, f_key in factors:
                f_val = sg.get_graph_property(f_key)
                fv_arr.append(f_val)
                fv_map[f_key] = f_val
                pass
            record = np.array(fv_arr)
            self.persist_record(session, record)
            self.persist_factor_map(session, fv_map)
            traffic_record.remove_redis_record()
            # sg.print_graph()
        pass

    def persist_record(self, session, record):
        serialized = pickle.dumps(record)
        # using the same key will reduce workload in analyser
        self.redis.set(redis_key_template.format(session, "analyse", None), serialized)
        pass

    def persist_factor_map(self, session, factor_map):
        serialized = pickle.dumps(factor_map)
        self.redis.set(redis_key_template.format(session, "factors", None), serialized)
        pass

    pass