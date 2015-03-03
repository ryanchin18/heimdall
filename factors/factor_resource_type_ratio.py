from factors import BaseFactor


class FactorResourceTypeRatio(BaseFactor):
    """
    This feature considers the type of content that is being requested. It considers if a
    requester is only retrieving HTML content but no ancillary data such as images, CSS
    or JavaScript files.
    i.e.: .php : 60%, .js: 15%, .css : 10%, .jpg : 5%
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 7
        self._FACTOR_KEY = "FactorResourceTypeRatio"
        pass

    def compute(self):
        # TODO : This might be possible to do like the opposite of the User-Agent Cycling Ratio
        """
        Compute the Resource Type Ratio

        Variables Required:
            *

        Calculation:
            Resource Type Ratio =
        """
        pass
    pass