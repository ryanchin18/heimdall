"""

"""
import re
import hashlib
from twisted.internet import protocol
from interceptor import parse_response
from util import config


class ClientProtocol(protocol.Protocol):
    def __init__(self):
        self.config = config
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
        # print "FROM SERVER"
        # print "Server IP : ", str(self.transport.getPeer())
        # print "Client IP : ", str(self.factory.server.transport.getPeer())
        # print "status:", response.status
        # print "Date:", response.getheader('Date')
        # print "Server:", response.getheader('Server')
        # print "X-Powered-By:", response.getheader('X-Powered-By')
        print "Content-Length:", response.getheader('Content-Length')
        # print "Keep-Alive:", response.getheader('Keep-Alive')
        # print "Connection:", response.getheader('Connection')
        # print "Content-Type:", response.getheader('Content-Type')
        # print "Data Length:", len(data)
        print "Content Length:", len(content)
        # print "Content Size:", len(content) / 1024, 'kb'
        # print "Content:", content
        # ------------------------------------------------------------

        # ------------------------------------------------------------
        # Manipulate responses
        # Only if it seems to be ref is disabled / or faked
        # append md5 encoded referer as md5_ref

        # md5 the rq_uri
        md5_ref = hashlib.md5(rq_uri).hexdigest()

        # TODO : add to redis (as reference)

        man_data = data
        # man_data = unicode(data, 'utf8') # do not use unicode

        # strip get parameters
        try:
            rq_uri = rq_uri[:rq_uri.index('?')]
            pass
        except ValueError:
            pass

        # get the file type (file extinction)
        try:
            f_type = rq_uri[rq_uri.rindex('.'):]
            pass
        except ValueError:
            f_type = None
            pass

        if f_type not in self.config.IGNORE_FILE_TYPES:
            # If the file type not in IGNORE_FILE_TYPES, manipulate the content and inject o_ref values
            # inject for href surround with " or ' or none of them ie : href=about.php
            # ur'href=([\"|\'])([^"]+)([\"|\'])'
            man_data = re.sub(ur'href(=\"|=\'|=)(.*?)(\"|\'|>| |/>)', (
                lambda m:
                    'href{0}{1}&o_ref={3}{2}'.format(m.group(1), m.group(2), m.group(3), md5_ref) if '?' in m.group(2)
                    else 'href{0}{1}?o_ref={3}{2}'.format(m.group(1), m.group(2), m.group(3), md5_ref)
            ), data)

            # TODO - Have to fix content length according to new content
            cl_diff = len(man_data) - len(data)
            man_data = re.sub(ur'Content-Length(?::|: )(\d+)(?:\n|\r\n)', (
                lambda m:
                    'Content-Length: {}\r\n'.format(str(int(m.group(1)) + cl_diff))
            ), man_data)
            print "DATA Length:",
            print "MAN DATA Length:",
            pass

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