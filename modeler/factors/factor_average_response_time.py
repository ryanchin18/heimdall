from modeler.factors import BaseFactor


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
            * Number of Responses (N) (Including new Response)
            * Time Taken For New Response (T)

        Calculation:
            * Average Response Time = ((A * (N - 1)) + T) / N
        """
        current_average = self._session_graph.get_graph_property(self._FACTOR_KEY)
        current_average = current_average if current_average else 0.
        total_responses = self._session_graph.graph.num_edges()

        response_time_milliseconds = self._traffic_record['response_time']
        response_time_seconds = float(response_time_milliseconds) / 1000.

        average_response_time = ((current_average * float(total_responses - 1)) + response_time_seconds) / float(total_responses)
        self.append_graph_factor('float', average_response_time)

        print "Average Response Time : ", average_response_time
        pass
    pass