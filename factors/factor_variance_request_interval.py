from factors import BaseFactor


class FactorVarianceRequestInterval(BaseFactor):
    """
    While many DDOS attacks use a very simplistic brute force approach,
    some have incorporated a slightly more sophisticated approach by making
    burst requests in order to avoid being blocked by simple rules which
    allow only a certain number of requests within a time frame.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        pass

    def compute(self):
        """
        No Idea How to do this
        :return:
        """
        pass
    pass