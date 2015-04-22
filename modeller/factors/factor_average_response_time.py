from modeller.factors import BaseFactor


class FactorAverageResponseTime(BaseFactor):
    """
    For each request made by the client, a web server will take a small amount of time to
    process and return a response. This factor defines the average time that will be taken
    by the server to produce a response. If a client is waiting for the server to return a
    response, value of this factor must be lower than Average Request Interval.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        self._FACTOR_KEY = "AverageResponseTime"
        pass

    def compute(self):
        """
        Compute the Average Response Time

        Variables Required:
            * Current Average Response Time (ART)
            * Total Response Count (TR) (Including new Response)
            * Time Taken For New Response (TFR)

        Calculation:
            * Average Response Time = ((ART * (TR - 1)) + TFR) / TR
        """
        art = self._session_graph.get_graph_property(self._FACTOR_KEY)
        art = art if art else 0.
        tr = self._session_graph.graph.num_edges()
        tr = tr if tr > 0 else 1

        tfr_milliseconds = self._traffic_record['response_time']
        tfr = float(tfr_milliseconds) / 1000.

        new_art = ((art * float(tr - 1)) + tfr) / float(tr)
        self.append_graph_factor('float', new_art)

        print "Average Response Time : ", new_art
        pass
    pass