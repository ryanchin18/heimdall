"""

"""
from config import Config
import logging
import logging.config
import os
import time
import redis

conf_dir = os.path.join(os.path.dirname(__file__), '../conf')

root_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]

# load the server.conf file
config = Config(file('%s/server.conf' % conf_dir))

# load the logging.conf file
logging.config.fileConfig('%s/logging.conf' % conf_dir)

# initialize loggers
loggers = {
    'server': logging.getLogger('server'),
    # other loggers goes here
}

current_time_milliseconds = lambda: int(round(time.time() * 1000))

# this template should be used to store records on redis
redis_key_template = "session::{0}||type::{1}||hash::{2}"

# redis connection pool for multiple connections
# refer to http://stackoverflow.com/questions/13431803/python-redis-connections
REDIS_POOL = redis.ConnectionPool(
    host=config.redis.get('host', '127.0.0.1'),
    port=config.redis.get('port', '6379'),
    db=config.redis.get('db', 0)
)