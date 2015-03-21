__author__ = 'grainier'

from common.graphs import SessionGraph


class ApplicationGraph(SessionGraph):
    def __init__(self):
        SessionGraph.__init__(self, 'base', temp=False)
        pass

    def sync(self, session):

        pass

    def filter(self, prop):

        pass