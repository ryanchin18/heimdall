from modeler.factors import BaseFactor


class FactorRequestDistribution(BaseFactor):
    """
    Normal users will typically request for more-than one resource,
    but DDoS attackers usually request for single resource over and over again.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 3
        self._FACTOR_KEY = "FactorRequestDistribution"
        pass

    def compute(self):
        """
        Get the Request Distribution

        Variables Required:
            * Number of unique resources. (Number of Vertices (NV))
            * Number of requests per each vertex (NRPV) (In degree of vertex)
            * Total number of requests (TR) (Number of edges)

        Calculation:
            Average Requests Per Vertex (ARPR) = TR / NV
            Request Distribution (RD) = [i=0; i=NV]Sigma(|NRPV{i} - ARPR|) / NV

        Possible Analysis:
            If the calculated Request Distribution is equals to 0,
            that means all the requests originated from the client
            went to same set of resources.
        """
        nv = self._session_graph.graph.num_vertices()
        tr = self._session_graph.graph.num_edges()
        tr = tr if tr > 0 else 1
        if nv > 1:
            arpr = float(tr) / float(nv)
            diff = 0
            for v in self._session_graph.graph.vertices():
                diff += abs(arpr - v.in_degree())
            rd = float(diff) / float(nv)
            pass
        else:
            rd = 1.
            pass
        self.append_graph_factor('float', rd)
        print "Request Distribution : ", rd
        pass
    pass