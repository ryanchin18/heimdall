__author__ = 'grainier'

from util import config
import redis


def process_message(m):
    key = m['data']
    session, type_val, hash_val = key.split('||')
    session = session.split('::')[1]
    type_val = type_val.split('::')[1]
    hash_val = hash_val.split('::')[1]
    channel = m['channel']
    command = channel[channel.rindex(':')+1:]
    print "command :", command, " | session :", session, " | type :", type_val, " | hash :", hash_val
    pass

r = redis.StrictRedis(
    config.redis.get('host', '127.0.0.1'),
    config.redis.get('port', '6379')
)

# read http://redis.io/topics/notifications to
# learn more about config key set (i.e. KEA)
r.config_set('notify-keyspace-events', 'EA')
sub = r.pubsub()

# subsscribe to keyspace events in separate thread (background process)
sub.psubscribe(**{'__key*__:*': process_message})  # ** for keyword args
thread = sub.run_in_thread(sleep_time=0.001)

# when it's time to shut it down...
# thread.stop()
# sub.close()
