from factors import BaseFactor


class FactorResourceTypeRatio(BaseFactor):
    """
    This feature considers the type of content that is being requested.
    It considers if a requester is only retrieving HTML content but no
    ancillary data such as images, css or javascript files.

    It's better to define this as resource type percentages
    IE :
        .php : 60%, .js: 15%, .css : 10%, .jpg : 5%
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