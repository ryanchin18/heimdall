__author__ = 'grainier'

from config import Config
import logging
import logging.config

# load the server.conf file
config = Config(file('../conf/server.conf'))

# load the logging.conf file
logging.config.fileConfig('../conf/logging.conf')

# initialize loggers
loggers = {
    'server': logging.getLogger('server'),
    # other loggers goes here
}

