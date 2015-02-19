"""

"""
import httplib
import re
import hashlib
from twisted.internet import protocol
from urlparse import urlparse, parse_qs
from interceptor import parse_response
from modeler import SessionGraph
from util import config
import redis


class ClientProtocol(protocol.Protocol):
    def __init__(self):
        self.config = config
        self.redis = redis.StrictRedis(
            self.config.redis.get('host', '127.0.0.1'),
            self.config.redis.get('port', '6379')
        )
        pass

    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''
        pass

    # Server => Proxy
    def dataReceived(self, data):
        # here we can extract http response content
        response = parse_response(data)
        ori_len = len(data)
        try:
            content = response.read(ori_len)
        except httplib.IncompleteRead as e:
            content = e.partial

        rq_uri = self.factory.server.request_uri
        rq_ref_url = self.factory.server.referer
        rq_cilent_ip = str(self.factory.server.transport.getPeer().host)

        # this request's response url will be the referrer of
        # requests originated from rendered response
        url = urlparse(rq_uri)
        rq_uri_path = url.path if url.path == '/' else url.path.rstrip('/')
        res_ref = hashlib.md5(rq_uri_path).hexdigest()
        self.redis.set('session:{0}.url.{1}'.format(rq_cilent_ip, res_ref), rq_uri_path)

        if rq_ref_url:
            # client request has referer without "o_ref" injecting
            # referer for this request
            ref_u = urlparse(rq_ref_url)
            rq_ref_path = ref_u.path if ref_u.path == '/' else ref_u.path.rstrip('/')
            rq_ref = hashlib.md5(rq_ref_path).hexdigest()
            self.redis.set('session:{0}.url.{1}'.format(rq_cilent_ip, rq_ref), rq_ref_path)

            pass
        else:
            # client request doesn't have referrer. have to inject "o_ref"
            # referrer for this request
            rq_params = parse_qs(url.query)
            rq_ref = rq_params['o_ref'][0] if 'o_ref' in rq_params else None

            # get the file type (file extinction) of response that's going to generate
            try:
                f_type = rq_uri_path[rq_uri_path.rindex('.'):]
                pass
            except ValueError:
                f_type = None
                pass

            if f_type not in self.config.DO_NOT_TAMPER_FILE_TYPES:
                # if the file type not in DO_NOT_TAMPER_FILE_TYPES,
                # manipulate the content and inject o_ref values
                man_data = re.sub(ur'(href|src)(=\"|=\'|=)(.*?)(\"|\'|>| |/>)', (
                    lambda m:
                    '{0}{1}{2}&o_ref={4}{3}'.format(
                        m.group(1),
                        m.group(2),
                        m.group(3),
                        m.group(4),
                        res_ref
                    )
                    if '?' in m.group(3)
                    else '{0}{1}{2}?o_ref={4}{3}'.format(
                        m.group(1),
                        m.group(2),
                        m.group(3),
                        m.group(4),
                        res_ref
                    )
                ), data)

                # fix content length according to new content
                cl_diff = len(man_data) - ori_len
                man_data = re.sub(ur'Content-Length(?::|: )(\d+)(?:\n|\r\n)', (
                    lambda m:
                    'Content-Length: {}\r\n'.format(
                        str(int(m.group(1)) + cl_diff)
                    )
                ), man_data)
                print "Content-Length Diff:{}".format(len(man_data) - ori_len)
                data = man_data
                man_data = None
                pass
            pass

        # ------------------------------------------------------------
        # TODO : Need to get time (If there is a way)
        r_server_ip = str(self.transport.getPeer().host)
        r_client_ip = rq_cilent_ip
        r_response_status = response.status
        r_date = response.getheader('Date')
        r_server = response.getheader('Server')
        r_x_powered_by = response.getheader('X-Powered-By')
        r_res_content_length = int(response.getheader('Content-Length')) if response.getheader('Content-Length') else len(content)
        r_keep_alive = response.getheader('Keep-Alive')
        r_connection = response.getheader('Connection')
        r_content_type = response.getheader('Content-Type')
        r_data_length = ori_len
        r_res_content_size = r_res_content_length / 1024, 'kb'
        r_res_content = content
        print "Request-URI", rq_uri_path
        print "Content-Length:", response.getheader('Content-Length')

        # ------------------------------------------------------------
        # add to session graph
        b = SessionGraph(r_client_ip)
        b.add_edge(
            {'vertex_id': rq_ref},
            {'vertex_id': res_ref}
        )
        b.print_graph()
        b.save()

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