import operator
from modeller.factors import BaseFactor


class FactorVarianceRequestInterval(BaseFactor):
    """
    While many DDOS attacks use a very simplistic brute force approach, some have
    incorporated a slightly more sophisticated approach by making burst requests in order
    to avoid being blocked by simple rules which allow only a certain number of requests
    within a time frame.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 11
        self._FACTOR_KEY = "VarianceRequestInterval"
        pass

    def compute(self):
        """
        Compute the Variance Request Interval

        Variables Required:
            * Number of Intervals (NI)
            * Number of Requests Per each Interval (NRPI)
            * Total number of requests (TR) (Number of edges)

        Calculation:
            Average Requests Per Interval (ARPI) = TR / NI
            Variance Request Interval (VRI) = [i=0; i=NI]Sigma(|NRPI{i} - ARPI|) / NI

        Possible Analysis:

        """
        request_intervals = sorted(
            self._session_graph.get_graph_property('request_intervals').iteritems(),
            key=operator.itemgetter(1),
            reverse=True
        )
        ni = len(request_intervals)
        tr = self._session_graph.graph.num_edges()
        tr = tr if tr > 0 else 1
        if ni > 1:
            arpi = float(tr) / float(ni)
            diff = 0
            for i in request_intervals:
                diff += abs(i[1] - arpi)
            vri = float(diff) / float(ni)
            pass
        else:
            vri = 1.
            pass
        self.append_graph_factor('float', vri)

        print "Variance Request Interval : ", vri
        pass
    pass