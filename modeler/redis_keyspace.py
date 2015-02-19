__author__ = 'grainier'

from util import config
import redis


def print_message(m):
    print m
    pass

r = redis.StrictRedis(
    config.redis.get('host', '127.0.0.1'),
    config.redis.get('port', '6379')
)

# read http://redis.io/topics/notifications to
# learn more about config key set (i.e. KEA)
r.config_set('notify-keyspace-events', 'KEA')
sub = r.pubsub()

# subsscribe to keyspace events in separate thread (background process)
sub.psubscribe(**{'__key*__:*': print_message})  # ** for keyword args
thread = sub.run_in_thread(sleep_time=0.001)

# when it's time to shut it down...
thread.stop()
sub.close()
