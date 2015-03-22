from modeler.factors import BaseFactor


class FactorAverageRequestInterval(BaseFactor):
    """
    This factor will considers the behaviour of the requester in terms of the average time
    between two requests per session. Therefore, this factor value will represent the
    frequency with which a requester attempts to access a given resource (webpage,
    image, style sheet, etc...) of the application. It takes into account the requests as whole
    (Per Graph) and as a single request (Per Node).
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        self._FACTOR_KEY = "FactorAverageRequestInterval"
        pass

    def compute(self):
        """
        Compute the Average Request Interval

        Variables Required:
            * Length of the Session in Seconds (T)
            * Number of Requests (Per Graph or Per Node) (N)

        Calculation:
            Average Request Interval = L / N
        """
        session_length_milliseconds = self._session_graph.get_session_length()
        session_length_seconds = float(session_length_milliseconds) / 1000.
        total_requests = self._session_graph.graph.num_edges()

        average_request_interval = float(session_length_seconds) / float(total_requests)
        self.append_graph_factor('float', average_request_interval)
        print "Average Request Interval : ", average_request_interval
        pass
    pass