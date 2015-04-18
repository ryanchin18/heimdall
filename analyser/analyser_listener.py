"""

"""
from common.listeners import RedisListener
from common.settings import current_time_milliseconds, redis_key_template
from analyser import Analyser


class AnalyserListener(RedisListener):
    def __init__(self, *args, **kwargs):
        super(AnalyserListener, self).__init__(*args, **kwargs)
        self.analyser = Analyser()
        self.queue = []
        self.last_Process = current_time_milliseconds()
        self.max_interval = 1000 * 20
        self.queue_limit = 100
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
                    try:
                        self.queue.append(session)
                        diff = abs(current_time_milliseconds() - self.last_Process)
                        if len(self.queue) > self.queue_limit or diff > self.max_interval:
                            self.process_queue()
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

    def process_queue(self):
        self.last_Process = current_time_milliseconds()
        queue = list(set(self.queue))
        self.queue = []

        for s in queue:
            k = redis_key_template.format(s, "analyse", None)
            self.analyser.analyse(s, k)
        pass
    pass