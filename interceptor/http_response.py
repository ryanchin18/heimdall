"""
Since there is no Python function to parse HTTP
Response originating from the server, we need to
manually parse the content of response headers.

Refer to    : http://stackoverflow.com/a/24729316
Author      : Grainier Perera
Date        : 2015/02/10
"""
from httplib import HTTPResponse
from StringIO import StringIO
__all__ = []


class SocketSimulator():
    """
    Simulate a simple socket to parse headers
    from a raw header string.
    """
    def __init__(self, response_str):
        self._file = StringIO(response_str)
        pass

    def makefile(self, *args, **kwargs):
        return self._file
    pass


def parse_response(response_str):
    """
    Parse_response method will parse the content
    of a raw response string and produce a HTTPResponse object
    :param response_str: raw response string
    :return: Parsed HTTPResponse object
    """
    source = SocketSimulator(response_str)
    response = HTTPResponse(source)
    response.begin()
    return response