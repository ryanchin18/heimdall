"""

"""
from common.listeners import RedisListener
from modeller import Modeller


class ModellerListener(RedisListener):
    def __init__(self, *args, **kwargs):
        super(ModellerListener, self).__init__(*args, **kwargs)
        self.modeller = Modeller()
        pass

    def process(self, key, channel, command):
        if key and channel and command:
            try:
                session, type_val, hash_val = key.split('||')
                session = session.split('::')[1]
                type_val = type_val.split('::')[1]
                hash_val = hash_val.split('::')[1]

                command = command.lower()
                if type_val == 'transport' and command == 'set':
                    try:
                        self.modeller.model(key, session)
                    except Exception, e:
                        print e
                        pass
                else:
                    # ignore the event
                    pass
            except ValueError, e:
                print "invalid key detected"
                pass
            pass
        pass
    pass