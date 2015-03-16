"""
http://stackoverflow.com/questions/15640640/python-twisted-man-in-the-middle-implementation/15645169#15645169
http://www.mostthingsweb.com/2013/08/a-basic-man-in-the-middle-proxy-with-twisted/
"""
from twisted.internet import protocol, reactor
from twisted.python import log
from interceptor import ServerProtocol
from modeler import ModelerListener
from analyser import AnalyserListener
from common import config
import sys


def run():
    log.startLogging(sys.stdout)

    # initialize the ModelerListener and listen on a separate thread
    ml = ModelerListener(
        config.redis.get('host', '127.0.0.1'),
        config.redis.get('port', '6379')
    )
    ml.listen()

    # initialize the AnalyserListener and listen on a separate thread
    al = AnalyserListener(
        config.redis.get('host', '127.0.0.1'),
        config.redis.get('port', '6379')
    )
    al.listen()

    # initialize and start the interceptor reactor
    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol
    reactor.listenTCP(config.interceptor.get('port', 9191), factory)
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