from factors import BaseFactor


class FactorPercentageConsecutiveRequests(BaseFactor):
    """
    To further elucidate the requester's interaction
    with a given site we additionally consider how many
    of the requests made were consecutive as another
    window onto frequency.
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