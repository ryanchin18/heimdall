from modeller.factors import BaseFactor, FactorAverageRequestInterval, FactorAverageResponseTime


class FactorRequestIntervalResponseTimeDifference(BaseFactor):
    """
    This will take average response time (ART) and average request
    interval (ARI) to he consideration and compute the difference.
    Main assumption is that a legitimate users will wait for
    a response to be return by the server before proceeding with a new request.
    User consecutively requesting form server without waiting for a response
    can make that user a suspect of a DDoS attack.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 9
        self._FACTOR_KEY = "RequestIntervalResponseTimeDifference"
        pass

    def compute(self):
        """
        Compute the Difference between average response time (ART) and average
        request interval (ARI)

        Factors Required:
            * average response time (ART)
            * average request interval (ARI)

        Calculation:
            diff = ARI - ART

        Analysis:
            if the diff is a negative value, there is a possibility of this
            session been an attack. Because attackers tend not wait for a response
            to be returned
        """
        ri_key = FactorAverageRequestInterval(None, None, None)._FACTOR_KEY
        rt_key = FactorAverageResponseTime(None, None, None)._FACTOR_KEY
        art = self._session_graph.get_graph_property(rt_key)
        ari = self._session_graph.get_graph_property(ri_key)

        diff = float(ari - art)
        self.append_graph_factor('float', diff)
        print "Request Interval & Response Time Difference : ", diff
        pass
    pass