"""

"""
from common.listeners import RedisListener
from analyser import Analyser


class AnalyserListener(RedisListener):
    def __init__(self, *args, **kwargs):
        super(AnalyserListener, self).__init__(*args, **kwargs)
        self.analyser = Analyser()
        pass

    def process(self, key, channel, command):
        if key and channel and command:
            try:
                session, type_val, hash_val = key.split('||')
                session = session.split('::')[1]
                type_val = type_val.split('::')[1]
                hash_val = hash_val.split('::')[1]

                command = command.lower()
                if type_val == 'analyse' and command == 'set':
                    self.analyser.analyse(session, key)
                else:
                    # ignore the event
                    pass
            except ValueError, e:
                print "invalid key detected"
                pass
            pass
        pass
    pass