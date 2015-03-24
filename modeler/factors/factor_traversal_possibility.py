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
        request_sequence = self._session_graph.get_graph_property('request_sequence')

        # for dfs
        dfs_visitor = DFSearchVisitor()
        gt.dfs_search(application_graph.graph, application_graph.graph.vertex(0), dfs_visitor)
        dfs_match = self.get_longest_match(dfs_visitor.sequence, request_sequence)
        dfs_match_percentage = (float(dfs_match) / float(len(dfs_visitor.sequence))) * 100.

        # for bfs
        bfs_visitor = BFSearchVisitor()
        gt.bfs_search(application_graph.graph, application_graph.graph.vertex(0), bfs_visitor)
        bfs_match = self.get_longest_match(bfs_visitor.sequence, request_sequence)
        bfs_match_percentage = (float(bfs_match) / float(len(bfs_visitor.sequence))) * 100.

        print "BFS sequence : ", bfs_visitor.sequence, " | match : ", bfs_match_percentage
        print "DFS sequence : ", dfs_visitor.sequence, " | match : ", dfs_match_percentage
        print "Traversal Possibility : ", request_sequence
        pass

    def get_longest_match(self, search_sequence, request_sequence):
        ss_len = len(search_sequence)
        # there should be at-least 10 nodes
        if ss_len > 10:
            # decremental iteration to get the window value
            # (only take up-to 1 /4 of length), checking small windows will give false alarm
            for i in range(ss_len, ss_len / 4, -1):
                # Split the search sequence in to chunks of "i" elements
                for j in xrange(0, ss_len, i):
                    # check whether that chunk is in request sequence
                    chunk = search_sequence[j:j+i]
                    is_sub_array = self.is_sub_array(request_sequence, chunk)

                    # length of the should still be checked,
                    # "i = 2", [1,2], [3] <- but this can be the match
                    if is_sub_array and len(chunk) == i:
                        return i
                        pass
                    pass
                pass
            pass
        return 0
        pass

    def is_sub_array(self, array, sub_array):
        sub_len = len(sub_array)
        return any((sub_array == array[i:i+sub_len]) for i in xrange(len(array)-sub_len+1))
        pass

    pass