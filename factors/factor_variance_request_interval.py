from factors import BaseFactor


class FactorVarianceRequestInterval(BaseFactor):
    """
    While many DDOS attacks use a very simplistic brute force approach, some have
    incorporated a slightly more sophisticated approach by making burst requests in order
    to avoid being blocked by simple rules which allow only a certain number of requests
    within a time frame.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        self._FACTOR_KEY = "FactorVarianceRequestInterval"
        pass

    def compute(self):
        """
        Compute the Variance Request Interval

        Variables Required:
            *

        Calculation:
            Variance Request Interval =
        """
        pass
    pass