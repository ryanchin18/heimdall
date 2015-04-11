from twisted.internet import reactor
from twisted.python import log
from interceptor import ProxyFactory
from modeler import ModelerListener
from analyser import AnalyserListener
from common import REDIS_POOL, config
import sys


def run():
    log.startLogging(sys.stdout)

    # initialize the ModelerListener and listen on a separate thread
    ml = ModelerListener(connection_pool=REDIS_POOL)
    ml.listen()

    # initialize the AnalyserListener and listen on a separate thread
    al = AnalyserListener(connection_pool=REDIS_POOL)
    al.listen()

    # initialize and start the interceptor reactor
    reactor.listenTCP(config.interceptor.get('port', 9191), ProxyFactory())
    reactor.run()

    # this is only reachable once the reactor
    # is shutdown. once the reactor receive SIGINT
    # and shutdown stop the Event Listeners too.
    ml.stop()
    al.stop()
    pass


if __name__ == '__main__':
    run()
    pass