"""

"""
from twisted.internet import protocol, reactor
from interceptor import ClientProtocol, HTTPRequest
from util import config, current_time_milliseconds


class ServerProtocol(protocol.Protocol):
    def __init__(self):
        self.request = None
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
        # here we can extract http request content
        request = HTTPRequest(data)

        request_uri = request.requestline \
            .replace(request.command, '') \
            .replace(request.request_version, '') \
            .strip()

        self.request = {
            "time": current_time_milliseconds(),
            "client_ip": str(self.transport.getPeer().host),
            "request_uri": request_uri,
            "referer": request.headers.get('Referer'),
            "command": request.command,
            "content_length": len(data),  # content + headers
            "content_size": float(len(data)) / float(1024),  # in kb
            "user_agent": request.headers.get('User-Agent'),
            "protocol_version": request.protocol_version,
            "request-version": request.request_version,
            "host": request.headers.get('Host'),
            "accept": request.headers.get('Accept'),
            "accept-language": request.headers.get('Accept-Language'),
            "accept-encoding": request.headers.get('Accept-Encoding')
        }

        # continue with the response
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