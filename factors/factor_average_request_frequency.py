from factors import BaseFactor


class FactorAverageRequestFrequency(BaseFactor):
    """
    This feature considers the behaviour of the requester in terms of
    the average number of request made within a given time interval.
    This is essentially the frequency with which a requester attempts
    to access a given host.

    It takes into account the requests as whole (Per Graph) and as a
    single request (Per Node).
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        self._FACTOR_KEY = "FactorAverageRequestFrequency"
        pass

    def compute(self):
        """
        Compute the average time between two request for each session
        variables needed: Number of Requests (Per Graph or Per Node) (Check for Zero), Session Length in Seconds
        avg_req_frq = Session Length / Number of Requests
        :return:
        """
        pass
    pass