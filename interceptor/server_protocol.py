"""

"""
from twisted.internet import protocol, reactor
from interceptor import ClientProtocol, HTTPRequest

LISTEN_PORT = 9191
SERVER_PORT = 80
SERVER_ADDR = "127.0.0.1"


class ServerProtocol(protocol.Protocol):
    def __init__(self):
        self.buffer = None
        self.client = None
        pass

    def connectionMade(self):
        factory = protocol.ClientFactory()
        factory.protocol = ClientProtocol
        factory.server = self
        reactor.connectTCP(SERVER_ADDR, SERVER_PORT, factory)
        pass

    # Client => Proxy
    def dataReceived(self, data):
        #-------------------------------------------------------------------
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
        #-------------------------------------------------------------------

        if self.client:
            self.client.write(data)
            pass
        else:
            self.buffer = data
            pass
        pass

    def allContentReceived(self):
        pass

    # Proxy => Client
    def write(self, data):
        self.transport.write(data)
        pass

    pass