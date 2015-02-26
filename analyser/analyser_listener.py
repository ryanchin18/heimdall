"""

"""
from listener import RedisListener


class AnalyserListener(RedisListener):
    def process(self, key, channel, command):
        try:
            session, type_val, hash_val = key.split('||')
            session = session.split('::')[1]
            type_val = type_val.split('::')[1]
            hash_val = hash_val.split('::')[1]
            print "command :", command, " | session :", session, " | type :", type_val, " | hash :", hash_val
        except ValueError, e:
            print "invalid key detected"
        pass

    def process_command(self, key, command, session, type_val, hash_val):
        command = command.lower()
        # only need to care about set, del, expired commands
        if type_val == 'transport' and command == 'set':

            pass

        elif type_val == 'transport' and command == 'del':

            pass

        elif type_val == 'transport' and command == 'expired':

            pass

        else:
            # default option
            pass
        pass

    pass