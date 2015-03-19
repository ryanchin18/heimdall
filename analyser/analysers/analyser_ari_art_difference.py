from analyser.analysers import BaseAnalyser
from common.graph import SessionGraph


class AnalyserARTARIDifference(BaseAnalyser):
    """
    This analyser will take average response time (ART) and average request
    interval (ARI) to he consideration and compute a value to represent a
    severity factor. Main assumption is that a legitimate users will wait for
    a response to be return by the server before proceeding with a new request.
    User consecutively requesting form server without waiting for a response
    can make that user a suspect of a DDOS attack.
    """
    def __init__(self, session):
        BaseAnalyser.__init__(self, session)
        self._FACTOR_INDEX = 1
        self._FACTOR_KEY = "ARTARIDifference"
        self._WEIGHT = 0.5
        pass

    def analyse(self):
        """
        Compute the Difference between average response time (ART) and average
        request interval (ARI)

        Factors Required:
            * average response time (ART)
            * average request interval (ARI)

        Calculation:
            diff = ARI - ART

        Analysis:
            if the diff is a negative value, there is a possibility of this
            session been an attack.
        """
        # load respective session graph
        session_graph = SessionGraph(self._session)

        # analyse the factors
        arst = session_graph.get_graph_property('FactorAverageResponseTime')
        arqi = session_graph.get_graph_property('FactorAverageRequestInterval')

        diff = arqi - arst
        s = 0 if diff > 0 else (-1 * diff)

        self.update_severity(s)
        pass
    pass