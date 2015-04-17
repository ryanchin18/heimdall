from modeller.factors import BaseFactor
import graph_tool.all as gt


class FactorBrowsingDepth(BaseFactor):
    """
    Normal site users with commonly browse beyond the home page of a given site.
    Human users interaction with a website will resemble browsing more than that of a
    BotNet.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 3
        self._FACTOR_KEY = "FactorBrowsingDepth"
        pass

    def compute(self):
        """
        Get the Browsing Depth

        Variables Required:
            * Max Span of Graph

        Calculation:
            Browsing Depth (BD) = Edges on Minimum Span Tree (from initial vertex)

            Get the minimum spanning tree using Prim's algorithm

        Analysis:
            More browsing depth means that the requester isn't targeting on a
            particular resource
        """
        mst = gt.min_spanning_tree(
            self._session_graph.graph,
            root=self._session_graph.graph.vertex(0)
        )
        all_edges = mst.get_array()

        # edge in mst will have a value of 1,
        # and other edges will have a value of 0
        # therefore, sum of edges will give number of edges in mst.
        # this way parallel edges will also be ignored.
        edges_in_path = sum(all_edges)
        bd = edges_in_path
        self.append_graph_factor('int', bd)

        print "Browsing Depth : ", bd
        pass
    pass