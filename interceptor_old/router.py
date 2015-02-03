"""
HTTP request interceptor which entirely written using default python library.
Author  : Grainier Perera
Date    : 2015/01/16
"""
import socket
import select
import time
from util.settings import loggers
from interceptor_old import Destination
from interceptor_old import HTTPRequest
logger = loggers['server']


class Router:
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
        destination = Destination().start(
            self.config.destination.get('host', '127.0.0.1'),
            self.config.destination.get('port', 80)
        )
        clientsock, clientaddr = self.server.accept()
        self.client = clientaddr
        if destination:
            print clientaddr, "has connected"
            self.input_list.append(clientsock)
            self.input_list.append(destination)
            self.channel[clientsock] = destination
            self.channel[destination] = clientsock
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

        print(vars(request))

        # here we can extract http headers
        if hasattr(request, 'headers'):
            content_len = int(request.headers.getheader('content-length', 0))
            post_body = request.rfile.read(content_len)
            print('--------------------------------------------------------')
            print('body : %s' % post_body)
            print request.headers.dict
            print self.client
            print('--------------------------------------------------------')

        # print data
        self.channel[self.s].send(data)
        pass

    pass
