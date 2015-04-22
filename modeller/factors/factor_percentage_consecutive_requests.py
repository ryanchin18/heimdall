from modeller.factors import BaseFactor


class FactorPercentageConsecutiveRequests(BaseFactor):
    """
    To further elucidate the requester's interaction with a given site we additionally
    consider how many of the requests made were consecutive as another window onto
    frequency.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 4
        self._FACTOR_KEY = "PercentageConsecutiveRequests"
        pass

    def compute(self):
        """
        Compute the Percentage Consecutive Requests

        Variables Required:
            * Total number of requests (TR) (Number of edges)
            * Number of consecutive requests (CR)

        Calculation:
            Percentage Consecutive Requests (PCR) = (CR / TR) * 100

        Possible Analysis:
            If the calculated value is close to 100, that implies the
            requester consecutively requested for a specific resource.
        """
        tr = self._session_graph.graph.num_edges()
        cr = self._session_graph.get_graph_property('consecutive_requests')
        pcr = float(cr) / float(tr) * 100

        self.append_graph_factor('float', pcr)
        print "Percentage Consecutive Requests : ", pcr
        pass
    pass