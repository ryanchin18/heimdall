"""

"""
import httplib
import re
import hashlib
from twisted.internet import protocol
from urlparse import urlparse, parse_qs
from interceptor import parse_response
from modeler import BaseGraph
from util import config
import redis


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
        try:
            content = response.read(len(data))
        except httplib.IncompleteRead as e:
            content = e.partial

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
        man_data = data

        url = urlparse(rq_uri)
        rq_uri = url.path
        rq_params = parse_qs(url.query)
        rq_ref = rq_params['o_ref'][0] if 'o_ref' in rq_params else None

        # md5 the rq_uri
        md5_ref = hashlib.md5(rq_uri).hexdigest()

        # ------------------------------------------------------------
        # add to redis (as reference)
        r = redis.StrictRedis(self.config.redis.get('host', '127.0.0.1'), self.config.redis.get('port', '6379'))
        r.set('url_{}'.format(md5_ref), rq_uri)

        # add to graph
        b = BaseGraph()
        b.add_edge(
            {'vertex_id': rq_ref},
            {'vertex_id': md5_ref}
        )
        b.print_graph()
        b.save()
        b = None
        # ------------------------------------------------------------

        # get the file type (file extinction)
        try:
            f_type = rq_uri[rq_uri.rindex('.'):]
            pass
        except ValueError:
            f_type = None
            pass

        if f_type not in self.config.RESOURCE_FILE_TYPES:
            # if the file type not in RESOURCE_FILE_TYPES, manipulate the content and inject o_ref values
            man_data = re.sub(ur'(href|src)(=\"|=\'|=)(.*?)(\"|\'|>| |/>)', (
                lambda m:
                    '{0}{1}{2}&o_ref={4}{3}'.format(
                        m.group(1),
                        m.group(2),
                        m.group(3),
                        m.group(4),
                        md5_ref
                    )
                    if '?' in m.group(3)
                    else '{0}{1}{2}?o_ref={4}{3}'.format(
                        m.group(1),
                        m.group(2),
                        m.group(3),
                        m.group(4),
                        md5_ref
                    )
            ), data)

            # fix content length according to new content
            cl_diff = len(man_data) - len(data)
            man_data = re.sub(ur'Content-Length(?::|: )(\d+)(?:\n|\r\n)', (
                lambda m:
                    'Content-Length: {}\r\n'.format(
                        str(int(m.group(1)) + cl_diff)
                    )
            ), man_data)

            print "DATA Length:", len(data)
            print "MAN DATA Length:", len(man_data)
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