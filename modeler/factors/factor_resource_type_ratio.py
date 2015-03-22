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
            * Total Requests Count (TR),
            * Unique Resource Types per session and their usages as a Dictionary
              sorted by Usage in descending order. (SRT)

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
             Resource Types Ratio (RTR) = Minority Resource Types Usage / Total requests
             RTR = (11 -  7) / 11 = 0.364

        If the value of Resource Types Ratio is equal to 0, that implies
        someone tried to consecutively request for same type of resource (like hot-linking)
        """
        tr = self._session_graph.graph.num_edges()
        tr = tr if tr > 0 else 1
        srt = sorted(
            self._session_graph.get_graph_property('resource_types').iteritems(),
            key=operator.itemgetter(1),
            reverse=True
        )
        rtr = float(tr - srt[0][1]) / float(tr)
        self.append_graph_factor('float', rtr)
        print "Resource Type Ratio : ", rtr
        pass
    pass