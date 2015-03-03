from factors import BaseFactor


class FactorRequestPayloadSizeAverage(BaseFactor):
    """
    This factor represents the average size of the content (payload) that a requester sends
    with a request.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 6
        self._FACTOR_KEY = "FactorRequestPayloadSizeAverage"
        pass

    def compute(self):
        """
        Compute the Request Payload Size Average

        Variables Required:
            * Previously Calculated Request Payload Size Average (A)
            * Total Requests Count (N)
            * Size of New Request (S)

        Calculation:
            Request Payload Size Average = ( A * N + S) / N + 1
        """
        pass
    pass