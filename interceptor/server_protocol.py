"""

"""
from StringIO import StringIO
from twisted.internet import protocol, reactor
from interceptor import ClientProtocol, HTTPRequest
from util import config


class ServerProtocol(protocol.Protocol):
    def __init__(self):
        self.buffer = None
        self.client = None
        self.config = config
        pass

    def connectionMade(self):
        factory = protocol.ClientFactory()
        factory.protocol = ClientProtocol
        factory.server = self
        reactor.connectTCP(
            self.config.destination.get('host', ''),
            self.config.destination.get('port', 80),
            factory
        )
        pass

    # Client => Proxy
    def dataReceived(self, data):
        # ------------------------------------------------------------
        # here we can extract http request content
        request = HTTPRequest(data)
        # content = request.rfile.read(len(data)) # this doesn't seem to be working
        content = StringIO(data).read(len(data))
        print("FROM CLIENT")
        print("Client IP: " + str(self.transport.getPeer()))
        print "Host:", request.headers.get('Host')
        print "Referer:", request.headers.get('Referer')
        print "User-Agent:", request.headers.get('User-Agent')
        print "Accept:", request.headers.get('Accept')
        print "Accept-Language:", request.headers.get('Accept-Language')
        print "Accept-Encoding:", request.headers.get('Accept-Encoding')
        print "DNT:", request.headers.get('DNT')
        print "Connection:", request.headers.get('Connection')
        print "Cache-Control:", request.headers.get('Cache-Control')
        print "Data Length:", len(data)
        print "Content Length:", len(content)
        print "Content Size:", len(content) / 1024, 'kb'
        print "Content:", content
        # ------------------------------------------------------------

        # continue with the response
        if self.client:
            self.client.write(data)
            pass
        else:
            self.buffer = data
            pass
        pass

    # Proxy => Client
    def write(self, data):
        self.transport.write(data)
        pass

    pass