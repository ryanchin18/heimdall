"""
HTTP request interceptor which entirely written using default python library.
Author  : Grainier Perera
Date    : 2015/01/16
"""
__author__ = 'grainier'

import socket
import select
import time
from http_request import HTTPRequest
from util.settings import loggers

# load server logger
logger = loggers['server']


class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pass

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception, e:
            print e
            return False
        pass

    pass


class Server:
    input_list = []
    channel = {}

    def __init__(self, config):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((config.interceptor.get('host', ''), config.interceptor.get('port', 9191)))
        self.server.listen(200)
        self.config = config

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            time.sleep(self.config.get('delay', 0.0001))
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                self.data = self.s.recv(self.config.get('buffer_size', 4096))
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()

    def on_accept(self):
        forward = Forward().start(
            self.config.destination.get('host', '127.0.0.1'),
            self.config.destination.get('port', 80)
        )
        clientsock, clientaddr = self.server.accept()
        self.client = clientaddr
        if forward:
            print clientaddr, "has connected"
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
        else:
            print "Can't establish connection with remote server.",
            print "Closing connection with client side", clientaddr
            clientsock.close()

    def on_close(self):
        print self.s.getpeername(), "has disconnected"
        # remove objects from input_list
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        # close the connection with client
        self.channel[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        self.channel[self.s].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        # here we can parse and/or modify the data before send forward
        request = HTTPRequest(data)

        # here we can extract http headers
        if hasattr(request, 'headers'):
            print('--------------------------------------------------------')
            print request.headers.dict
            print self.client
            print('--------------------------------------------------------')

        # print data
        self.channel[self.s].send(data)
