from factors import BaseFactor


class FactorSessionLength(BaseFactor):
    """
    This feature also elucidates general behaviour considering the
    requester's interaction with a given sight in terms of session time.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        pass

    def compute(self):
        """
        :return:
        """
        pass
    pass