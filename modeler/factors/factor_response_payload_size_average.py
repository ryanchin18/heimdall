from modeler.factors import BaseFactor


class FactorResponsePayloadSizeAverage(BaseFactor):
    """
    This factor represents the average size of the content (payload) that the web server
    sends with the response.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 8
        self._FACTOR_KEY = "FactorResponsePayloadSizeAverage"
        pass

    def compute(self):
        """
        Compute the Response Payload Size Average

        Variables Required:
            * Previously Calculated Response Payload Size Average (A)
            * Total Responses Count (N)
            * Size of New Response (S)

        Calculation:
            Response Payload Size Average = ( A * N + S) / N + 1
        """
        pass
    pass