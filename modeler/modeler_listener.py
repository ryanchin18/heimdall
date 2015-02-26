"""

"""
from listener import RedisListener
from modeler import TrafficRecord


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