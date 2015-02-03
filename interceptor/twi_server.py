"""
http://stackoverflow.com/questions/15640640/python-twisted-man-in-the-middle-implementation/15645169#15645169
http://www.mostthingsweb.com/2013/08/a-basic-man-in-the-middle-proxy-with-twisted/
"""
from twisted.internet import protocol, reactor
from interceptor import ServerProtocol
from util import config


def main():
    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol

    reactor.listenTCP(config.interceptor.get('port', 9191), factory)
    reactor.run()


if __name__ == '__main__':
    main()