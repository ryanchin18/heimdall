"""

"""
from common.graphs import SessionGraph, ApplicationGraph
from common import redis_key_template
from common.records import TrafficRecord
from common.listeners import RedisListener
from modeler.factors import *


class ModelerListener(RedisListener):
    def process(self, key, channel, command):
        if key and channel and command:
            try:
                session, type_val, hash_val = key.split('||')
                session = session.split('::')[1]
                type_val = type_val.split('::')[1]
                hash_val = hash_val.split('::')[1]
                self.process_command(key, command, session, type_val, hash_val)
            except ValueError, e:
                print "invalid key detected"
                pass
            pass
        pass

    def process_command(self, key, command, session, type_val, hash_val, traffic_record=None, notify_analyser=True):
        command = command.lower()
        # only need to care about set, del, expired commands
        if type_val == 'transport' and command == 'set':
            # get the session graph
            session_graph = SessionGraph(session)

            # get the traffic record
            if traffic_record is None:
                traffic_record = TrafficRecord(key)

            origin = traffic_record['origin_hash']
            destination = traffic_record['destination_hash']

            # add session to the graph
            session_graph.add_edge(
                {'vertex_id': origin},
                {'vertex_id': destination}
            )
            session_graph.print_graph()
            session_graph.save()

            # ----------------------------------------------------------------
            # REMOVE THIS LATER
            # TODO : This is just checking, have to write a better sync method
            ag = ApplicationGraph()
            ag.add_edge(
                {'vertex_id': origin},
                {'vertex_id': destination}
            )
            ag.remove_parallel_edges()
            ag.print_graph()
            ag.save()
            # ----------------------------------------------------------------

            # get the destination vertex
            destination_vertex = session_graph.get_vertex(destination)

            # update graph variables
            session_graph.update_request_intervals()
            session_graph.update_sequence(int(destination_vertex))
            session_graph.update_user_agent_usage(traffic_record['user_agent'])
            session_graph.update_response_code_usage(traffic_record['response_code'])
            session_graph.update_resource_type_usage(traffic_record['response_type'])
            session_graph.update_consecutive_requests(traffic_record['request_uri'])

            # compute and store factors on session graph
            for Factor in BaseFactor.__subclasses__():
                factor = Factor(session, session_graph, traffic_record)
                factor.compute()
                pass

            if notify_analyser:
                self.notify_analyser(session, hash_val)
            pass

        elif type_val == 'session' and command == 'expired':
            # TODO : Sync Sessions Graph with Application Graph
            # TODO : Delete everything related to that particular session
            pass

        else:
            # default option (do nothing)
            pass
        pass

    def notify_analyser(self, session, hash_val):
        self.set(redis_key_template.format(session, "analyse", hash_val), "analyser_event")
        pass
    pass