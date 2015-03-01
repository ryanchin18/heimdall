from factors import BaseFactor


class FactorAverageResponseTime(BaseFactor):
    """
    For each request, server will take considerable amount of time to
    process and return a response. This factor defines the average number
    of responses that the server can produce with in a given time interval.
    If a client is waiting for the server to return a response, value of
    this factor must be greater than Average Request Frequency.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 2
        pass

    def compute(self):
        """
        Compute the average response time for each session
        variables needed: Time Taken for Each Response (in an array)
        avg_res_time = Time taken for N responses / N
        updating avg_res_time = ( avg_res_time * N + Time Taken For New Response) /  (N + 1)
        :return:
        """
        pass
    pass