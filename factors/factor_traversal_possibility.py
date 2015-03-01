from factors import BaseFactor


class FactorTraversalPossibility(BaseFactor):
    """

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