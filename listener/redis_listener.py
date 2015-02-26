"""

"""
from util import config
import redis


class RedisListener(redis.StrictRedis):
    def __init__(self, *args, **kwargs):
        super(RedisListener, self).__init__(*args, **kwargs)
        # read http://redis.io/topics/notifications to
        # learn more about config key set (i.e. KEA)
        self.config_set('notify-keyspace-events', 'EA')
        self.subscriber = self.pubsub()
        self.listener_thread = None
        pass

    def __callback(self, m):
        try:
            key = m['data']
            channel = m['channel']
            command = channel[channel.rindex(':')+1:]
            self.process(key, channel, command)
            pass
        except ValueError, e:
            self.process(None, None, None)
        pass

    def listen(self):
        # subscribe to keys events as a background process
        self.subscriber.psubscribe(**{'__key*__:*': self.__callback})  # ** for kwargs
        self.listener_thread = self.subscriber.run_in_thread(sleep_time=0.001)
        pass

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

    def stop(self):
        if self.listener_thread:
            self.listener_thread.stop()
        self.subscriber.close()
        pass

    pass

if __name__ == '__main__':
    rl = RedisListener(
        config.redis.get('host', '127.0.0.1'),
        config.redis.get('port', '6379')
    )
    rl.listen()
    pass
