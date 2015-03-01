from factors import BaseFactor


class FactorBrowsingDepth(BaseFactor):
    """
    Normal site users with commonly browse beyond the home page
    of a given site. Human users interaction with a website will
    resemble browsing more than that of a botnet.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        pass

    def compute(self):
        """
        RD = Max Span of Graph
        :return:
        """
        pass
    pass