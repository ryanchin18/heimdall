from factors import BaseFactor


class FactorAverageResponseTime(BaseFactor):
    """
    For each request made by the client, a web server will take a small amount of time to
    process and return a response. This factor defines the average time that will be taken
    by the server to produce a response. If a client is waiting for the server to return a
    response, value of this factor must be lower than Average Request Interval.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 2
        self._FACTOR_KEY = "FactorAverageResponseTime"
        pass

    def compute(self):
        """
        Compute the Average Response Time

        Variables Required:
            * Current Average Response Time (A)
            * Number of Responses (N)
            * Time Taken For New Response (T)

        Calculation:
            * Average Response Time = ( A * N + T) / (N + 1)
        """
        pass
    pass