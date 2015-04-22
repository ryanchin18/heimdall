from modeller.factors import BaseFactor


class FactorAverageRequestInterval(BaseFactor):
    """
    This factor will considers the behaviour of the requester in terms of the average time
    between two requests per session. Therefore, this factor value will represent the
    frequency with which a requester attempts to access a given resource (webpage,
    image, style sheet, etc...) of the application. It takes into account the requests as whole
    (Per Graph).
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 0
        self._FACTOR_KEY = "AverageRequestInterval"
        pass

    def compute(self):
        """
        Compute the Average Request Interval

        Variables Required:
            * Length of the Session in Seconds (SL)
            * Total Requests Count (TR)

        Calculation:
            Average Request Interval (ARI) = SL / TR
        """
        sl_milliseconds = self._session_graph.get_session_length()
        sl = float(sl_milliseconds) / 1000.
        tr = self._session_graph.graph.num_edges()
        tr = tr if tr > 0 else 1

        ari = float(sl) / float(tr)
        self.append_graph_factor('float', ari)
        print "Average Request Interval : ", ari
        pass
    pass