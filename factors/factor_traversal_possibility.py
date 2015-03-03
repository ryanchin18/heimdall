from factors import BaseFactor


class FactorTraversalPossibility(BaseFactor):
    """
    Web Scrapers, Bots, Spiders tend to use a specific method of crawling the web
    application. For this they use either breadth first or depth first traversing algorithm to
    crawl the application. With this factor it calculates, up to which percentage the client is
    using a predictable browsing pattern to browse the application. Then it can be used to
    identify Web Scrapers, Bots, Spiders from legitimate clients.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        self._FACTOR_KEY = "FactorTraversalPossibility"
        pass

    def compute(self):
        """
        Compute the Traversal Possibility

        Variables Required:
            *

        Calculation:
            Traversal Possibility =
        """
        pass
    pass