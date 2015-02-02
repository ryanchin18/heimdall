"""

"""
from twisted.internet import protocol
from interceptor import HTTPRequest


class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''
        print("CP : " + str(self.transport.getPeer()))


    # Server => Proxy
    def dataReceived(self, data):
        self.factory.server.write(data)

        #-------------------------------------------------------------------
        request = HTTPRequest(data)
        print(vars(request))
        # here we can extract http headers
        if hasattr(request, 'headers'):
            content_len = int(request.headers.getheader('content-length', 0))
            post_body = request.rfile.read(content_len)
            print('--------------------------------------------------------')
            print("FROM SERVER")
            print('body : %s' % post_body)
            print request.headers.dict
            print self.client
            print('--------------------------------------------------------')
        #-------------------------------------------------------------------

    # Proxy => Server
    def write(self, data):
        if data:
            self.transport.write(data)