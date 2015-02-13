"""

"""
import re
import hashlib
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
        # Need to get time (If there is a way)

        # ------------------------------------------------------------
        # here we can extract http response content
        response = parse_response(data)
        content = response.read(len(data))
        rq_uri = self.factory.server.request_uri
        print "Request-URI", rq_uri
        print "FROM SERVER"
        print "Server IP : ", str(self.transport.getPeer())
        print "Client IP : ", str(self.factory.server.transport.getPeer())
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

        # ------------------------------------------------------------
        # Manipulate responses
        # Only if it seems to be ref is disabled / or faked
        # append md5 encoded referer as md5_ref

        man_data = data
        # man_data = unicode(data, 'utf8')

        # strip get parameters
        try:
            rq_uri = rq_uri[:rq_uri.index('?')]
            pass
        except ValueError:
            pass

        # md5 the rq_uri
        md5_ref = hashlib.md5(rq_uri).hexdigest()

        # TODO : add to redis (as reference)

        # TODO : check is resource???? if resource do not manipulate

        # inject for href surround with " or ' or none of them ie : href=about.php
        # ur'href=([\"|\'])([^"]+)([\"|\'])'
        man_data = re.sub(ur'href(=\"|=\'|=)(.*?)(\"|\'|>| |/>)', (
            lambda m:
                'href{0}{1}&o_ref={3}{2}'.format(m.group(1), m.group(2), m.group(3), md5_ref) if '?' in m.group(2)
                else 'href{0}{1}?o_ref={3}{2}'.format(m.group(1), m.group(2), m.group(3), md5_ref)
        ), data)
        # ------------------------------------------------------------

        # continue with the response
        # self.factory.server.write(data)
        self.factory.server.write(man_data)
        pass

    # Proxy => Server
    def write(self, data):
        if data:
            self.transport.write(data)
            pass
        pass

    pass