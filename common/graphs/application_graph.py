__author__ = 'grainier'

from common.graphs import SessionGraph
import graph_tool.all as gt


class ApplicationGraph(SessionGraph):
    def __init__(self):
        SessionGraph.__init__(self, 'base', temp=False)
        pass

    def sync(self, session):

        pass

    def filter(self, prop):

        pass

    def remove_parallel_edges(self):
        gt.remove_parallel_edges(self.graph)
        pass