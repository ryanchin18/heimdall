"""

"""
import re
import hashlib
from twisted.internet import protocol
from urlparse import urlparse, parse_qs
from interceptor import parse_response
from modeler import SessionGraph, ApplicationGraph
from common import config, current_time_milliseconds
import cPickle as pickle
import redis


class ClientProtocol(protocol.Protocol):
    def __init__(self):
        self.redis = redis.StrictRedis(
            config.redis.get('host', '127.0.0.1'),
            config.redis.get('port', '6379')
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
        request_data = self.factory.server.request

        rq_uri = request_data['request_uri']
        rq_ref_url = request_data['referer']
        rq_cilent_ip = request_data['client_ip']

        # url of response for this request will be the referrer of
        # requests originated from rendered response
        url = urlparse(rq_uri)
        rq_uri_path = url.path if url.path == '/' else url.path.rstrip('/')
        res_ref = hashlib.md5(rq_uri_path).hexdigest()
        self.redis.set('session::any||type::url||hash::{0}'.format(res_ref), rq_uri_path)

        # get the file type (file extinction) of response that's going to generate
        try:
            f_type = rq_uri_path[rq_uri_path.rindex('.'):]
            pass
        except ValueError:
            f_type = 'unknown'
            pass

        if rq_ref_url:
            # client request has referer without "o_ref" injecting
            # referer for this request
            ref_u = urlparse(rq_ref_url)
            rq_ref_path = ref_u.path if ref_u.path == '/' else ref_u.path.rstrip('/')
            rq_ref = hashlib.md5(rq_ref_path).hexdigest()
            self.redis.set('session::any||type::url||hash::{0}'.format(rq_ref), rq_ref_path)
            pass
        else:
            # client request doesn't have referrer. have to inject "o_ref"
            # referrer for this request
            rq_params = parse_qs(url.query)
            rq_ref = rq_params['o_ref'][0] if 'o_ref' in rq_params else None
            man_data = data  # take a copy of original data

            if config.get('force_append_referrer', False):
                if f_type not in config.do_not_tamper_file_types:
                    # if the file type not in DO_NOT_TAMPER_FILE_TYPES,
                    # manipulate the content and inject o_ref values
                    man_data = re.sub(r'(href|src)(=\"|=\'|=)(.*?)(\"|\'|>| |/>)', (
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
                    ), man_data)
                    pass
                pass

            # adding meta referer to force browser to send referrer
            # http://smerity.com/articles/2013/where_did_all_the_http_referrers_go.html
            man_data = re.sub(
                r'<head>(.*?)</head>',
                r'<head>\r\n\1\r\n<meta name="referrer" content="always">\r\n</head>',
                man_data,
                flags=re.DOTALL
            )

            # fix content length according to new content
            cl_diff = len(man_data) - ori_len
            man_data = re.sub(r'Content-Length(?::|: )(\d+)(?:\n|\r\n)', (
                lambda m:
                'Content-Length: {}\r\n'.format(
                    str(int(m.group(1)) + cl_diff)
                )
            ), man_data)
            data = man_data
            man_data = None
            pass

        # ------------------------------------------------------------
        # continue with the response
        self.factory.server.write(data)

        # ------------------------------------------------------------
        # TODO : Need to get Response time (If there is a way)
        # METHOD
        # Resource Type

        response_data = {
            "time": current_time_milliseconds(),
            "client_ip": rq_cilent_ip,
            "response_code": response.status,
            "date": response.getheader('Date'),
            "server": response.getheader('Server'),
            "response_length": len(data),  # headers + content
            "response_size": float(len(data)) / float(1024),  # in kb
            "keep_alive": response.getheader('Keep-Alive'),
            "connection": response.getheader('Connection'),
            "content_type": response.getheader('Content-Type'),
            "origin_hash": rq_ref,
            "destination_hash": res_ref,
            "request_uri": rq_uri_path,
            "response_type": f_type,
        }

        self.persist_and_notify(request_data, response_data)

        # ------------------------------------------------------------
        # add to session graph
        b = SessionGraph(rq_cilent_ip)
        b.add_edge(
            {'vertex_id': rq_ref},
            {'vertex_id': res_ref}
        )
        b.print_graph()
        b.save()

        # TODO : This is just checking, have to write a better sync method

        bg = ApplicationGraph()
        bg.add_edge(
            {'vertex_id': rq_ref},
            {'vertex_id': res_ref}
        )
        bg.print_graph()
        bg.save()
        pass

    # Proxy => Server
    def write(self, data):
        if data:
            self.transport.write(data)
            pass
        pass

    def persist_and_notify(self, request, response):
        merged_data = {
            "client_ip": request['client_ip'],
            "response_time": int(response['time'] - request['time']),
            "requested_time": request['time'],
            "responded_time": response['time'],
            "referer": request['referer'],
            "command": request['command'],
            "user_agent": request['user_agent'],
            "response_code": response['response_code'],
            "request_length": request['content_length'],  # content + headers
            "request_size": request['content_size'],  # in kb
            "response_length": response['response_length'],  # headers + content
            "response_size": response['response_size'],  # in kb
            "origin_hash": response['origin_hash'],
            "destination_hash": response['destination_hash'],
            "request_uri": response['request_uri'],
            "content_type": response['content_type'],
            "response_type": response['response_type'],
            "host": request['host'],
            "accept": request['accept'],
            "accept-language": request['accept-language'],
            "accept-encoding": request['accept-encoding'],
            "protocol_version": request['protocol_version'],
            "request-version": request['request-version'],
            "date": response['date'],
            "server": response['server'],
            "keep_alive": response['keep_alive'],
            "connection": response['connection']
        }
        serialized = pickle.dumps(merged_data)
        md5_sum = hashlib.md5(serialized).hexdigest()
        self.redis.set('session::{0}||type::transport||hash::{1}'.format(request['client_ip'], md5_sum), serialized)
        pass
    pass