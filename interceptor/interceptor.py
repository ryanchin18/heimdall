"""
inspiration taken from Erik Johansson's transparent proxy
https://github.com/erijo/transparent-proxy
"""
from twisted.web import http
from twisted.internet import reactor, protocol
from twisted.python import log
from common import REDIS_POOL, config, current_time_milliseconds, redis_key_template
from urlparse import urlparse
import cPickle as pickle
import hashlib
import redis
import re


class ProxyClient(http.HTTPClient):
    """
    The proxy client connects to the real server, fetches the response and
    sends it back to the original client. fetched responses and requests
    can be tampered or analysed using this approach.
    """
    def __init__(self, method, uri, postData, headers, originalRequest):
        self.redis = redis.Redis(connection_pool=REDIS_POOL)
        self.method = method
        self.uri = uri
        self.postData = postData
        self.headers = list(headers)
        self.originalRequest = originalRequest
        self.contentLength = None
        headers_dict = {x: y[0] for x, y in self.headers}
        self.req = {
            "time": current_time_milliseconds(),
            "client_ip": self.originalRequest.getClientIP(),
            "request_uri": self.uri,
            "referer": headers_dict['Referer'] if 'Referer' in headers_dict else None,
            "command": self.method,
            "content_length": len(self.postData),  # content + headers
            "content_size": float(len(self.postData)) / float(1024),  # in kb
            "user_agent": headers_dict['User-Agent'] if 'User-Agent' in headers_dict else None,
            "protocol_version": self.originalRequest.clientproto,
            "host": headers_dict['Host'] if 'Host' in headers_dict else None,
            "accept": headers_dict['Accept'] if 'Accept' in headers_dict else None,
            "accept-language": headers_dict['Accept-Language'] if 'Accept-Language' in headers_dict else None,
            "accept-encoding": headers_dict['Accept-Encoding'] if 'Accept-Encoding' in headers_dict else None
        }
        pass

    def sendRequest(self):
        """
        Send the request to the destination server
        :return:
        """
        log.msg("Sending request: %s %s" % (self.method, self.uri))
        self.sendCommand(self.method, self.uri)

    def sendHeaders(self):
        for key, values in self.headers:
            if key.lower() == 'connection':
                values = ['close']
            elif key.lower() == 'keep-alive':
                next

            for value in values:
                self.sendHeader(key, value)
        self.endHeaders()

    def sendPostData(self):
        log.msg("Sending POST data")
        self.transport.write(self.postData)
        pass

    def connectionMade(self):
        log.msg("HTTP connection made")
        self.sendRequest()
        self.sendHeaders()
        if self.method == 'POST' or len(self.postData) > 0:
            self.sendPostData()
            pass
        pass

    def handleStatus(self, version, code, message):
        log.msg("Got server response: %s %s %s" % (version, code, message))
        self.originalRequest.setResponseCode(int(code), message)
        pass

    def handleHeader(self, key, value):
        if key.lower() == 'content-length':
            self.contentLength = value
        else:
            self.originalRequest.responseHeaders.addRawHeader(key, value)
        pass

    def handleResponse(self, data):
        data = self.originalRequest.processResponse(data)
        data = self.injectReferer(data)
        if self.contentLength is not None:
            self.originalRequest.setHeader('Content-Length', len(data))
            pass

        self.res = {
            "time": current_time_milliseconds(),
            "response_code": self.originalRequest.code,
            "response_length": len(data),  # headers + content
            "response_size": float(len(data)) / float(1024),  # in kb
        }

        # persist data
        self.persist_and_notify(self.req, self.res)

        # continue with the response
        self.originalRequest.write(data)
        # terminate connection
        try:
            self.originalRequest.finish()
            self.transport.loseConnection()
        except RuntimeError, e:
            log.err("Request.finish calling issue occurred, ignoring exception.")
            pass
        pass

    def injectReferer(self, data):
        if not self.req["referer"]:
            # client request doesn't have referrer. inject "o_ref"
            if config.get('force_append_referrer', False):
                # url of response for this request will be the referrer of
                # requests originated from rendered response
                rq_uri = self.req['request_uri']
                url = urlparse(rq_uri)
                rq_uri_path = url.path if url.path == '/' else url.path.rstrip('/')
                res_ref = hashlib.md5(rq_uri_path).hexdigest()
                # self.redis.set(redis_key_template.format("any", "url", res_ref), rq_uri_path)

                # get the file type (file extinction) of response that's going to generate
                try:
                    f_type = rq_uri_path[rq_uri_path.rindex('.'):]
                except ValueError:
                    f_type = 'unknown'
                    pass

                if f_type not in config.do_not_tamper_file_types:
                    # if the file type not in DO_NOT_TAMPER_FILE_TYPES, inject o_ref values
                    data = re.sub(r'(href|src)(=\"|=\'|=)(.*?)(\"|\'|>| |/>)', (
                        lambda m:
                        '{0}{1}{2}&o_ref={4}{3}'.format(
                            m.group(1), m.group(2), m.group(3), m.group(4), res_ref
                        )
                        if '?' in m.group(3)
                        else '{0}{1}{2}?o_ref={4}{3}'.format(
                            m.group(1), m.group(2), m.group(3), m.group(4), res_ref
                        )
                    ), data)

                    # adding meta referer to force browser to send referrer
                    # http://smerity.com/articles/2013/where_did_all_the_http_referrers_go.html
                    data = re.sub(
                        r'<head>(.*?)</head>',
                        r'<head>\r\n\1\r\n<meta name="referrer" content="always">\r\n</head>',
                        data,
                        flags=re.DOTALL
                    )
                    pass
                pass
            pass
        return data
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
            "request_uri": request['request_uri'],
            "host": request['host'],
            "accept": request['accept'],
            "accept-language": request['accept-language'],
            "accept-encoding": request['accept-encoding'],
            "protocol_version": request['protocol_version'],
        }
        serialized = pickle.dumps(merged_data)
        md5_sum = hashlib.md5(serialized).hexdigest()
        self.redis.set(redis_key_template.format(request['client_ip'], "transport", md5_sum), serialized)
        pass


class ProxyClientFactory(protocol.ClientFactory):
    def __init__(self, method, uri, postData, headers, originalRequest):
        self.protocol = ProxyClient
        self.method = method
        self.uri = uri
        self.postData = postData
        self.headers = headers
        self.originalRequest = originalRequest
        pass

    def buildProtocol(self, addr):
        return self.protocol(
            self.method,
            self.uri,
            self.postData,
            self.headers,
            self.originalRequest
        )

    def clientConnectionFailed(self, connector, reason):
        log.err("Server connection failed: %s" % reason)
        self.originalRequest.setResponseCode(504)
        self.originalRequest.finish()
        pass


class ProxyRequest(http.Request):
    def __init__(self, channel, queued, reactor=reactor):
        http.Request.__init__(self, channel, queued)
        self.reactor = reactor
        pass

    def process(self):
        # TODO: fix this  ban can happen here
        # if self.is_ban():
        #     log.msg("DDoS attacker detected, Sending status code 400")
        #     self.setResponseCode(400)
        #     self.finish()
        #     return

        host = self.getHeader('host')
        if not host:
            log.err("No host header given")
            self.setResponseCode(400)
            self.finish()
            return

        port = 80
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
            pass

        self.setHost(host, port)

        self.content.seek(0, 0)
        postData = self.content.read()
        factory = ProxyClientFactory(
            self.method,
            self.uri, postData,
            self.requestHeaders.getAllRawHeaders(),
            self
        )

        # self.reactor.connectTCP(host, port, factory)
        self.reactor.connectTCP(
            config.destination.get('host', ''),
            config.destination.get('port', 80),
            factory
        )
        pass

    def processResponse(self, data):
        return data

    def is_ban(self):
        ip = self.originalRequest.getClientIP()
        # sr = SeverityRecord(ip)
        # return sr.get_level() > 5
        return False
        pass

    pass


class TransparentProxy(http.HTTPChannel):
    requestFactory = ProxyRequest
    pass


class ProxyFactory(http.HTTPFactory):
    protocol = TransparentProxy
    pass