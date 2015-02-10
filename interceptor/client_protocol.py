"""

"""
from twisted.internet import protocol
from interceptor import parse_response


class ClientProtocol(protocol.Protocol):
    def __init__(self):
        pass

    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''
        pass

    # Server => Proxy
    def dataReceived(self, data):
        # ------------------------------------------------------------
        # here we can extract http response content
        response = parse_response(data)
        content = response.read(len(data))
        print("FROM SERVER")
        print("Server IP : " + str(self.transport.getPeer()))
        print "status:", response.status
        print "Date:", response.getheader('Date')
        print "Server:", response.getheader('Server')
        print "X-Powered-By:", response.getheader('X-Powered-By')
        print "Content-Length:", response.getheader('Content-Length')
        print "Keep-Alive:", response.getheader('Keep-Alive')
        print "Connection:", response.getheader('Connection')
        print "Content-Type:", response.getheader('Content-Type')
        print "Data Length:", len(data)
        print "Content Length:", len(content)
        print "Content Size:", len(content) / 1024, 'kb'
        print "Content:", content
        # ------------------------------------------------------------

        # continue with the response
        self.factory.server.write(data)
        pass

    # Proxy => Server
    def write(self, data):
        if data:
            self.transport.write(data)
            pass
        pass

    pass