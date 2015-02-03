__author__ = 'grainier'

from interceptor_old import Router
from util import config, loggers
import sys

if __name__ == '__main__':
    # load server logger
    logger = loggers['server']

    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

    # initialize interceptor server
    server = Router(config)
    try:
        server.main_loop()
    except KeyboardInterrupt:
        logger.error('Ctrl C - Stopping server')
        print "Ctrl C - Stopping server"
        sys.exit(1)