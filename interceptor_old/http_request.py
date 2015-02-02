"""
Parse socket recv buffer in to HTTPRequest
http://stackoverflow.com/questions/2115410/does-python-have-a-module-for-parsing-http-requests-and-responses
Author  : Grainier Perera
Date    : 2015/01/16
"""
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO


class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()
        pass

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message
        pass

    pass