"""

"""
from config import Config
import logging
import logging.config
import os

conf_dir = os.path.join(os.path.dirname(__file__), '../conf')

# load the server.conf file
config = Config(file('%s/server.conf' % conf_dir))

# load the logging.conf file
logging.config.fileConfig('%s/logging.conf' % conf_dir)

# initialize loggers
loggers = {
    'server': logging.getLogger('server'),
    # other loggers goes here
}

