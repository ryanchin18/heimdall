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
        self._FACTOR_INDEX = -1  # since this is an abstract class this is not a actual index
        self._FACTOR_KEY = "Factor"  # since this is an abstract class this is not a actual key
        pass

    def compute(self):
        """
        Subclasses inherits from this class should override this method to
        perform the factor computation. And the value of the computed factor
        should be appended to the graph using either append_graph_factor() or
        append_vertex_factor() or append_edge_factor()
        """
        pass

    def append_graph_factor(self, value_type, feature_value):
        self._session_graph.add_graph_property(self._FACTOR_KEY, value_type, feature_value)
        pass

    def append_vertex_factor(self, value_type, feature_value, vertex=None, vertex_id=None):
        if vertex:
            self._session_graph.add_vertex_property(
                self._FACTOR_KEY, value_type, feature_value, vertex=vertex
            )
        elif vertex_id:
            self._session_graph.add_vertex_property(
                self._FACTOR_KEY, value_type, feature_value, vertex_id=vertex_id
            )
        pass

    def append_edge_factor(
            self, value_type, feature_value, edge=None,
            source_vertex=None, destination_vertex=None,
            source_vertex_id=None, destination_vertex_id=None):
        # update vertex
        if edge:
            self._session_graph.add_edge_property(
                self._FACTOR_KEY, value_type, feature_value, edge=edge
            )
            pass
        elif source_vertex and destination_vertex:
            self._session_graph.add_edge_property(
                self._FACTOR_KEY, value_type, feature_value,
                source_vertex=source_vertex, destination_vertex=destination_vertex
            )
            pass
        elif source_vertex_id and destination_vertex_id:
            self._session_graph.add_edge_property(
                self._FACTOR_KEY, value_type, feature_value,
                source_vertex_id=source_vertex_id, destination_vertex_id=destination_vertex_id
            )
            pass
        else:
            # TODO Throw an exception
            print "insufficient parameters"
            pass
        pass

    def append_session_factor(self, value_type, feature_value):
        """
        This is to be used if there's going to be SVM integration to analyse
        """
        pass
