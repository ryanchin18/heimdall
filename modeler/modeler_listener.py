"""

"""
from modeler import SessionGraph
from util import current_time_milliseconds
from listener import RedisListener
from modeler import TrafficRecord
from factors import *


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

    def process_command(self, key, command, session, type_val, hash_val):
        command = command.lower()
        # only need to care about set, del, expired commands
        if type_val == 'transport' and command == 'set':
            # TODO : Update Sessions Graph
            # TODO : Do NOT delete Traffic Record, It should be deleted from AnalyserListener

            # get the session graph
            session_graph = SessionGraph(session)

            # get the traffic record
            traffic_record = TrafficRecord(key)

            # update graph variables
            #   request / response count should be equal, therefore take traffic_record count

            #   user agents usage

            #   session length
            session_start = self._session_graph.session_start
            now = current_time_milliseconds()
            session_length_milliseconds = now - session_start
            session_length_seconds = float(session_length_milliseconds) / 1000.
            self.append_graph_factor('double', session_length_seconds)

            #   response codes returned




            # compute and store factors on session graph
            for Factor in BaseFactor.__subclasses__():
                factor = Factor(session, session_graph, traffic_record)
                factor.compute()
                pass
            pass

        elif type_val == 'session' and command == 'expired':
            # TODO : Sync Sessions Graph with Application Graph
            # TODO : Delete everything related to that particular session
            pass

        else:
            # default option (do nothing)
            pass
        pass
    pass