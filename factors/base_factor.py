"""
The base class for all factors that used to identify an attack from a legitimate HTTP Traffic
"""


class BaseFactor(object):
    """
    Need to collect various factors from HTTP headers to be modeled and
    analysed using graphs. In order to make the process easier values of
    the factors should be represented in numerical values.
    """

    def __init__(self, session, session_graph, traffic_record):
        self._session = session
        self._session_graph = session_graph
        self._traffic_record = traffic_record
        self._FACTOR_INDEX = -1  # since this is an abstract class this is not a actual feature
        pass

    def compute(self):
        """
        Subclasses inherits from this class should override this method to
        perform the factor computation. And the value of the computed factor
        should be appended to the graph using either append_graph_factor() or
        append_vertex_factor() or append_edge_factor()
        """
        pass

    def append_graph_factor(self, inspected_ip, feature_value):
        # update graph property
        pass

    def append_vertex_factor(self, inspected_ip, feature_value):
        # get the vertex

        # update vertex
        pass

    def append_edge_factor(self, inspected_ip, feature_value):
        # get the vertex

        # update vertex
        pass

    def append_session_factor(self, inspected_ip, feature_value):
        """
        This is to be used if there's going to be SVM integration to analyse
        """
        pass
