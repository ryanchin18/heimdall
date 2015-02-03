"""

"""
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
        # -------------------------------------------------------------------
        request = HTTPRequest(data)
        print("SP : " + str(self.transport.getPeer()))
        print(vars(request))
        # here we can extract http headers
        if hasattr(request, 'headers'):
            content_len = int(request.headers.getheader('content-length', 0))
            post_body = request.rfile.read(content_len)
            print('--------------------------------------------------------')
            print("FROM CLIENT")
            print('body : %s' % post_body)
            print request.headers.dict
            print self.client
            print('--------------------------------------------------------')
            pass
        # -------------------------------------------------------------------

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