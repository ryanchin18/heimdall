"""

"""
from common.listener import RedisListener
from common.graph import SessionGraph
from common import SeverityRecord, redis_key_template


class AnalyserListener(RedisListener):
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
        if type_val == 'analyse' and command == 'set':
            # load respective session graph
            session_graph = SessionGraph(session)

            # analyse the factors
            arst = session_graph.get_graph_property('FactorAverageResponseTime')
            arqi = session_graph.get_graph_property('FactorAverageRequestInterval')

            diff = arqi - arst
            s = 0 if diff > 0 else (-1 * diff)

            # set severity after analysing
            severity = SeverityRecord(session, s)
            severity.save()

            print "Analysed : ", key

            self.clean_garbage(session, hash_val)
            pass
        else:
            # default option
            pass
        pass

    def clean_garbage(self, session, hash_val):
        self.delete(redis_key_template.format(session, "transport", hash_val))
        self.delete(redis_key_template.format(session, "analyse", hash_val))
        pass

    pass