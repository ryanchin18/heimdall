from modeller.factors import BaseFactor


class FactorResponseSizeAverage(BaseFactor):
    """
    This factor represents the average size of the content that the web server
    sends with the response.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 9
        self._FACTOR_KEY = "FactorResponseSizeAverage"
        pass

    def compute(self):
        """
        Compute the Response Size Average

        Variables Required:
            * Previously Calculated Response Size Average (RSA)
            * Total Responses Count (TR)
            * Size of New Response (RS)

        Calculation:
           Response Size Average (RSA) = ((RSA * (TR - 1)) + RS) / TR
        """
        rsa = self._session_graph.get_graph_property(self._FACTOR_KEY)
        rsa = rsa if rsa else 0.
        tr = self._session_graph.graph.num_edges()
        tr = tr if tr > 0 else 1
        rs = self._traffic_record['response_size']
        rsa = ((float(rsa) * (float(tr) - 1.)) + float(rs)) / float(tr)
        self.append_graph_factor('float', rsa)

        print "Response Size Average : ", rsa
        pass
    pass