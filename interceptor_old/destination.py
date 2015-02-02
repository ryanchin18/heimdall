"""
Destination Class
Author  : Grainier Perera
Date    : 2015/01/16
"""
import socket


class Destination:
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