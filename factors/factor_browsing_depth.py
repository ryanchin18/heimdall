from factors import BaseFactor


class FactorBrowsingDepth(BaseFactor):
    """
    Normal site users with commonly browse beyond the home page of a given site.
    Human users interaction with a website will resemble browsing more than that of a
    BotNet.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        self._FACTOR_KEY = "FactorBrowsingDepth"
        pass

    def compute(self):
        """
        Get the Variance Request Interval

        Variables Required:
            * Max Span of Graph

        Calculation:
            Variance Request Interval = Max Span of Graph
        """
        pass
    pass