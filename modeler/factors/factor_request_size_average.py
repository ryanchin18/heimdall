from modeler.factors import BaseFactor


class FactorRequestSizeAverage(BaseFactor):
    """
    This factor represents the average size of the content that a requester sends
    with a request.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 6
        self._FACTOR_KEY = "FactorRequestSizeAverage"
        pass

    def compute(self):
        """
        Compute the Request Size Average

        Variables Required:
            * Previously Calculated Request Size Average (RSA)
            * Total Requests Count (TR)
            * New Request Size (RS)

        Calculation:
            Request Size Average (RSA) = ((RSA * (TR - 1)) + RS) / TR
        """
        rsa = self._session_graph.get_graph_property(self._FACTOR_KEY)
        rsa = rsa if rsa else 0.
        tr = self._session_graph.graph.num_edges()
        rs = self._traffic_record['request_size']
        rsa = ((float(rsa) * (float(tr) - 1.)) + float(rs)) / float(tr)
        self.append_graph_factor('float', rsa)

        print "Request Size Average : ", rsa
        pass
    pass