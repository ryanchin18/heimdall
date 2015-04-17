from modeller.factors import BaseFactor


class FactorHTTPClientErrorResponseRate(BaseFactor):
    """
    This factor will compute the ratio between total number of error codes and the total
    number of requests have been made per each session. This factor become helpful to
    identify cache busting attacks.

    HTTP Codes : http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 4
        self._FACTOR_KEY = "FactorHTTPClientErrorResponseRate"
        pass

    def compute(self):
        """
        Compute the HTTP Client Error Response Rate

        Variables Required:
            * Response code Usage (RCU)
            * Total Number of HTTP Client Error (4XX) occurrences (TE)
            * Total Number of Requests (TR)

        Calculation:
            HTTP Client Error Response Rate (ERR) = TE / TR
        """
        tr = self._session_graph.graph.num_edges()
        tr = tr if tr > 0 else 1
        rcu = self._session_graph.get_graph_property('response_codes')
        te = 0
        for code in rcu.keys():
            if 400 <= code < 500:
                te += rcu[code]
                pass
            pass
        err = 0 if te <= 0 else float(te) / float(tr)
        self.append_graph_factor('float', err)
        print "HTTP Client Error Response Rate : ", err
        pass
    pass