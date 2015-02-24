"""
http://stackoverflow.com/questions/15640640/python-twisted-man-in-the-middle-implementation/15645169#15645169
http://www.mostthingsweb.com/2013/08/a-basic-man-in-the-middle-proxy-with-twisted/
"""
from twisted.internet import protocol, reactor
from twisted.python import log
from interceptor import ServerProtocol
from util import config
import sys


def run():
    log.startLogging(sys.stdout)

    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol

    reactor.listenTCP(config.interceptor.get('port', 9191), factory)
    reactor.run()
    pass


if __name__ == '__main__':
    run()
    pass