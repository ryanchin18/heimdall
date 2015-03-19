import operator
from modeler.factors import BaseFactor


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
        """
        Compute the Resource Type Ratio

        Variables Required:
            * Total Requests Count,
            * Unique Resource Types per session and their usages as a Dictionary
              sorted by Usage in descending order

        Calculation:
        Assume sorted Resource Types usage dictionary as this
        {
             ".html" : 7,
             ".png" : 2,
             ".css" : 1,
             ".js" : 1,
        }

        According to that;
             Total requests = Sigma (Resource Types Usage)
             Total requests = 11
             Minority Resource Types Usage = Total requests - Majority User-Agent Usage
             Minority Resource Types Usage = 11 -  7
             Resource Types Ratio = Minority Resource Types Usage / Total requests
             Resource Types Ratio = (11 -  7) / 11 = 0.364

        If the value of Resource Types Ratio is equal to 0, that implies
        someone tried to consecutively request for same type of resource (like hot-linking)
        """
        total_requests = self._session_graph.get_graph_property('traffic_records')
        sorted_rt_usage = sorted(
            self._session_graph.get_graph_property('resource_types').iteritems(),
            key=operator.itemgetter(1),
            reverse=True
        )
        resource_type_ratio = float(total_requests - sorted_rt_usage[0][1]) / float(total_requests)
        self.append_graph_factor('float', resource_type_ratio)
        print "Resource Type Ratio : ", resource_type_ratio
        pass
    pass