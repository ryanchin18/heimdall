from factors import BaseFactor


class FactorRequestPayloadSizeAverage(BaseFactor):
    """
    This feature looks at the size of the content that a requester
    sends with a request.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        self._FACTOR_KEY = "FactorRequestPayloadSizeAverage"
        pass

    def compute(self):
        """
        variables needed:
            * Previously Calculated Request Payload Size Average,
            * Total Requests Count,
            * Size of New Request

        avg_req_size = Size for N requests / N
        updating avg_req_size = ( avg_req_size * N + Size of New Request) / ( N + 1 )
        :return:
        """
        pass
    pass