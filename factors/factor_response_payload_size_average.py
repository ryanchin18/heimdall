from factors import BaseFactor


class FactorResponsePayloadSizeAverage(BaseFactor):
    """
    This feature looks at the size of the content that a requester
    is retrieving.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        pass

    def compute(self):
        """
        variables needed:
        * Previously Calculated Response Payload Size Average,
        * Total Response Count,
        * Size of New Response

        avg_res_size = Size for N responses / N
        updating avg_res_size = ( avg_res_size * N + Size of New Response) / ( N + 1 )
        :return:
        """
        pass
    pass