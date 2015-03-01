from factors import BaseFactor


class FactorHTTPClientErrorResponseRate(BaseFactor):
    """
    Considers http response rate, primarily looking for error codes
    that may signal a cache busting attack.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 1
        pass

    def compute(self):
        """
        This will compute the ratio between Total number of Error Codes
        and the Total Number of Requests have been made per each session.
        When computing this factor, it takes total HTTP Client Error (4XX)
        codes as Total number of Error Codes.

        HTTP Codes : http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html

        error_res_rate = 0 if total_error_statuses <= 0 else float(total_error_statuses) / float(total_requests)
        :return:
        """
        pass
    pass