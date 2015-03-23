from modeler.factors import BaseFactor
from common.graphs import ApplicationGraph, DFSearchVisitor, BFSearchVisitor
import graph_tool.all as gt


class FactorTraversalPossibility(BaseFactor):
    """
    Web Scrapers, Bots, Spiders tend to use a specific method of crawling the web
    application. For this they use either breadth first or depth first traversing algorithm to
    crawl the application. With this factor it calculates, up to which percentage the client is
    using a predictable browsing pattern to browse the application. Then it can be used to
    identify Web Scrapers, Bots, Spiders from legitimate clients.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 10
        self._FACTOR_KEY = "FactorTraversalPossibility"
        pass

    def compute(self):
        """
        Compute the Traversal Possibility

        Variables Required:
            *

        Calculation:
            Traversal Possibility =
        """
        # TODO : Index 0 might not always be the ROOT
        application_graph = ApplicationGraph()

        # for dfs
        dfs_visitor = DFSearchVisitor()
        gt.dfs_search(application_graph.graph, application_graph.graph.vertex(0), dfs_visitor)

        # for bfs
        bfs_visitor = BFSearchVisitor()
        gt.bfs_search(application_graph.graph, application_graph.graph.vertex(0), bfs_visitor)

        sequence = self._session_graph.get_graph_property('request_sequence')

        print "BFS predecessor : ", bfs_visitor.sequence
        print "DFS predecessor : ", dfs_visitor.sequence
        print "Traversal Possibility : ", sequence

        pass
    pass