from factors import BaseFactor


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
            * Total Number of HTTP Client Error (4XX) occurrences (E)
            * Total Number of Requests Count (N)

        Calculation:
            HTTP Client Error Response Rate = E / N
        """
        total_requests = self._session_graph.get_graph_property('traffic_records')
        rcu = self._session_graph.get_graph_property('response_codes')
        total_errors = 0
        for code in rcu.keys():
            if 400 <= code < 500:
                total_errors += rcu[code]
                pass
            pass
        error_rate = 0 if total_errors <= 0 else float(total_errors) / float(total_requests)
        self.append_graph_factor('float', error_rate)
        print "HTTP Client Error Response Rate : ", error_rate
        pass
    pass